#!/usr/bin/env python3
import os
import tempfile
import asyncio
from typing import Optional, Dict, Any
import torch
import whisper_timestamped as whisper
from fastapi import FastAPI, File, UploadFile, HTTPException, Query
from fastapi.responses import JSONResponse
import aiofiles
import uvicorn
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Whisper Timestamped Microservice",
    description="Speech-to-text with timestamps using whisper-timestamped",
    version="1.0.0"
)

# Global model cache
MODEL_CACHE = {}

# Supported audio formats
SUPPORTED_FORMATS = {'.mp3', '.wav', '.m4a', '.flac', '.ogg', '.wma', '.aac'}

def get_device_info():
    """Get available device information"""
    device_info = {
        "cuda_available": torch.cuda.is_available(),
        "cuda_device_count": torch.cuda.device_count() if torch.cuda.is_available() else 0,
        "mps_available": torch.backends.mps.is_available() if hasattr(torch.backends, 'mps') else False,
        "cpu_count": os.cpu_count(),
    }
    
    if device_info["cuda_available"]:
        device_info["cuda_devices"] = [
            torch.cuda.get_device_name(i) 
            for i in range(device_info["cuda_device_count"])
        ]
    
    return device_info

def get_optimal_device():
    """Determine the best available device"""
    if torch.cuda.is_available():
        return "cuda"
    elif hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
        return "mps"
    else:
        return "cpu"

def load_model(model_name: str = "base", device: Optional[str] = None):
    """Load whisper model with caching"""
    if device is None:
        device = get_optimal_device()
    
    cache_key = f"{model_name}_{device}"
    
    if cache_key not in MODEL_CACHE:
        logger.info(f"Loading model {model_name} on device {device}")
        try:
            model = whisper.load_model(model_name, device=device)
            MODEL_CACHE[cache_key] = model
            logger.info(f"Model {model_name} loaded successfully on {device}")
        except Exception as e:
            logger.error(f"Failed to load model {model_name} on {device}: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to load model: {e}")
    
    return MODEL_CACHE[cache_key]

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "whisper-timestamped",
        "device_info": get_device_info()
    }

@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "device_info": get_device_info(),
        "supported_formats": list(SUPPORTED_FORMATS),
        "available_models": ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
    }

@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    model: str = Query(default="base", description="Whisper model to use"),
    language: Optional[str] = Query(default=None, description="Language code (auto-detect if None)"),
    device: Optional[str] = Query(default=None, description="Device to use (auto if None)"),
    word_timestamps: bool = Query(default=True, description="Include word-level timestamps"),
    verbose: bool = Query(default=False, description="Verbose output")
):
    """Transcribe audio file with timestamps"""
    
    # Validate file format
    file_extension = os.path.splitext(file.filename)[1].lower()
    if file_extension not in SUPPORTED_FORMATS:
        raise HTTPException(
            status_code=400, 
            detail=f"Unsupported file format. Supported formats: {list(SUPPORTED_FORMATS)}"
        )
    
    # Create temporary file
    temp_file = None
    try:
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Load the appropriate model
        whisper_model = load_model(model, device)
        
        # Transcribe with timestamps
        logger.info(f"Transcribing {file.filename} with model {model}")
        
        result = whisper.transcribe(
            whisper_model,
            temp_file_path,
            language=language,
            verbose=verbose
        )
        
        # Clean up temporary file
        os.unlink(temp_file_path)
        
        # Format response
        response = {
            "text": result["text"],
            "language": result.get("language", "unknown"),
            "segments": result.get("segments", []),
            "model_used": model,
            "device_used": get_optimal_device() if device is None else device,
            "filename": file.filename
        }
        
        logger.info(f"Transcription completed for {file.filename}")
        return JSONResponse(content=response)
        
    except Exception as e:
        # Clean up temporary file if it exists
        if temp_file and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        
        logger.error(f"Transcription failed: {e}")
        raise HTTPException(status_code=500, detail=f"Transcription failed: {str(e)}")

@app.post("/transcribe-url")
async def transcribe_from_url(
    url: str,
    model: str = Query(default="base", description="Whisper model to use"),
    language: Optional[str] = Query(default=None, description="Language code (auto-detect if None)"),
    device: Optional[str] = Query(default=None, description="Device to use (auto if None)"),
    word_timestamps: bool = Query(default=True, description="Include word-level timestamps"),
    verbose: bool = Query(default=False, description="Verbose output")
):
    """Transcribe audio from URL"""
    try:
        import requests
        
        # Download file from URL
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()
        
        # Get content type and determine file extension
        content_type = response.headers.get('content-type', '')
        if 'audio' not in content_type.lower():
            logger.warning(f"Content type {content_type} might not be audio")
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.tmp') as temp_file:
            for chunk in response.iter_content(chunk_size=8192):
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        # Load model and transcribe
        whisper_model = load_model(model, device)
        
        logger.info(f"Transcribing audio from URL: {url}")
        
        result = whisper.transcribe(
            whisper_model,
            temp_file_path,
            language=language,
            verbose=verbose
        )
        
        # Clean up
        os.unlink(temp_file_path)
        
        response_data = {
            "text": result["text"],
            "language": result.get("language", "unknown"),
            "segments": result.get("segments", []),
            "model_used": model,
            "device_used": get_optimal_device() if device is None else device,
            "source_url": url
        }
        
        return JSONResponse(content=response_data)
        
    except Exception as e:
        logger.error(f"URL transcription failed: {e}")
        raise HTTPException(status_code=500, detail=f"URL transcription failed: {str(e)}")

@app.get("/models")
async def list_models():
    """List available models and their status"""
    models = ["tiny", "base", "small", "medium", "large", "large-v2", "large-v3"]
    loaded_models = list(MODEL_CACHE.keys())
    
    return {
        "available_models": models,
        "loaded_models": loaded_models,
        "device_info": get_device_info()
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    
    logger.info(f"Starting Whisper Timestamped service on {host}:{port}")
    logger.info(f"Device info: {get_device_info()}")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=False,
        log_level="info"
    )