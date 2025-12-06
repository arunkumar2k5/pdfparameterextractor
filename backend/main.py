from fastapi import FastAPI, UploadFile, File, HTTPException, Form
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
from markdown_converter import MarkdownConverter
from markdown_parameter_extractor import MarkdownParameterExtractor
from openai_extractor import OpenAIExtractor
<<<<<<< HEAD
from graph_analyzer import GraphAnalyzer
=======
from vision_extractor import VisionExtractor
from config import APIConfig
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
import dev_cache

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
    "pdf_pages": [],
    "markdown": None,
    "page_mapping": {},
    "total_pages": 0
}


@app.get("/")
async def root():
    return {"message": "Engineering Parameter Extraction API"}


@app.get("/api/config")
async def get_config():
    """Get current API configuration"""
    try:
        config_info = APIConfig.get_provider_info()
        is_valid, error_msg = APIConfig.validate_config()
        
        return {
            "success": True,
            "config": config_info,
            "is_valid": is_valid,
            "error": error_msg if not is_valid else None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }


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
                    # Handle list of strings or list of dicts with 'name' field
                    parameters = [p if isinstance(p, str) else p.get('name', str(p)) for p in data]
                elif isinstance(data, dict) and 'parameters' in data:
                    param_list = data['parameters']
                    # Handle list of strings or list of dicts with 'name' field
                    parameters = [p if isinstance(p, str) else p.get('name', str(p)) for p in param_list]
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
        
        # DEVELOPMENT MODE: Use cached data to skip slow conversion
        if dev_cache.DEV_MODE and dev_cache.is_cache_available():
            print("🚀 DEV MODE: Using cached PDF and markdown")
            
            # Load from cache
            cached_pdf_path, markdown, page_mapping, total_pages = dev_cache.load_from_cache()
            
            # Process cached PDF for highlighting
            processor = PDFProcessor(cached_pdf_path)
            pdf_text = processor.extract_text()
            pdf_pages = processor.extract_pages()
            
            # Store in session
            session_data["pdf_path"] = cached_pdf_path
            session_data["pdf_text"] = pdf_text
            session_data["pdf_pages"] = pdf_pages
            session_data["markdown"] = markdown
            session_data["page_mapping"] = page_mapping
            session_data["total_pages"] = total_pages
            
            return {
                "success": True,
                "filename": Path(cached_pdf_path).name,
                "pages": len(pdf_pages),
                "pdf_url": f"/api/pdf/{Path(cached_pdf_path).name}",
                "markdown_length": len(markdown),
                "has_markdown": True,
                "dev_mode": True
            }
        
        # PRODUCTION MODE: Normal processing
        # Save PDF file
        pdf_path = UPLOAD_DIR / file.filename
        with open(pdf_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        # Process PDF with both methods
        # 1. Original PDF processing (for highlighting)
        processor = PDFProcessor(str(pdf_path))
        pdf_text = processor.extract_text()
        pdf_pages = processor.extract_pages()
        
        # 2. Docling markdown conversion (for better search)
        print("⏳ Converting PDF to markdown with Docling...")
        md_converter = MarkdownConverter()
        md_result = md_converter.convert_pdf_to_markdown(str(pdf_path))
        
        # Save to cache for future dev use
        if dev_cache.DEV_MODE:
            print("💾 Saving to cache for future dev use...")
            dev_cache.save_to_cache(str(pdf_path), md_result["markdown"], md_result["page_mapping"])
        
        # Store in session
        session_data["pdf_path"] = str(pdf_path)
        session_data["pdf_text"] = pdf_text
        session_data["pdf_pages"] = pdf_pages
        session_data["markdown"] = md_result["markdown"]
        session_data["page_mapping"] = md_result["page_mapping"]
        session_data["total_pages"] = md_result["total_pages"]
        
        return {
            "success": True,
            "filename": file.filename,
            "pages": len(pdf_pages),
            "pdf_url": f"/api/pdf/{file.filename}",
            "markdown_length": len(md_result["markdown"]),
            "has_markdown": True,
            "dev_mode": False
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/extract")
async def extract_parameters(request: Dict[str, Any]):
    """Extract parameters from uploaded PDF using markdown or AI"""
    try:
        if not session_data["parameters"]:
            raise HTTPException(status_code=400, detail="No parameters uploaded")
        
        if not session_data["pdf_path"]:
            raise HTTPException(status_code=400, detail="No PDF uploaded")
        
        # Get extraction mode from request
        mode = request.get("mode", "simple")  # "simple" or "ai"
        
        results = []
        
        if mode == "ai":
            # AI-powered extraction using configured provider (OpenAI or OpenRouter)
            try:
<<<<<<< HEAD
                print(f"\n🤖 Starting AI extraction for {len(session_data['parameters'])} parameters...")
                print(f"📋 Parameters: {session_data['parameters']}")
                print(f"📄 Markdown length: {len(session_data.get('markdown', ''))} chars")
                
                extractor = OpenAIExtractor()  # Reads from .env automatically
=======
                extractor = OpenAIExtractor()  # Reads from config/.env automatically
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
                results = extractor.extract_parameters(
                    session_data["markdown"],
                    session_data["parameters"],
                    session_data.get("page_mapping")
                )
                
                print(f"✅ AI extraction completed: {len(results)} results returned")
                found_count = sum(1 for r in results if r.get("value") != "NF")
                print(f"   Found: {found_count}, Not found: {len(results) - found_count}")
                
            except ValueError as e:
<<<<<<< HEAD
                print(f"❌ API key error: {str(e)}")
                raise HTTPException(status_code=400, detail=f"OpenAI API key not configured. Please set OPENAI_API_KEY in backend/.env file")
            except Exception as e:
                print(f"❌ Extraction error: {str(e)}")
                import traceback
                traceback.print_exc()
                raise HTTPException(status_code=500, detail=f"OpenAI extraction failed: {str(e)}")
=======
                raise HTTPException(status_code=400, detail=f"API configuration error: {str(e)}. Please check your .env file.")
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"AI extraction failed: {str(e)}")
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
        
        else:
            # Simple search mode (existing logic)
            if session_data.get("markdown"):
                extractor = MarkdownParameterExtractor(
                    session_data["markdown"],
                    session_data["page_mapping"],
                    session_data["pdf_pages"]
                )
            else:
                # Fallback to original PDF extractor
                extractor = ParameterExtractor(
                    session_data["pdf_text"],
                    session_data["pdf_pages"]
                )
            
            for param_name in session_data["parameters"]:
                extraction = extractor.extract_parameter(param_name)
                results.append(extraction)
        
        return {
            "success": True,
            "results": results,
            "metadata": {
                "total_parameters": len(results),
                "extracted_count": sum(1 for r in results if r["value"] != "NF"),
                "not_found_count": sum(1 for r in results if r["value"] == "NF"),
                "extraction_mode": mode,
                "used_markdown": session_data.get("markdown") is not None
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/pdf/{filename}")
async def get_pdf(filename: str):
    """Serve PDF file"""
    # Check uploads directory first
    pdf_path = UPLOAD_DIR / filename
    if pdf_path.exists():
        return FileResponse(pdf_path, media_type="application/pdf")
    
    # Check dev cache directory
    cache_pdf_path = dev_cache.CACHE_DIR / filename
    if cache_pdf_path.exists():
        return FileResponse(cache_pdf_path, media_type="application/pdf")
    
    raise HTTPException(status_code=404, detail="PDF not found")


@app.get("/api/markdown")
async def get_markdown():
    """Get markdown content and page mapping"""
    if not session_data.get("markdown"):
        raise HTTPException(status_code=404, detail="No markdown available")
    
    return JSONResponse(content={
        "markdown": session_data["markdown"],
        "page_mapping": session_data["page_mapping"],
        "total_pages": session_data["total_pages"]
    })


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


@app.post("/api/analyze-graph")
<<<<<<< HEAD
async def analyze_graph(
    file: UploadFile = File(...),
    question: str = Form(None)
):
    """Analyze graph image and extract equations or answer a custom question using OpenAI Vision API"""
=======
async def analyze_graph(file: UploadFile = File(...), prompt: str = Form(None)):
    """Analyze a graph image using vision AI"""
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
    try:
        # Validate file type
        if not file.content_type or not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="Only image files are supported")
        
<<<<<<< HEAD
        print(f"\n📊 Received graph image: {file.filename}")
        if question:
            print(f"❓ Custom question: {question}")
        
        # Save uploaded image
        image_path = UPLOAD_DIR / file.filename
        with open(image_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        
        print(f"💾 Saved image to: {image_path}")
        
        # Analyze graph using OpenAI Vision
        try:
            analyzer = GraphAnalyzer()
            result = analyzer.analyze_graph(str(image_path), custom_question=question)
            
            if result["success"]:
                if result.get("question_answer"):
                    print(f"✅ Question answered successfully")
                else:
                    print(f"✅ Graph analysis completed: {len(result['curves'])} curve(s) found")
            else:
                print(f"❌ Graph analysis failed: {result.get('error', 'Unknown error')}")
            
            return JSONResponse(content=result)
            
        except ValueError as e:
            # API key not configured
            raise HTTPException(
                status_code=400, 
                detail=f"OpenAI API key not configured. Please set OPENAI_API_KEY in backend/.env file"
            )
        except Exception as e:
            print(f"❌ Graph analysis error: {str(e)}")
            import traceback
            traceback.print_exc()
            raise HTTPException(status_code=500, detail=f"Graph analysis failed: {str(e)}")
=======
        # Read image data
        image_data = await file.read()
        
        # Get image format
        image_format = file.content_type.split('/')[-1]
        if image_format == 'jpeg':
            image_format = 'jpeg'
        elif image_format == 'jpg':
            image_format = 'jpeg'
        
        # Initialize vision extractor
        try:
            extractor = VisionExtractor()
        except ValueError as e:
            raise HTTPException(status_code=400, detail=f"Vision API configuration error: {str(e)}")
        
        # Debug: Print what we received
        print(f"📥 Received prompt from frontend: '{prompt}'")
        
        # Analyze the graph
        if prompt and prompt.strip():
            print(f"✅ Using analyze_graph with user question")
            result = extractor.analyze_graph(image_data, prompt)
        else:
            print(f"⚠️ No prompt provided, using extract_equation")
            result = extractor.extract_equation(image_data)
        
        if result["success"]:
            return {
                "success": True,
                "answer": result["answer"],
                "model": result["model"],
                "provider": result["provider"]
            }
        else:
            raise HTTPException(status_code=500, detail=result.get("error", "Analysis failed"))
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5
    
    except HTTPException:
        raise
    except Exception as e:
<<<<<<< HEAD
        print(f"❌ Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
=======
        raise HTTPException(status_code=500, detail=f"Graph analysis failed: {str(e)}")
>>>>>>> 7560fa43c8d7e652d881cb9f983e0c44ad3dd6e5


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
