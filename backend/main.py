from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
import os
import json
import shutil
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd

from pdf_processor import PDFProcessor
from parameter_extractor import ParameterExtractor

app = FastAPI(title="Engineering Parameter Extraction Tool")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create uploads directory
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Global storage for current session
session_data = {
    "parameters": [],
    "pdf_path": None,
    "pdf_text": None,
    "pdf_pages": []
}


@app.get("/")
async def root():
    return {"message": "Engineering Parameter Extraction API"}


@app.post("/api/upload-parameters")
async def upload_parameters(file: UploadFile = File(...)):
    """Upload and parse parameter list file (CSV, Excel, JSON)"""
    try:
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Parse file based on extension
        file_ext = file.filename.lower().split('.')[-1]
        parameters = []
        
        if file_ext == 'csv':
            df = pd.read_csv(file_path)
            # Assume first column contains parameter names
            parameters = df.iloc[:, 0].tolist()
        elif file_ext in ['xlsx', 'xls']:
            df = pd.read_excel(file_path)
            parameters = df.iloc[:, 0].tolist()
        elif file_ext == 'json':
            with open(file_path, 'r') as f:
                data = json.load(f)
                if isinstance(data, list):
                    parameters = data
                elif isinstance(data, dict) and 'parameters' in data:
                    parameters = data['parameters']
        else:
            raise HTTPException(status_code=400, detail="Unsupported file format")
        
        # Clean parameters
        parameters = [str(p).strip() for p in parameters if p and str(p).strip()]
        
        # Store in session
        session_data["parameters"] = parameters
        
        # Clean up file
        os.remove(file_path)
        
        return {
            "success": True,
            "parameters": parameters,
            "count": len(parameters)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):
    """Upload PDF datasheet"""
    try:
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Only PDF files are supported")
        
        # Save PDF file
        pdf_path = UPLOAD_DIR / file.filename
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process PDF
        processor = PDFProcessor(str(pdf_path))
        pdf_text = processor.extract_text()
        pdf_pages = processor.extract_pages()
        
        # Store in session
        session_data["pdf_path"] = str(pdf_path)
        session_data["pdf_text"] = pdf_text
        session_data["pdf_pages"] = pdf_pages
        
        return {
            "success": True,
            "filename": file.filename,
            "pages": len(pdf_pages),
            "pdf_url": f"/api/pdf/{file.filename}"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/extract")
async def extract_parameters():
    """Extract parameters from uploaded PDF"""
    try:
        if not session_data["parameters"]:
            raise HTTPException(status_code=400, detail="No parameters uploaded")
        
        if not session_data["pdf_path"]:
            raise HTTPException(status_code=400, detail="No PDF uploaded")
        
        # Extract parameters
        extractor = ParameterExtractor(
            session_data["pdf_text"],
            session_data["pdf_pages"]
        )
        
        results = []
        for param_name in session_data["parameters"]:
            extraction = extractor.extract_parameter(param_name)
            results.append(extraction)
        
        return {
            "success": True,
            "results": results,
            "metadata": {
                "total_parameters": len(results),
                "extracted_count": sum(1 for r in results if r["value"] != "NF"),
                "not_found_count": sum(1 for r in results if r["value"] == "NF")
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/pdf/{filename}")
async def get_pdf(filename: str):
    """Serve PDF file"""
    pdf_path = UPLOAD_DIR / filename
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF not found")
    
    return FileResponse(pdf_path, media_type="application/pdf")


@app.post("/api/export")
async def export_data(data: Dict[str, Any]):
    """Export extracted data to JSON"""
    try:
        export_format = data.get("format", "json")
        parameters = data.get("parameters", [])
        
        if export_format == "json":
            return JSONResponse(content={
                "metadata": data.get("metadata", {}),
                "parameters": parameters
            })
        
        return {"success": True}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
