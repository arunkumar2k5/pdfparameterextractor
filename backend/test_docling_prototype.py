"""
Docling Prototype - Test PDF to Markdown Conversion
====================================================

This prototype demonstrates:
1. Converting PDF to Markdown using Docling
2. Extracting page references
3. Searching for parameters in markdown
4. Comparing with current PDF extraction

Usage:
    python test_docling_prototype.py
"""

from pathlib import Path
from docling.document_converter import DocumentConverter
import re
from typing import Dict, List, Any
import json


class DoclingPrototype:
    def __init__(self):
        self.converter = DocumentConverter()
    
    def convert_pdf_to_markdown(self, pdf_path: str) -> Dict[str, Any]:
        """Convert PDF to markdown with page tracking"""
        print(f"\n{'='*60}")
        print(f"Converting PDF to Markdown")
        print(f"{'='*60}")
        print(f"Input: {pdf_path}\n")
        
        # Convert PDF
        print("⏳ Processing PDF with Docling...")
        result = self.converter.convert(pdf_path)
        
        # Export to markdown
        markdown = result.document.export_to_markdown()
        
        # Get document structure for page mapping
        doc = result.document
        
        print(f"✅ Conversion complete!")
        print(f"   Markdown length: {len(markdown)} characters")
        print(f"   Lines: {len(markdown.split(chr(10)))}")
        
        return {
            "markdown": markdown,
            "document": doc,
            "result": result
        }
    
    def extract_page_mapping(self, markdown: str) -> Dict[int, int]:
        """Extract page references from markdown"""
        page_mapping = {}
        lines = markdown.split('\n')
        
        current_page = 1
        for line_num, line in enumerate(lines):
            # Look for page markers (Docling often includes these)
            if '<!-- Page' in line or 'Page ' in line:
                match = re.search(r'Page\s+(\d+)', line)
                if match:
                    current_page = int(match.group(1))
            
            page_mapping[line_num] = current_page
        
        return page_mapping
    
    def search_parameter_in_markdown(self, markdown: str, param_name: str) -> List[Dict[str, Any]]:
        """Search for parameter in markdown text"""
        print(f"\n{'='*60}")
        print(f"Searching for: {param_name}")
        print(f"{'='*60}")
        
        results = []
        lines = markdown.split('\n')
        
        # Search for parameter name (case-insensitive)
        for line_num, line in enumerate(lines):
            if param_name.lower() in line.lower():
                # Try to extract value from the line
                value_info = self._extract_value_from_line(line)
                
                if value_info:
                    results.append({
                        "line_number": line_num,
                        "line_text": line.strip(),
                        "value": value_info["value"],
                        "unit": value_info["unit"],
                        "context": self._get_context(lines, line_num)
                    })
        
        return results
    
    def _extract_value_from_line(self, line: str) -> Dict[str, str]:
        """Extract value and unit from a line"""
        # Pattern for value extraction
        patterns = [
            r'[:=]\s*([+-]?\d+\.?\d*\s*(?:to|-|–)\s*[+-]?\d+\.?\d*)\s*([A-Za-z°%/]+)?',
            r'[:=]\s*([+-]?\d+\.?\d*)\s*([A-Za-z°%/]+)?',
            r'\|\s*([+-]?\d+\.?\d*\s*(?:to|-|–)\s*[+-]?\d+\.?\d*)\s*([A-Za-z°%/]+)?\s*\|',
            r'\|\s*([+-]?\d+\.?\d*)\s*([A-Za-z°%/]+)?\s*\|'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                value = match.group(1).strip()
                unit = match.group(2).strip() if match.group(2) else ""
                return {"value": value, "unit": unit}
        
        return None
    
    def _get_context(self, lines: List[str], line_num: int, context_size: int = 2) -> str:
        """Get surrounding context for a line"""
        start = max(0, line_num - context_size)
        end = min(len(lines), line_num + context_size + 1)
        return '\n'.join(lines[start:end])
    
    def save_markdown(self, markdown: str, output_path: str):
        """Save markdown to file"""
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(markdown)
        print(f"\n✅ Markdown saved to: {output_path}")
    
    def display_results(self, results: List[Dict[str, Any]]):
        """Display search results"""
        if not results:
            print("❌ No results found")
            return
        
        print(f"\n✅ Found {len(results)} match(es):\n")
        
        for i, result in enumerate(results, 1):
            print(f"--- Match {i} ---")
            print(f"Line {result['line_number']}: {result['line_text']}")
            print(f"Value: {result['value']} {result['unit']}")
            print(f"\nContext:")
            print(result['context'])
            print()


def main():
    """Run the prototype test"""
    print("\n" + "="*60)
    print("DOCLING PROTOTYPE TEST")
    print("="*60)
    
    # Initialize prototype
    prototype = DoclingPrototype()
    
    # PDF path - use the uploaded PDF
    pdf_path = "../Source/tps746-q1.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ Error: PDF not found at {pdf_path}")
        print("Please update the path to your PDF file")
        return
    
    try:
        # Step 1: Convert PDF to Markdown
        conversion_result = prototype.convert_pdf_to_markdown(pdf_path)
        markdown = conversion_result["markdown"]
        
        # Step 2: Save markdown for inspection
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        output_path = output_dir / "tps746-q1.md"
        prototype.save_markdown(markdown, str(output_path))
        
        # Step 3: Display first 2000 characters
        print(f"\n{'='*60}")
        print("MARKDOWN PREVIEW (first 2000 chars)")
        print(f"{'='*60}")
        print(markdown[:2000])
        print("\n... (truncated)")
        
        # Step 4: Test parameter search
        test_parameters = [
            "Input voltage Range",
            "Output voltage Range",
            "Output current"
        ]
        
        print(f"\n{'='*60}")
        print("PARAMETER SEARCH TEST")
        print(f"{'='*60}")
        
        all_results = {}
        for param in test_parameters:
            results = prototype.search_parameter_in_markdown(markdown, param)
            all_results[param] = results
            prototype.display_results(results)
        
        # Step 5: Save results to JSON
        results_path = output_dir / "search_results.json"
        with open(results_path, 'w', encoding='utf-8') as f:
            json.dump(all_results, f, indent=2)
        print(f"✅ Search results saved to: {results_path}")
        
        # Step 6: Summary
        print(f"\n{'='*60}")
        print("PROTOTYPE SUMMARY")
        print(f"{'='*60}")
        print(f"✅ PDF converted to Markdown successfully")
        print(f"✅ Markdown length: {len(markdown)} characters")
        print(f"✅ Total lines: {len(markdown.split(chr(10)))}")
        print(f"✅ Parameters tested: {len(test_parameters)}")
        print(f"✅ Total matches found: {sum(len(r) for r in all_results.values())}")
        print(f"\nNext steps:")
        print(f"1. Review the markdown file: {output_path}")
        print(f"2. Check search results: {results_path}")
        print(f"3. Compare with current PDF extraction")
        print(f"4. Proceed with full integration if results are good")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
