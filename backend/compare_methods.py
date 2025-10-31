"""
Comparison: Current PDF Extraction vs Docling Markdown
=======================================================

This script compares the two methods side-by-side to show
the improvement in search accuracy.
"""

from pathlib import Path
from pdf_processor import PDFProcessor
from parameter_extractor import ParameterExtractor
from test_docling_prototype import DoclingPrototype
import json


def test_current_method(pdf_path: str, parameters: list) -> dict:
    """Test current PDF extraction method"""
    print("\n" + "="*60)
    print("CURRENT METHOD (PyPDF2/pdfplumber)")
    print("="*60)
    
    processor = PDFProcessor(pdf_path)
    pdf_text = processor.extract_text()
    pdf_pages = processor.extract_pages()
    
    extractor = ParameterExtractor(pdf_text, pdf_pages)
    
    results = {}
    for param in parameters:
        print(f"\nSearching: {param}")
        result = extractor.extract_parameter(param)
        results[param] = result
        print(f"  Value: {result['value']} {result['unit']}")
        print(f"  Confidence: {result['confidence']}%")
        print(f"  Method: {result['extraction_method']}")
    
    return results


def test_docling_method(pdf_path: str, parameters: list) -> dict:
    """Test Docling markdown method"""
    print("\n" + "="*60)
    print("DOCLING METHOD (Markdown)")
    print("="*60)
    
    prototype = DoclingPrototype()
    conversion = prototype.convert_pdf_to_markdown(pdf_path)
    markdown = conversion["markdown"]
    
    results = {}
    for param in parameters:
        print(f"\nSearching: {param}")
        matches = prototype.search_parameter_in_markdown(markdown, param)
        
        if matches:
            best_match = matches[0]
            results[param] = {
                "value": best_match["value"],
                "unit": best_match["unit"],
                "line_number": best_match["line_number"],
                "line_text": best_match["line_text"],
                "found": True
            }
            print(f"  Value: {best_match['value']} {best_match['unit']}")
            print(f"  Line: {best_match['line_text'][:80]}...")
        else:
            results[param] = {"found": False}
            print(f"  Not found")
    
    return results


def compare_results(current: dict, docling: dict, parameters: list):
    """Compare and display results"""
    print("\n" + "="*60)
    print("COMPARISON RESULTS")
    print("="*60)
    
    comparison = []
    
    for param in parameters:
        curr = current[param]
        docl = docling[param]
        
        curr_found = curr['value'] != 'NF'
        docl_found = docl.get('found', False)
        
        comparison.append({
            "parameter": param,
            "current_value": curr['value'],
            "docling_value": docl.get('value', 'NF'),
            "current_found": curr_found,
            "docling_found": docl_found,
            "improvement": docl_found and not curr_found
        })
    
    # Display table
    print(f"\n{'Parameter':<30} | {'Current':<15} | {'Docling':<15} | {'Better?'}")
    print("-" * 80)
    
    for comp in comparison:
        current_val = comp['current_value'][:15] if comp['current_found'] else "❌ NF"
        docling_val = comp['docling_value'][:15] if comp['docling_found'] else "❌ NF"
        better = "✅ YES" if comp['improvement'] else ("✅ SAME" if comp['current_found'] and comp['docling_found'] else "")
        
        print(f"{comp['parameter']:<30} | {current_val:<15} | {docling_val:<15} | {better}")
    
    # Summary
    current_found = sum(1 for c in comparison if c['current_found'])
    docling_found = sum(1 for c in comparison if c['docling_found'])
    improvements = sum(1 for c in comparison if c['improvement'])
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    print(f"Total parameters: {len(parameters)}")
    print(f"Current method found: {current_found}/{len(parameters)}")
    print(f"Docling method found: {docling_found}/{len(parameters)}")
    print(f"Improvements: {improvements}")
    print(f"Accuracy improvement: {((docling_found - current_found) / len(parameters) * 100):.1f}%")
    
    return comparison


def main():
    """Run comparison test"""
    print("\n" + "="*60)
    print("METHOD COMPARISON TEST")
    print("="*60)
    
    pdf_path = "../Source/tps746-q1.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ Error: PDF not found at {pdf_path}")
        return
    
    # Parameters to test
    parameters = [
        "Input voltage Range",
        "Output voltage Range",
        "Output current"
    ]
    
    try:
        # Test both methods
        current_results = test_current_method(pdf_path, parameters)
        docling_results = test_docling_method(pdf_path, parameters)
        
        # Compare
        comparison = compare_results(current_results, docling_results, parameters)
        
        # Save comparison
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        comparison_path = output_dir / "method_comparison.json"
        with open(comparison_path, 'w', encoding='utf-8') as f:
            json.dump({
                "current_method": current_results,
                "docling_method": docling_results,
                "comparison": comparison
            }, f, indent=2)
        
        print(f"\n✅ Comparison saved to: {comparison_path}")
        
        # Recommendation
        docling_found = sum(1 for c in comparison if c['docling_found'])
        current_found = sum(1 for c in comparison if c['current_found'])
        
        print("\n" + "="*60)
        print("RECOMMENDATION")
        print("="*60)
        
        if docling_found > current_found:
            print("✅ PROCEED with Docling integration")
            print(f"   Docling found {docling_found - current_found} more parameters")
            print("   Expected improvement in production")
        elif docling_found == current_found:
            print("⚠️  SIMILAR RESULTS")
            print("   Consider other benefits (readability, table handling)")
            print("   Docling may still be worth it for complex PDFs")
        else:
            print("❌ CURRENT METHOD BETTER")
            print("   Stick with current implementation")
            print("   Or investigate why Docling performed worse")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
