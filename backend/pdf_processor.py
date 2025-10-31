from PyPDF2 import PdfReader
import pdfplumber
from typing import List, Dict, Any


class PDFProcessor:
    """Process PDF files to extract text and metadata"""
    
    def __init__(self, pdf_path: str):
        self.pdf_path = pdf_path
        self.reader = PdfReader(pdf_path)
    
    def extract_text(self) -> str:
        """Extract all text from PDF"""
        text = ""
        for page in self.reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    def extract_pages(self) -> List[Dict[str, Any]]:
        """Extract text from each page separately with metadata"""
        pages = []
        
        # Use pdfplumber for better text extraction with positions
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text() or ""
                
                # Extract text blocks with positions for highlighting
                blocks = []
                words = page.extract_words()
                for word in words:
                    blocks.append({
                        "text": word.get("text", ""),
                        "bbox": [word.get("x0", 0), word.get("top", 0), 
                                word.get("x1", 0), word.get("bottom", 0)],
                        "size": word.get("height", 0)
                    })
                
                pages.append({
                    "page_number": page_num,
                    "text": page_text,
                    "blocks": blocks,
                    "width": page.width,
                    "height": page.height
                })
        
        return pages
    
    def extract_tables(self) -> List[Dict[str, Any]]:
        """Extract tables from PDF using pdfplumber"""
        tables = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for page_num, page in enumerate(pdf.pages, start=1):
                page_tables = page.extract_tables()
                for table in page_tables:
                    if table:
                        tables.append({
                            "page_number": page_num,
                            "data": table
                        })
        return tables
    
    def search_text(self, query: str, page_num: int = None) -> List[Dict[str, Any]]:
        """Search for text in PDF and return positions"""
        results = []
        
        with pdfplumber.open(self.pdf_path) as pdf:
            pages_to_search = [pdf.pages[page_num - 1]] if page_num else pdf.pages
            
            for page_idx, page in enumerate(pages_to_search):
                actual_page_num = page_num if page_num else page_idx + 1
                page_text = page.extract_text() or ""
                
                # Simple text search
                if query.lower() in page_text.lower():
                    results.append({
                        "page_number": actual_page_num,
                        "bbox": [0, 0, 0, 0],  # Simplified bbox
                        "text": query
                    })
        
        return results
    
    def close(self):
        """Close the PDF document"""
        # PyPDF2 doesn't require explicit closing
        pass
