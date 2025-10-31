# Requirements Document: Engineering Parameter Extraction Tool

## Project Overview
A desktop/web application that automates the extraction of engineering parameters from component datasheets (PDF files) and provides an interactive interface for verification and correction of extracted data.

## 1. Technology Stack

### Frontend
- **Framework Options**: React.js, Vue.js, or Angular (React.js recommended for component-based architecture)
- **UI Library**: Material-UI, Ant Design, or Tailwind CSS for responsive design
- **PDF Viewer**: react-pdf, PDF.js, or vue-pdf for PDF rendering and interaction
- **Split View**: react-split-pane or similar library for resizable split-screen layout

### Backend
- **Framework**: Python with Flask or FastAPI for REST API
- **PDF Processing**: PyPDF2, pdfplumber, or PyMuPDF (fitz) for PDF text extraction
- **OCR (if needed)**: Tesseract OCR via pytesseract for scanned PDFs
- **NLP/Pattern Matching**: Regular expressions, fuzzy string matching (fuzzywuzzy), or spaCy for intelligent parameter extraction

### Data Handling
- **Input Parsing**: pandas for CSV/Excel, json module for JSON
- **Output Format**: JSON with proper schema validation

## 2. Functional Requirements

### 2.1 Input File Management

#### 2.1.1 File Format Support
- **Supported Formats**: CSV (.csv), Excel (.xlsx, .xls), JSON (.json), and optionally XML (.xml)
- **File Upload**: Drag-and-drop or file browser interface
- **File Validation**: 
  - Check file format integrity
  - Validate file size (max 10MB recommended)
  - Display clear error messages for unsupported formats

#### 2.1.2 Input File Structure
- **Expected Content**: List of engineering parameter names (one per line/row)
- **Examples of Parameters**:
  - Maximum Current (A)
  - Maximum Voltage (V)
  - Maximum Power (W)
  - Operating Temperature Range (°C)
  - Input Voltage Range (V)
  - Output Current (A)
  - Efficiency (%)
  - Frequency Range (Hz/kHz/MHz)
  - Dimensions (mm)
  - Weight (g/kg)

#### 2.1.3 Parameter Format Requirements
- Support parameters with or without units
- Handle variations in parameter naming (e.g., "Max Voltage" vs "Maximum Voltage" vs "Voltage Max")
- Case-insensitive matching

### 2.2 PDF Datasheet Upload

#### 2.2.1 Upload Mechanism
- **File Upload Interface**: Separate upload area for PDF file
- **File Validation**:
  - Accept only PDF files (.pdf)
  - Maximum file size: 50MB
  - Display file name and size after upload
- **Multiple PDF Support**: (Future enhancement) Allow multiple datasheets for comparison

#### 2.2.2 PDF Processing
- Extract text content from all pages
- Handle both text-based and scanned (image-based) PDFs
- Preserve page numbers for reference
- Extract tables and structured data where applicable

### 2.3 Parameter Extraction Engine

#### 2.3.1 Search Methodology
- **Exact Match**: Search for exact parameter names in PDF text
- **Fuzzy Matching**: Use fuzzy string matching (80%+ similarity threshold)
- **Context-Aware Search**: 
  - Look for parameter names followed by ":", "=", or whitespace and numeric values
  - Detect units in parentheses or adjacent to values (V, A, W, °C, etc.)
- **Pattern Recognition**:
  - Identify tables containing parameter-value pairs
  - Extract data from specification tables
  - Handle multi-line parameter descriptions

#### 2.3.2 Value Extraction Logic
- Extract numeric values with units
- Handle ranges (e.g., "10-20V", "15V to 25V")
- Extract typical, minimum, and maximum values where specified
- Preserve original formatting and units from PDF

#### 2.3.3 Confidence Scoring
- Assign confidence score (0-100%) to each extraction
- Flag low-confidence extractions (< 70%) for manual review
- Store source page number and text snippet for verification

### 2.4 User Interface Layout

#### 2.4.1 Split-Screen Design
- **Vertical Split**: Divide screen into two equal parts (50-50 default)
- **Resizable Panels**: Allow users to adjust the split ratio (30-70 to 70-30 range)
- **Minimum Width**: Each panel should have minimum width of 400px
- **Responsive Design**: Adapt to different screen sizes (desktop, tablet)

#### 2.4.2 Left Panel - Parameter List & Editor

##### Layout Structure
```
┌─────────────────────────────────────┐
│  Parameter Extraction Results       │
│  ─────────────────────────────────  │
│  Search: [___________________] 🔍   │
│  ─────────────────────────────────  │
│  ┌─────────────────────────────┐   │
│  │ Maximum Current              │   │
│  │ [15A____________] ✓ Page 3   │   │
│  ├─────────────────────────────┤   │
│  │ Maximum Voltage              │   │
│  │ [240V___________] ✓ Page 3   │   │
│  ├─────────────────────────────┤   │
│  │ Operating Temperature        │   │
│  │ [NF_____________] ⚠️ Not Found│   │
│  └─────────────────────────────┘   │
│                                     │
│  [Save to JSON]  [Export CSV]      │
└─────────────────────────────────────┘
```

