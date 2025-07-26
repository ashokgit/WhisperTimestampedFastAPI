#!/usr/bin/env python3
"""
Test client for Whisper Timestamped Microservice
"""
import requests
import json
import time
import argparse
from pathlib import Path

class WhisperClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url.rstrip('/')
    
    def health_check(self):
        """Check service health"""
        try:
            response = requests.get(f"{self.base_url}/health")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Health check failed: {e}")
            return None
    
    def list_models(self):
        """List available models"""
        try:
            response = requests.get(f"{self.base_url}/models")
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Failed to list models: {e}")
            return None
    
    def transcribe_file(self, file_path, model="base", language=None, 
                       word_timestamps=True, verbose=False):
        """Transcribe audio file"""
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        params = {
            "model": model,
            "word_timestamps": word_timestamps,
            "verbose": verbose
        }
        if language:
            params["language"] = language
        
        try:
            with open(file_path, 'rb') as f:
                files = {"file": (file_path.name, f, "audio/wav")}
                response = requests.post(
                    f"{self.base_url}/transcribe",
                    files=files,
                    params=params,
                    timeout=300  # 5 minute timeout
                )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Transcription failed: {e}")
            return None
    
    def transcribe_url(self, url, model="base", language=None, 
                      word_timestamps=True, verbose=False):
        """Transcribe audio from URL"""
        data = {
            "url": url,
            "model": model,
            "word_timestamps": word_timestamps,
            "verbose": verbose
        }
        if language:
            data["language"] = language
        
        try:
            response = requests.post(
                f"{self.base_url}/transcribe-url",
                json=data,
                timeout=300
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"URL transcription failed: {e}")
            return None

def format_timestamps(segments):
    """Format segment timestamps for display"""
    formatted = []
    for segment in segments:
        start = segment.get('start', 0)
        end = segment.get('end', 0)
        text = segment.get('text', '').strip()
        
        start_time = f"{int(start//60):02d}:{int(start%60):02d}.{int((start%1)*1000):03d}"
        end_time = f"{int(end//60):02d}:{int(end%60):02d}.{int((end%1)*1000):03d}"
        
        formatted.append(f"[{start_time} --> {end_time}] {text}")
    
    return formatted

def main():
    parser = argparse.ArgumentParser(description="Test Whisper Timestamped Service")
    parser.add_argument("--url", default="http://localhost:8000", 
                       help="Service URL")
    parser.add_argument("--health", action="store_true", 
                       help="Check service health")
    parser.add_argument("--models", action="store_true", 
                       help="List available models")
    parser.add_argument("--file", type=str, 
                       help="Audio file to transcribe")
    parser.add_argument("--audio-url", type=str, 
                       help="Audio URL to transcribe")
    parser.add_argument("--model", default="base", 
                       help="Model to use (default: base)")
    parser.add_argument("--language", type=str, 
                       help="Language code (optional)")
    parser.add_argument("--no-word-timestamps", action="store_true", 
                       help="Disable word timestamps")
    parser.add_argument("--verbose", action="store_true", 
                       help="Verbose output")
    parser.add_argument("--output", type=str, 
                       help="Output file for results")
    
    args = parser.parse_args()
    
    client = WhisperClient(args.url)
    
    # Health check
    if args.health:
        print("=== Health Check ===")
        health = client.health_check()
        if health:
            print(json.dumps(health, indent=2))
        else:
            print("Service is not healthy")
            return 1
        print()
    
    # List models
    if args.models:
        print("=== Available Models ===")
        models = client.list_models()
        if models:
            print(json.dumps(models, indent=2))
        else:
            print("Failed to retrieve models")
            return 1
        print()
    
    # Transcribe file
    if args.file:
        print(f"=== Transcribing File: {args.file} ===")
        start_time = time.time()
        
        result = client.transcribe_file(
            args.file,
            model=args.model,
            language=args.language,
            word_timestamps=not args.no_word_timestamps,
            verbose=args.verbose
        )
        
        end_time = time.time()
        
        if result:
            print(f"Transcription completed in {end_time - start_time:.2f} seconds")
            print(f"Language: {result.get('language', 'unknown')}")
            print(f"Model: {result.get('model_used', 'unknown')}")
            print(f"Device: {result.get('device_used', 'unknown')}")
            print()
            
            print("=== Full Text ===")
            print(result['text'])
            print()
            
            if result.get('segments'):
                print("=== Timestamped Segments ===")
                formatted_segments = format_timestamps(result['segments'])
                for segment in formatted_segments:
                    print(segment)
                print()
            
            # Save to file if requested
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"Results saved to {args.output}")
        else:
            print("Transcription failed")
            return 1
    
    # Transcribe URL
    if args.audio_url:
        print(f"=== Transcribing URL: {args.audio_url} ===")
        start_time = time.time()
        
        result = client.transcribe_url(
            args.audio_url,
            model=args.model,
            language=args.language,
            word_timestamps=not args.no_word_timestamps,
            verbose=args.verbose
        )
        
        end_time = time.time()
        
        if result:
            print(f"Transcription completed in {end_time - start_time:.2f} seconds")
            print(f"Language: {result.get('language', 'unknown')}")
            print(f"Model: {result.get('model_used', 'unknown')}")
            print(f"Device: {result.get('device_used', 'unknown')}")
            print()
            
            print("=== Full Text ===")
            print(result['text'])
            print()
            
            if result.get('segments'):
                print("=== Timestamped Segments ===")
                formatted_segments = format_timestamps(result['segments'])
                for segment in formatted_segments:
                    print(segment)
                print()
            
            # Save to file if requested
            if args.output:
                with open(args.output, 'w') as f:
                    json.dump(result, f, indent=2)
                print(f"Results saved to {args.output}")
        else:
            print("Transcription failed")
            return 1
    
    return 0

if __name__ == "__main__":
    exit(main())