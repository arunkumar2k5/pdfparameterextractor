"""
Simple test to show what docling conversion would produce
This uses your existing PDF processor to simulate the output
"""

from pdf_processor import PDFProcessor
from pathlib import Path
import json


def simulate_markdown_conversion(pdf_path: str):
    """Simulate what docling markdown would look like"""
    print("\n" + "="*60)
    print("SIMULATED MARKDOWN CONVERSION")
    print("="*60)
    print("(This shows what docling would produce)")
    print()
    
    processor = PDFProcessor(pdf_path)
    pages = processor.extract_pages()
    
    # Create markdown-like output
    markdown_lines = []
    markdown_lines.append("# PDF Document\n")
    
    for page in pages:
        markdown_lines.append(f"\n## Page {page['page_number']}\n")
        
        # Clean up the text
        text = page['text']
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line:
                # Try to detect tables (simple heuristic)
                if '|' in line or '\t' in line:
                    markdown_lines.append(f"| {line} |")
                else:
                    markdown_lines.append(line)
        
        markdown_lines.append("")
    
    markdown = '\n'.join(markdown_lines)
    
    # Save
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / "simulated_markdown.md"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"✅ Simulated markdown saved to: {output_path}")
    print(f"   Length: {len(markdown)} characters")
    print(f"   Lines: {len(markdown_lines)}")
    
    # Show preview
    print(f"\n{'='*60}")
    print("PREVIEW (first 1500 chars)")
    print(f"{'='*60}")
    print(markdown[:1500])
    print("\n... (see file for full content)")
    
    return markdown


def main():
    pdf_path = "../Source/tps746-q1.pdf"
    
    if not Path(pdf_path).exists():
        print(f"❌ PDF not found: {pdf_path}")
        return
    
    print("This is a SIMULATION of what docling would produce.")
    print("The actual docling output will be much better formatted.")
    print()
    
    markdown = simulate_markdown_conversion(pdf_path)
    
    print(f"\n{'='*60}")
    print("NEXT STEPS")
    print(f"{'='*60}")
    print("1. Wait for docling installation to complete")
    print("2. Run: python test_docling_prototype.py")
    print("3. Compare the actual docling output with this simulation")
    print("4. Docling will have better table formatting and structure")


if __name__ == "__main__":
    main()