##### Features
- **Parameter List**: 
  - Display all parameters from input file
  - Scrollable list with fixed header
  - Numbered list for easy reference
  
- **Editable Text Boxes**:
  - One text box per parameter
  - Pre-filled with extracted value or "NF" if not found
  - Clear visual distinction between found and not-found parameters
  - Input validation (ensure proper formatting)
  - Auto-save on blur (optional)

- **Status Indicators**:
  - ✓ Green checkmark: Successfully extracted
  - ⚠️ Yellow warning: Low confidence extraction
  - ❌ Red cross: Not found (NF)
  - Page number reference next to each parameter

- **Search/Filter**: 
  - Search box to filter parameters by name
  - Filter by status (All, Found, Not Found, Low Confidence)

- **Bulk Actions**:
  - Select multiple parameters for batch operations
  - Mark as reviewed
  - Clear all "NF" entries

#### 2.4.3 Right Panel - PDF Viewer

##### Features
- **PDF Rendering**:
  - High-quality PDF rendering
  - Zoom controls (25%, 50%, 75%, 100%, 125%, 150%, 200%)
  - Fit to width/height options
  - Page navigation (Previous/Next buttons, page number input)
  
- **Navigation Bar**:
  ```
  [◀️ Prev] Page [3] of [45] [Next ▶️]  [🔍-] [100%] [🔍+]
  ```

- **Text Selection**: Allow users to select and copy text from PDF

- **Search Functionality**: Built-in PDF search to find text manually

### 2.5 Interactive Highlighting & Navigation

#### 2.5.1 Parameter Selection Behavior
**When user clicks/focuses on a parameter text box in the left panel:**

1. **Automatic Page Navigation**:
   - PDF viewer automatically jumps to the page where parameter was found
   - Smooth scrolling animation to page (0.3s transition)
   - If parameter not found (NF), stay on current page

2. **Text Highlighting**:
   - Highlight the exact text/value in the PDF with yellow background
   - Highlight should be prominent but not obscure text
   - Multiple occurrences: highlight all instances, scroll to first
   - Highlight remains visible until another parameter is selected

3. **Context Window**:
   - Display surrounding text (±2 lines) to provide context
   - Optional popup/tooltip showing extracted context

4. **Visual Feedback**:
   - Highlight border on right panel to indicate active state
   - Animate highlight appearance (fade-in effect)

#### 2.5.2 Synchronization
- Real-time sync between left and right panels
- Maintain scroll position when switching between parameters
- Remember last viewed page per parameter

### 2.6 Manual Verification & Correction

#### 2.6.1 User Workflow
1. **Review Process**:
   - User selects parameter from list
   - System displays PDF at relevant location with highlighting
   - User verifies extracted value against PDF content
   - User corrects value in text box if needed

2. **Correction Interface**:
   - Click text box to edit
   - Type or paste correct value
   - Auto-format input (e.g., add units if missing)
   - Mark parameter as "Reviewed" after correction

3. **Validation**:
   - Check for proper numeric format
   - Validate units consistency
   - Warn if value significantly differs from extracted value
   - Option to add notes/comments per parameter

#### 2.6.2 Progress Tracking
- Progress bar showing percentage of parameters reviewed
- Counter: "15 of 47 parameters verified"
- Color-coded status: 
  - Green: Verified correct
  - Yellow: Modified by user
  - Red: Still marked as "NF"
  - Gray: Not yet reviewed

### 2.7 Data Export & Save Functionality

#### 2.7.1 Save Button
- **Location**: Bottom of left panel, prominently displayed
- **Label**: "Save to JSON" or "Export Results"
- **State Management**:
  - Enabled only when at least one parameter has data
  - Show unsaved changes indicator
  - Confirm before overwriting existing file

#### 2.7.2 Output JSON Format
```json
{
  "metadata": {
    "extraction_date": "2025-10-29T10:30:00Z",
    "source_pdf": "component_datasheet.pdf",
    "input_file": "parameters_list.csv",
    "total_parameters": 47,
    "extracted_count": 42,
    "not_found_count": 5,
    "manually_edited_count": 3
  },
  "parameters": [
    {
      "name": "Maximum Current",
      "value": "15A",
      "unit": "A",
      "source_page": 3,
      "extraction_method": "automatic",
      "confidence": 95,
      "manually_edited": false,
      "source_text": "Maximum output current: 15A",
      "notes": ""
    },
    {
      "name": "Operating Temperature Range",
      "value": "-40 to 85",
      "unit": "°C",
      "source_page": 5,
      "extraction_method": "manual",
      "confidence": 100,
      "manually_edited": true,
      "source_text": "",
      "notes": "Corrected from extracted value"
    },
    {
      "name": "Input Capacitance",
      "value": "NF",
      "unit": "",
      "source_page": null,
      "extraction_method": "not_found",
      "confidence": 0,
      "manually_edited": false,
      "source_text": "",
      "notes": "Not found in datasheet"
    }
  ]
}
```

