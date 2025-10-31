"""
Markdown Converter using Docling
Converts PDFs to structured markdown with page number tracking
"""

from docling.document_converter import DocumentConverter
from pathlib import Path
from typing import Dict, List, Any
import re


class MarkdownConverter:
    """Convert PDF to markdown with page tracking using Docling"""
    
    def __init__(self):
        self.converter = DocumentConverter()
    
    def convert_pdf_to_markdown(self, pdf_path: str) -> Dict[str, Any]:
        """
        Convert PDF to markdown with page references
        
        Returns:
            dict with markdown, page_mapping, and metadata
        """
        print(f"Converting PDF to markdown: {pdf_path}")
        
        # Convert PDF using Docling
        result = self.converter.convert(pdf_path)
        doc = result.document
        
        # Export to markdown
        markdown = doc.export_to_markdown()
        
        # Extract page mapping from document structure
        page_mapping = self._extract_page_mapping(doc, markdown)
        
        # Get total pages
        total_pages = self._get_total_pages(doc)
        
        print(f"Conversion complete: {len(markdown)} chars, {total_pages} pages")
        
        return {
            "markdown": markdown,
            "page_mapping": page_mapping,
            "total_pages": total_pages,
            "document": doc
        }
    
    def _extract_page_mapping(self, doc, markdown: str) -> Dict[int, int]:
        """
        Map markdown line numbers to PDF page numbers using Docling's structure
        
        Returns:
            dict mapping line_number -> page_number
        """
        page_mapping = {}
        lines = markdown.split('\n')
        
        print(f"Building page mapping for {len(lines)} lines...")
        
        try:
            # Method 1: Export each page separately and find in markdown
            if hasattr(doc, 'pages') and len(doc.pages) > 0:
                print(f"   Using page-by-page export method ({len(doc.pages)} pages)")
                
                current_line = 0
                for page_idx, page in enumerate(doc.pages, start=1):
                    # Export this page to markdown
                    try:
                        if hasattr(page, 'export_to_markdown'):
                            page_md = page.export_to_markdown()
                        elif hasattr(page, 'text'):
                            page_md = page.text
                        else:
                            continue
                        
                        # Find first few lines of this page in the full markdown
                        page_lines = page_md.split('\n')
                        first_line = next((l.strip() for l in page_lines if l.strip()), None)
                        
                        if first_line:
                            # Find where this page starts in the markdown
                            for line_num in range(current_line, len(lines)):
                                if first_line[:30] in lines[line_num] or lines[line_num][:30] in first_line:
                                    # Mark this and next ~20 lines as this page
                                    for offset in range(min(30, len(lines) - line_num)):
                                        page_mapping[line_num + offset] = page_idx
                                    current_line = line_num + 30
                                    break
                    except Exception as e:
                        print(f"   Warning: Could not process page {page_idx}: {e}")
                        continue
                
                print(f"   Mapped {len(page_mapping)} lines using page export")
            
            # Method 2: Estimate based on line distribution
            if len(page_mapping) < len(lines) * 0.1:  # Less than 10% mapped
                print(f"   Falling back to estimation method")
                total_pages = self._get_total_pages(doc)
                lines_per_page = len(lines) // total_pages if total_pages > 0 else len(lines)
                
                for line_num in range(len(lines)):
                    estimated_page = min(total_pages, (line_num // lines_per_page) + 1)
                    page_mapping[line_num] = estimated_page
                
                print(f"   Estimated {len(page_mapping)} lines ({lines_per_page} lines/page)")
        
        except Exception as e:
            print(f"   Error in page mapping: {e}")
            # Ultimate fallback: distribute evenly
            total_pages = self._get_total_pages(doc)
            lines_per_page = len(lines) // total_pages if total_pages > 0 else len(lines)
            for line_num in range(len(lines)):
                page_mapping[line_num] = min(total_pages, (line_num // lines_per_page) + 1)
        
        # Fill in any remaining gaps
        page_mapping = self._fill_page_gaps(page_mapping, len(lines))
        
        # Verify distribution
        page_counts = {}
        for page in page_mapping.values():
            page_counts[page] = page_counts.get(page, 0) + 1
        print(f"   Page distribution: {len(page_counts)} pages, avg {len(lines)//len(page_counts)} lines/page")
        
        return page_mapping
    
    def _get_page_text(self, page) -> str:
        """Extract text from a page object"""
        try:
            if hasattr(page, 'text'):
                return page.text
            elif hasattr(page, 'export_to_markdown'):
                return page.export_to_markdown()
            return ""
        except:
            return ""
    
    def _fill_page_gaps(self, page_mapping: Dict[int, int], total_lines: int) -> Dict[int, int]:
        """
        Fill gaps in page mapping using interpolation
        Ensures every line has a page number
        """
        if not page_mapping:
            # If no mapping, assume single page
            return {i: 1 for i in range(total_lines)}
        
        filled_mapping = {}
        sorted_lines = sorted(page_mapping.keys())
        
        for line_num in range(total_lines):
            if line_num in page_mapping:
                filled_mapping[line_num] = page_mapping[line_num]
            else:
                # Find nearest known page
                if line_num < sorted_lines[0]:
                    filled_mapping[line_num] = page_mapping[sorted_lines[0]]
                else:
                    # Find previous known page
                    prev_page = 1
                    for known_line in sorted_lines:
                        if known_line <= line_num:
                            prev_page = page_mapping[known_line]
                        else:
                            break
                    filled_mapping[line_num] = prev_page
        
        return filled_mapping
    
    def _get_total_pages(self, doc) -> int:
        """Get total number of pages from document"""
        try:
            if hasattr(doc, 'pages'):
                return len(doc.pages)
            elif hasattr(doc, 'num_pages'):
                return doc.num_pages
            return 1
        except:
            return 1
    
    def search_in_markdown(self, markdown: str, page_mapping: Dict[int, int], 
                          param_name: str) -> List[Dict[str, Any]]:
        """
        Search for parameter in markdown with page tracking
        
        Returns:
            list of matches with line_number, page_number, text, value, unit
        """
        results = []
        lines = markdown.split('\n')
        
        # Search for parameter (case-insensitive)
        for line_num, line in enumerate(lines):
            if param_name.lower() in line.lower():
                # Extract value from line
                value_info = self._extract_value_from_line(line)
                
                if value_info:
                    page_num = page_mapping.get(line_num, 1)
                    
                    results.append({
                        "line_number": line_num,
                        "page_number": page_num,
                        "line_text": line.strip(),
                        "value": value_info["value"],
                        "unit": value_info["unit"],
                        "context": self._get_context(lines, line_num)
                    })
        
        return results
    
    def _extract_value_from_line(self, line: str) -> Dict[str, str]:
        """Extract value and unit from a markdown line"""
        # Patterns for value extraction
        patterns = [
            # Table format: | param | value | unit |
            r'\|\s*([+-]?\d+\.?\d*\s*(?:to|-|–)\s*[+-]?\d+\.?\d*)\s*\|\s*([A-Za-z°%/]+)?\s*\|',
            r'\|\s*([+-]?\d+\.?\d*)\s*\|\s*([A-Za-z°%/]+)?\s*\|',
            # Colon/equals format: param: value unit
            r':\s*([+-]?\d+\.?\d*\s*(?:to|-|–)\s*[+-]?\d+\.?\d*)\s*([A-Za-z°%/]+)?',
            r':\s*([+-]?\d+\.?\d*)\s*([A-Za-z°%/]+)?',
            # Range format: 1.5V to 6.0V
            r'([+-]?\d+\.?\d*)\s*([A-Za-z]+)\s+to\s+([+-]?\d+\.?\d*)\s*([A-Za-z]+)?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                if len(match.groups()) >= 2:
                    value = match.group(1).strip()
                    unit = match.group(2).strip() if match.group(2) else ""
                    return {"value": value, "unit": unit}
        
        return None
    
    def _get_context(self, lines: List[str], line_num: int, context_size: int = 2) -> str:
        """Get surrounding context for a line"""
        start = max(0, line_num - context_size)
        end = min(len(lines), line_num + context_size + 1)
        return '\n'.join(lines[start:end])
