# PDF Highlighting Feature

## Overview
The application now highlights extracted parameters directly in the PDF viewer, making it easy to verify and fine-tune parameter extraction results.

## How It Works

### 1. **Automatic Highlighting**
When a parameter is successfully extracted from the PDF:
- The backend identifies the exact location (bounding box) of the parameter name and value
- This location data is stored in the `highlights` array for each parameter

### 2. **Visual Indicators**
- **Blue highlight**: Parameter name location
- **Green highlight**: Extracted value location
- **MapPin icon**: Appears next to parameters that have highlights available

### 3. **Interactive Navigation**
- Click on any parameter in the left panel
- The PDF viewer automatically navigates to the page where that parameter was found
- Highlights appear as colored rectangles over the text

## Usage Instructions

1. **Upload your parameter JSON file** (e.g., `parameters.json`)
2. **Upload your PDF datasheet** (e.g., `tps746-q1.pdf`)
3. **Click "Extract Parameters"** button
4. **Click on any extracted parameter** in the left panel
5. **View the highlights** in the PDF on the right panel

## Fine-Tuning Parameters

Use the highlights to:
- **Verify extraction accuracy**: Check if the correct text was extracted
- **Identify extraction errors**: See what the algorithm matched
- **Manually correct values**: If the extraction is wrong, edit the value in the input field
- **Understand context**: View the surrounding text where the parameter was found

## Technical Details

### Backend (Python)
- `pdf_processor.py`: Extracts word-level bounding boxes using pdfplumber
- `parameter_extractor.py`: Matches parameters and generates highlight data
- Each highlight contains: `text`, `bbox` (x0, y0, x1, y1), and `type` (parameter/value)

### Frontend (React)
- `PDFViewer.tsx`: Renders highlights as SVG rectangles overlaid on the PDF
- Highlights scale with zoom level
- Automatically shows/hides based on selected parameter

## Color Legend
- 🔵 **Blue**: Parameter name (what you're searching for)
- 🟢 **Green**: Extracted value (what was found)

## Troubleshooting

### No highlights appearing?
- Ensure the parameter was successfully extracted (not "NF")
- Check that you're on the correct page (source_page)
- Verify the backend is returning highlight data in the API response

### Highlights in wrong position?
- The PDF may have complex layout or multiple columns
- The bounding boxes are word-level, not character-level
- Consider the PDF's coordinate system (origin at top-left)

## Next Steps

To improve highlighting accuracy:
1. Enhance word grouping for multi-word parameters
2. Add table detection for structured data
3. Implement click-to-highlight for manual selection
4. Support highlighting across multiple pages
