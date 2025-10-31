# Docling Integration Plan

## Overview
Integrate Docling library to improve parameter extraction accuracy by converting PDFs to structured Markdown format before searching.

## Current vs Proposed Architecture

### Current Flow:
```
PDF Upload → PyPDF2/pdfplumber extraction → Search raw text → Return results
```

### Proposed Flow:
```
PDF Upload → Docling conversion to MD → Search structured MD → Return results with page refs
```

## Benefits

1. **Better Search Accuracy**
   - Structured markdown is cleaner than raw PDF text
   - Tables are properly formatted
   - Multi-column layouts are handled correctly
   - Headers and sections are preserved

2. **Improved User Experience**
   - View both PDF and markdown side-by-side
   - Easier to verify extraction context
   - Better readability for fine-tuning

3. **Page Number Preservation**
   - Docling maintains page references in markdown
   - Can still navigate to exact PDF page
   - Dual highlighting in both views

## Implementation Steps

### Phase 1: Backend Integration (1-2 hours)

#### 1.1 Add Dependencies
```bash
cd backend
pip install docling
pip freeze > requirements.txt
```

#### 1.2 Create Markdown Converter (`backend/markdown_converter.py`)
```python
from docling.document_converter import DocumentConverter
from pathlib import Path

class MarkdownConverter:
    def __init__(self):
        self.converter = DocumentConverter()
    
    def convert_pdf_to_markdown(self, pdf_path: str) -> dict:
        """Convert PDF to markdown with page references"""
        result = self.converter.convert(pdf_path)
        markdown = result.document.export_to_markdown()
        
        # Extract page mapping
        page_mapping = self._extract_page_mapping(result.document)
        
        return {
            "markdown": markdown,
            "page_mapping": page_mapping,
            "total_pages": len(page_mapping)
        }
    
    def _extract_page_mapping(self, doc):
        """Map markdown line numbers to PDF page numbers"""
        # Implementation to track which markdown lines correspond to which PDF pages
        pass
```

#### 1.3 Update PDF Upload Endpoint (`backend/main.py`)
```python
@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    # ... existing code ...
    
    # Convert to markdown
    md_converter = MarkdownConverter()
    md_result = md_converter.convert_pdf_to_markdown(str(pdf_path))
    
    # Store both PDF and markdown
    session_data["pdf_path"] = str(pdf_path)
    session_data["markdown"] = md_result["markdown"]
    session_data["page_mapping"] = md_result["page_mapping"]
    
    # Also keep existing PDF processing for highlighting
    processor = PDFProcessor(str(pdf_path))
    session_data["pdf_pages"] = processor.extract_pages()
    
    return {
        "success": True,
        "filename": file.filename,
        "pages": len(pdf_pages),
        "pdf_url": f"/api/pdf/{file.filename}",
        "markdown_url": f"/api/markdown/{file.filename}"
    }
```

#### 1.4 Create Markdown Search (`backend/markdown_searcher.py`)
```python
import re
from typing import List, Dict, Any

class MarkdownSearcher:
    def __init__(self, markdown: str, page_mapping: dict):
        self.markdown = markdown
        self.page_mapping = page_mapping
        self.lines = markdown.split('\n')
    
    def search_parameter(self, param_name: str) -> List[Dict[str, Any]]:
        """Search for parameter in markdown"""
        results = []
        
        # Search with fuzzy matching
        for line_num, line in enumerate(self.lines):
            if self._matches_parameter(param_name, line):
                value = self._extract_value(line)
                if value:
                    page_num = self._get_page_number(line_num)
                    results.append({
                        "line_number": line_num,
                        "page_number": page_num,
                        "text": line,
                        "value": value["value"],
                        "unit": value["unit"],
                        "confidence": value["confidence"]
                    })
        
        return results
    
    def _matches_parameter(self, param_name: str, line: str) -> bool:
        # Fuzzy matching logic
        pass
    
    def _extract_value(self, line: str) -> dict:
        # Value extraction from markdown line
        pass
    
    def _get_page_number(self, line_num: int) -> int:
        # Map markdown line to PDF page
        pass
```

#### 1.5 Add Markdown Endpoint
```python
@app.get("/api/markdown/{filename}")
async def get_markdown(filename: str):
    """Serve markdown content"""
    return JSONResponse(content={
        "markdown": session_data.get("markdown", ""),
        "page_mapping": session_data.get("page_mapping", {})
    })
```

### Phase 2: Frontend Integration (1-2 hours)

#### 2.1 Create Markdown Viewer Component (`frontend/src/components/MarkdownViewer.tsx`)
```typescript
import React, { useEffect, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import { Parameter } from '../types';

interface MarkdownViewerProps {
  markdownContent: string;
  selectedParameter: Parameter | null;
}

const MarkdownViewer: React.FC<MarkdownViewerProps> = ({ 
  markdownContent, 
  selectedParameter 
}) => {
  const [highlightedContent, setHighlightedContent] = useState('');

  useEffect(() => {
    if (selectedParameter && selectedParameter.markdown_line) {
      // Highlight the relevant line in markdown
      const lines = markdownContent.split('\n');
      const highlighted = lines.map((line, idx) => {
        if (idx === selectedParameter.markdown_line) {
          return `<mark class="bg-yellow-300">${line}</mark>`;
        }
        return line;
      }).join('\n');
      setHighlightedContent(highlighted);
    } else {
      setHighlightedContent(markdownContent);
    }
  }, [markdownContent, selectedParameter]);

  return (
    <div className="h-full overflow-auto p-4 bg-gray-50">
      <div className="prose max-w-none">
        <ReactMarkdown>{highlightedContent}</ReactMarkdown>
      </div>
    </div>
  );
};

export default MarkdownViewer;
```

