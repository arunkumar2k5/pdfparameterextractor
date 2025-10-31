# Engineering Parameter Extraction Tool

A web-based application that automates the extraction of engineering parameters from component datasheets (PDF files) with an interactive interface for verification and correction.

## Features

- 📄 Upload parameter lists (CSV, Excel, JSON)
- 📋 Upload PDF datasheets for automated extraction
- 🔍 Intelligent parameter extraction with fuzzy matching
- 📊 Split-screen interface with PDF viewer and parameter editor
- ✨ Interactive highlighting - click a parameter to see it highlighted in the PDF
- 💾 Export results to JSON, CSV, or Excel
- ⚡ Real-time validation and confidence scoring

## Technology Stack

### Frontend
- React 18 with TypeScript
- Tailwind CSS for styling
- React PDF for PDF viewing
- React Split Pane for resizable panels
- Lucide React for icons

### Backend
- FastAPI (Python)
- PyMuPDF (fitz) for PDF processing
- pdfplumber for table extraction
- FuzzyWuzzy for fuzzy string matching
- pandas for data handling

## Installation

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment:
```bash
python -m venv venv
```

3. Activate the virtual environment:
- Windows: `venv\Scripts\activate`
- Linux/Mac: `source venv/bin/activate`

4. Install dependencies:
```bash
pip install -r requirements.txt
```

5. Run the backend server:
```bash
uvicorn main:app --reload --port 8000
```

**Quick Start (Windows):** Simply run `start-backend.bat` from the project root

**Note:** The backend uses PyPDF2 and pdfplumber instead of PyMuPDF to avoid compilation requirements on Windows.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

4. Open http://localhost:3000 in your browser

## Usage

1. **Upload Parameter List**: Upload a CSV, Excel, or JSON file containing the parameters you want to extract
2. **Upload PDF Datasheet**: Upload the component datasheet PDF
3. **Review Extractions**: The system will automatically extract parameters and display them in the left panel
4. **Verify & Correct**: Click on any parameter to see it highlighted in the PDF viewer. Edit values as needed
5. **Export Results**: Save your verified data to JSON, CSV, or Excel format

## Project Structure

```
pdfread/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── pdf_processor.py        # PDF text extraction
│   ├── parameter_extractor.py  # Parameter extraction logic
│   ├── requirements.txt        # Python dependencies
│   └── uploads/                # Temporary file storage
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── components/         # React components
│   │   ├── App.tsx            # Main application
│   │   └── index.tsx          # Entry point
│   ├── package.json
│   └── tailwind.config.js
└── README.md
```

## API Endpoints

- `POST /api/upload-parameters` - Upload parameter list file
- `POST /api/upload-pdf` - Upload PDF datasheet
- `POST /api/extract` - Extract parameters from PDF
- `GET /api/pdf/{filename}` - Serve PDF file

## License

MIT License
