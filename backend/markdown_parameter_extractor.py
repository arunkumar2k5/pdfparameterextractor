"""
Enhanced Parameter Extractor using Markdown
Searches in markdown first, falls back to PDF if needed
"""

import re
from typing import List, Dict, Any, Optional
from fuzzywuzzy import fuzz


class MarkdownParameterExtractor:
    """Extract parameters from markdown with page tracking"""
    
    def __init__(self, markdown: str, page_mapping: Dict[int, int], pdf_pages: List[Dict[str, Any]]):
        self.markdown = markdown
        self.page_mapping = page_mapping
        self.pdf_pages = pdf_pages
        self.lines = markdown.split('\n')
        self.fuzzy_threshold = 80
    
    def extract_parameter(self, param_name: str) -> Dict[str, Any]:
        """
        Extract a single parameter from markdown
        Falls back to PDF if not found in markdown
        """
        
        print(f"Extracting parameter: {param_name}")
        
        # Try markdown search first (better accuracy)
        result = self._search_in_markdown(param_name)
        if result:
            print(f"   Found: {result['value']} {result['unit']} on page {result['source_page']}, line {result['markdown_line']}")
            return result
        
        # Fallback: not found
        return {
            "name": param_name,
            "value": "NF",
            "unit": "",
            "source_page": None,
            "markdown_line": None,
            "extraction_method": "not_found",
            "confidence": 0,
            "manually_edited": False,
            "source_text": "",
            "markdown_context": "",
            "notes": "Not found in datasheet",
            "highlights": []
        }
    
    def _search_in_markdown(self, param_name: str) -> Optional[Dict[str, Any]]:
        """Search for parameter in markdown"""
        
        # Try exact match first
        exact_matches = self._exact_match(param_name)
        if exact_matches:
            return self._create_result(param_name, exact_matches[0], "exact_match", 95)
        
        # Try fuzzy match
        fuzzy_matches = self._fuzzy_match(param_name)
        if fuzzy_matches:
            return self._create_result(param_name, fuzzy_matches[0], "fuzzy_match", fuzzy_matches[0]["confidence"])
        
        # Try keyword match
        keyword_matches = self._keyword_match(param_name)
        if keyword_matches:
            return self._create_result(param_name, keyword_matches[0], "keyword_match", 75)
        
        return None
    
    def _exact_match(self, param_name: str) -> List[Dict[str, Any]]:
        """Find exact matches for parameter name"""
        matches = []
        
        for line_num, line in enumerate(self.lines):
            if param_name.lower() in line.lower():
                value_info = self._extract_value_from_line(line)
                if value_info:
                    matches.append({
                        "line_number": line_num,
                        "line_text": line.strip(),
                        "value": value_info["value"],
                        "unit": value_info["unit"],
                        "page_number": self.page_mapping.get(line_num, 1)
                    })
        
        return matches
    
    def _fuzzy_match(self, param_name: str) -> List[Dict[str, Any]]:
        """Find fuzzy matches for parameter name"""
        matches = []
        
        for line_num, line in enumerate(self.lines):
            # Skip very short lines
            if len(line.strip()) < 5:
                continue
            
            # Calculate fuzzy score
            score = fuzz.partial_ratio(param_name.lower(), line.lower())
            
            if score >= self.fuzzy_threshold:
                value_info = self._extract_value_from_line(line)
                if value_info:
                    matches.append({
                        "line_number": line_num,
                        "line_text": line.strip(),
                        "value": value_info["value"],
                        "unit": value_info["unit"],
                        "page_number": self.page_mapping.get(line_num, 1),
                        "confidence": min(score, 90)
                    })
        
        # Sort by confidence
        matches.sort(key=lambda x: x.get("confidence", 0), reverse=True)
        return matches
    
    def _keyword_match(self, param_name: str) -> List[Dict[str, Any]]:
        """Find matches based on keywords"""
        keywords = self._extract_keywords(param_name)
        matches = []
        
        for line_num, line in enumerate(self.lines):
            line_lower = line.lower()
            
            # Check if line contains any keywords
            if any(kw.lower() in line_lower for kw in keywords):
                value_info = self._extract_value_from_line(line)
                if value_info:
                    matches.append({
                        "line_number": line_num,
                        "line_text": line.strip(),
                        "value": value_info["value"],
                        "unit": value_info["unit"],
                        "page_number": self.page_mapping.get(line_num, 1)
                    })
        
        return matches
    
    def _extract_value_from_line(self, line: str) -> Optional[Dict[str, str]]:
        """Extract value and unit from a markdown line"""
        # Patterns for value extraction (optimized for markdown tables)
        patterns = [
            # Table format: | param | min | typ | max | unit |
            r'\|\s*([+-]?\d+\.?\d*)\s*\|\s*\|\s*([+-]?\d+\.?\d*)\s*\|\s*([A-Za-z°%/]+)?\s*\|',
            # Table format: | param | value | unit |
            r'\|\s*([+-]?\d+\.?\d*)\s*\|\s*([A-Za-z°%/]+)?\s*\|',
            # Range in table: | param | 1.5 to 6.0 | V |
            r'\|\s*([+-]?\d+\.?\d*)\s+to\s+([+-]?\d+\.?\d*)\s*\|\s*([A-Za-z°%/]+)?\s*\|',
            # Colon format: param: 1.5V to 6.0V
            r':\s*([+-]?\d+\.?\d*)\s*([A-Za-z]+)\s+to\s+([+-]?\d+\.?\d*)\s*([A-Za-z]+)?',
            # Simple colon: param: value unit
            r':\s*([+-]?\d+\.?\d*)\s*([A-Za-z°%/]+)?',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                groups = match.groups()
                if len(groups) >= 2:
                    # Handle range format
                    if 'to' in pattern:
                        value = f"{groups[0]} to {groups[1]}"
                        unit = groups[2] if len(groups) > 2 and groups[2] else ""
                    else:
                        value = groups[0].strip()
                        unit = groups[1].strip() if groups[1] else ""
                    
                    return {"value": value, "unit": unit}
        
        return None
    
    def _extract_keywords(self, param_name: str) -> List[str]:
        """Extract keywords from parameter name"""
        common_words = {'the', 'a', 'an', 'of', 'in', 'to', 'for', 'range'}
        words = re.findall(r'\w+', param_name)
        keywords = [w for w in words if w.lower() not in common_words]
        return keywords
    
    def _create_result(self, param_name: str, match: Dict[str, Any], 
                      method: str, confidence: int) -> Dict[str, Any]:
        """Create standardized result from match"""
        line_num = match["line_number"]
        page_num = match["page_number"]
        
        # Get highlights from PDF for this page
        highlights = self._get_pdf_highlights(page_num, match["value"])
        
        # Get context
        context = self._get_context(line_num)
        
        return {
            "name": param_name,
            "value": match["value"],
            "unit": match["unit"],
            "source_page": page_num,
            "markdown_line": line_num,
            "extraction_method": method,
            "confidence": confidence,
            "manually_edited": False,
            "source_text": match["line_text"],
            "markdown_context": context,
            "notes": "",
            "highlights": highlights
        }
    
    def _get_pdf_highlights(self, page_num: int, value_text: str) -> List[Dict[str, Any]]:
        """Get PDF highlights for a specific page and value"""
        highlights = []
        
        # Find the page in pdf_pages
        for page in self.pdf_pages:
            if page["page_number"] == page_num:
                blocks = page.get("blocks", [])
                
                # Search for value in blocks
                for block in blocks:
                    block_text = block.get("text", "")
                    if value_text in block_text:
                        highlights.append({
                            "text": block_text,
                            "bbox": block.get("bbox", []),
                            "type": "value"
                        })
                break
        
        return highlights
    
    def _get_context(self, line_num: int, context_size: int = 2) -> str:
        """Get surrounding context for a line"""
        start = max(0, line_num - context_size)
        end = min(len(self.lines), line_num + context_size + 1)
        return '\n'.join(self.lines[start:end])