#### 2.2 Update PDFViewer to Split View (`frontend/src/components/PDFViewer.tsx`)
```typescript
import { Panel, PanelGroup, PanelResizeHandle } from 'react-resizable-panels';
import MarkdownViewer from './MarkdownViewer';

const PDFViewer: React.FC<PDFViewerProps> = ({ 
  pdfUrl, 
  markdownContent,
  selectedParameter 
}) => {
  return (
    <PanelGroup direction="vertical">
      {/* Top Panel - PDF */}
      <Panel defaultSize={50} minSize={30}>
        <div className="h-full flex flex-col bg-gray-100">
          {/* Existing PDF viewer code */}
        </div>
      </Panel>

      {/* Resize Handle */}
      <PanelResizeHandle className="h-2 bg-gray-300 hover:bg-blue-500 transition-colors cursor-row-resize" />

      {/* Bottom Panel - Markdown */}
      <Panel defaultSize={50} minSize={30}>
        <MarkdownViewer 
          markdownContent={markdownContent}
          selectedParameter={selectedParameter}
        />
      </Panel>
    </PanelGroup>
  );
};
```

#### 2.3 Install Required Dependencies
```bash
cd frontend
npm install react-markdown remark-gfm
```

#### 2.4 Update Types (`frontend/src/types.ts`)
```typescript
export interface Parameter {
  // ... existing fields ...
  markdown_line?: number;  // Line number in markdown
  markdown_context?: string;  // Surrounding markdown context
}
```

### Phase 3: Enhanced Search Logic (30 mins)

#### 3.1 Update Parameter Extractor
```python
class EnhancedParameterExtractor:
    def __init__(self, markdown: str, page_mapping: dict, pdf_pages: List[Dict]):
        self.markdown_searcher = MarkdownSearcher(markdown, page_mapping)
        self.pdf_pages = pdf_pages  # Keep for highlighting
    
    def extract_parameter(self, param_name: str) -> Dict[str, Any]:
        # First try markdown search
        md_results = self.markdown_searcher.search_parameter(param_name)
        
        if md_results:
            best_result = md_results[0]  # Take best match
            
            # Get PDF highlights for the same page
            highlights = self._get_pdf_highlights(
                best_result["page_number"],
                best_result["value"]
            )
            
            return {
                "name": param_name,
                "value": best_result["value"],
                "unit": best_result["unit"],
                "source_page": best_result["page_number"],
                "markdown_line": best_result["line_number"],
                "markdown_context": best_result["text"],
                "confidence": best_result["confidence"],
                "highlights": highlights
            }
        
        # Fallback to original PDF search
        return self._fallback_pdf_search(param_name)
```

## Testing Plan

### Test Cases:
1. **Simple parameters**: "Input voltage", "Output current"
2. **Table parameters**: Values in specification tables
3. **Multi-column PDFs**: Technical datasheets
4. **Range values**: "10-20V", "15V to 25V"
5. **Page navigation**: Click parameter → both views update

### Success Criteria:
- ✅ Markdown conversion completes in < 5 seconds
- ✅ Search accuracy improves by 30%+
- ✅ Both PDF and markdown views sync correctly
- ✅ Page numbers are accurate
- ✅ Highlighting works in both views

## Rollout Strategy

### Option 1: Parallel Implementation (Recommended)
- Keep existing PDF search as fallback
- Use markdown search as primary
- Compare results for validation
- Gradually phase out old method

### Option 2: Full Replacement
- Replace PDF search entirely
- Faster to implement
- Higher risk if issues arise

## Estimated Timeline

- **Backend Integration**: 2 hours
- **Frontend Split View**: 1.5 hours
- **Search Enhancement**: 1 hour
- **Testing & Debugging**: 1.5 hours
- **Total**: ~6 hours

## Dependencies to Install

### Backend:
```bash
pip install docling
```

### Frontend:
```bash
npm install react-markdown remark-gfm
```

## Next Steps

1. ✅ Review this plan
2. Install docling in backend
3. Create markdown_converter.py
4. Test PDF → Markdown conversion
5. Implement markdown search
6. Update frontend with split view
7. Test end-to-end flow
8. Deploy and validate

## Potential Challenges

1. **Large PDFs**: Markdown conversion may be slow
   - Solution: Add loading indicator, cache results

2. **Page Mapping Accuracy**: Line-to-page mapping may be complex
   - Solution: Use docling's built-in page tracking

3. **Markdown Rendering**: Some PDFs may have complex formatting
   - Solution: Use remark-gfm for GitHub-flavored markdown support

4. **Memory Usage**: Storing both PDF and markdown
   - Solution: Clear cache after session, use file storage

## Conclusion

This integration is **highly feasible** and will significantly improve:
- ✅ Search accuracy
- ✅ User experience
- ✅ Parameter verification
- ✅ Fine-tuning capabilities

Ready to proceed with implementation!
