"""
Test Full Integration - Verify parameter extraction with page numbers
"""

from markdown_converter import MarkdownConverter
from markdown_parameter_extractor import MarkdownParameterExtractor
from pdf_processor import PDFProcessor
from pathlib import Path
import json


def test_integration():
    """Test the full integration"""
    
    pdf_path = "../Source/tps746-q1.pdf"
    
    if not Path(pdf_path).exists():
        print(f"ERROR: PDF not found: {pdf_path}")
        return
    
    print("="*60)
    print("Testing Full Integration")
    print("="*60)
    
    # Step 1: Convert PDF to markdown
    print("\nStep 1: Converting PDF to markdown...")
    md_converter = MarkdownConverter()
    md_result = md_converter.convert_pdf_to_markdown(pdf_path)
    
    # Step 2: Process PDF for highlights
    print("\nStep 2: Processing PDF for highlights...")
    pdf_processor = PDFProcessor(pdf_path)
    pdf_pages = pdf_processor.extract_pages()
    
    # Step 3: Create extractor
    print("\nStep 3: Creating parameter extractor...")
    extractor = MarkdownParameterExtractor(
        md_result["markdown"],
        md_result["page_mapping"],
        pdf_pages
    )
    
    # Step 4: Test parameter extraction
    print("\nStep 4: Extracting parameters...")
    print("="*60)
    
    test_params = [
        "Input voltage Range",
        "Output voltage Range",
        "Output current"
    ]
    
    results = []
    for param in test_params:
        result = extractor.extract_parameter(param)
        results.append(result)
        
        print(f"\n{'='*60}")
        print(f"Parameter: {param}")
        print(f"{'='*60}")
        print(f"  Value: {result['value']} {result['unit']}")
        print(f"  Source Page: {result['source_page']}")
        print(f"  Markdown Line: {result['markdown_line']}")
        print(f"  Method: {result['extraction_method']}")
        print(f"  Confidence: {result['confidence']}%")
        print(f"  Source Text: {result['source_text'][:100]}...")
        print(f"  Highlights: {len(result['highlights'])} found")
    
    # Save results
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    
    results_file = output_dir / "integration_test_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\nResults saved to: {results_file}")
    
    # Summary
    print(f"\n{'='*60}")
    print("Summary")
    print(f"{'='*60}")
    
    found_count = sum(1 for r in results if r['value'] != 'NF')
    print(f"Parameters found: {found_count}/{len(test_params)}")
    
    for result in results:
        if result['value'] != 'NF':
            status = "[OK]"
            page_info = f"Page {result['source_page']}, Line {result['markdown_line']}"
        else:
            status = "[FAIL]"
            page_info = "Not found"
        
        print(f"{status} {result['name']}: {page_info}")
    
    print(f"\n{'='*60}")
    print("Next Steps")
    print(f"{'='*60}")
    print("1. Check the results JSON file")
    print("2. Verify page numbers are correct")
    print("3. Test in the web UI")
    print("4. Click on parameters and verify both PDF and markdown views update")


if __name__ == "__main__":
    test_integration()