#### 2.7.3 Additional Export Options
- **CSV Export**: Flat format with parameter, value, unit, page number
- **Excel Export**: Formatted spreadsheet with multiple sheets (summary, detailed)
- **PDF Report**: Generate verification report with extracted vs. corrected values

#### 2.7.4 Auto-Save Feature
- Optional auto-save every 5 minutes to prevent data loss
- Save draft to browser localStorage/sessionStorage
- Recover unsaved changes on application restart

### 2.8 Error Handling & Edge Cases

#### 2.8.1 File Upload Errors
- Invalid file format: "Unsupported file format. Please upload CSV, Excel, or JSON."
- File too large: "File size exceeds 50MB limit."
- Corrupted file: "Unable to read file. File may be corrupted."
- Empty file: "Input file is empty. Please provide a valid parameter list."

#### 2.8.2 PDF Processing Errors
- Scanned PDF without OCR: "PDF appears to be scanned. Applying OCR... (this may take a moment)"
- Password-protected PDF: "PDF is password-protected. Please provide password or upload unprotected version."
- Corrupted PDF: "Unable to open PDF file. File may be corrupted."
- No text content: "No text found in PDF. File may be image-only."

#### 2.8.3 Extraction Issues
- Parameter variations: Handle "Max Current" vs "Maximum Current" vs "I_max"
- Multiple matches: If parameter found multiple times, show first match or all matches
- Ambiguous values: Flag for manual review with warning
- Table extraction failures: Provide manual table selection tool

## 3. Non-Functional Requirements

### 3.1 Performance
- PDF upload and processing: < 10 seconds for typical 50-page document
- Parameter extraction: < 30 seconds for 50 parameters
- UI responsiveness: < 100ms for parameter selection and highlighting
- Smooth PDF rendering: 60 FPS scrolling

### 3.2 Usability
- Intuitive interface requiring minimal training
- Keyboard shortcuts for common actions (arrow keys to navigate parameters, Enter to edit)
- Undo/Redo functionality
- Tooltips and help text for guidance

### 3.3 Compatibility
- **Browser Support**: Chrome 90+, Firefox 88+, Safari 14+, Edge 90+
- **Operating Systems**: Windows 10+, macOS 10.15+, Linux (Ubuntu 20.04+)
- **Screen Resolution**: Minimum 1366x768, optimized for 1920x1080

### 3.4 Security
- File upload size limits to prevent DoS
- Input sanitization to prevent XSS attacks
- No storage of sensitive datasheet content on server (process in-memory)
- Optional: User authentication for multi-user scenarios

### 3.5 Scalability
- Handle input files with up to 200 parameters
- Support PDFs up to 200 pages
- Efficient memory management for large files

## 4. Optional/Future Enhancements

### 4.1 Advanced Features
- **Batch Processing**: Process multiple PDFs against same parameter list
- **Template Management**: Save and reuse parameter lists for different component types
- **AI-Powered Extraction**: Use ML models (e.g., BERT, GPT) for intelligent extraction
- **Comparison Mode**: Compare parameters across multiple datasheets
- **Version Control**: Track changes to extracted data over time
- **Collaboration**: Multiple users can review and verify parameters

### 4.2 Quality Improvements
- **Machine Learning**: Train on user corrections to improve extraction accuracy
- **Smart Suggestions**: Suggest likely values based on component type and common patterns
- **Validation Rules**: Define acceptable ranges for parameters (e.g., voltage must be positive)
- **Data Normalization**: Automatically convert units (mA to A, kW to W)

### 4.3 Integration
- **API Access**: RESTful API for integration with other tools
- **Database Storage**: Store extracted data in database for reporting
- **PLM/ERP Integration**: Export to Product Lifecycle Management systems
- **Cloud Storage**: Save to Google Drive, Dropbox, OneDrive

## 5. Development Phases

### Phase 1: MVP (Minimum Viable Product)
- Basic file upload (CSV, JSON)
- PDF upload and text extraction
- Simple parameter search (exact match)
- Split-screen UI with manual editing
- JSON export

### Phase 2: Enhanced Extraction
- Excel file support
- Fuzzy matching and pattern recognition
- Table extraction
- Confidence scoring
- Improved highlighting

### Phase 3: User Experience
- Advanced UI features (search, filters, progress tracking)
- Keyboard shortcuts
- Auto-save
- Error handling improvements
- Multiple export formats

### Phase 4: Intelligence & Scale
- OCR for scanned PDFs
- ML-powered extraction
- Batch processing
- Template management
- Performance optimization

## 6. Success Criteria
- **Extraction Accuracy**: > 85% automatic extraction accuracy
- **Time Savings**: 70% reduction in manual datasheet review time
- **User Satisfaction**: Average rating > 4/5 stars
- **Error Rate**: < 5% user-reported extraction errors
- **Adoption**: 90% of users complete full workflow on first attempt

---

**Document Version**: 1.0  
**Last Updated**: October 29, 2025  
**Status**: Ready for Implementation