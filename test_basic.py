#!/usr/bin/env python3
"""
Basic tests for WhisperTimestampedFastAPI
These tests don't require models or actual API calls
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all required modules can be imported"""
    try:
        import app
        print("✅ App module imports successfully")
        
        from app import get_device_info, get_optimal_device, SUPPORTED_FORMATS
        print("✅ Core functions import successfully")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_device_detection():
    """Test device detection logic"""
    try:
        from app import get_device_info, get_optimal_device
        
        device_info = get_device_info()
        print(f"✅ Device info: {device_info}")
        
        optimal_device = get_optimal_device()
        print(f"✅ Optimal device: {optimal_device}")
        
        # Check that device info has expected keys
        expected_keys = ['cuda_available', 'cuda_device_count', 'mps_available', 'cpu_count']
        for key in expected_keys:
            assert key in device_info, f"Missing key: {key}"
        
        return True
    except Exception as e:
        print(f"❌ Device detection failed: {e}")
        return False

def test_supported_formats():
    """Test supported audio formats"""
    try:
        from app import SUPPORTED_FORMATS
        
        print(f"✅ Supported formats: {SUPPORTED_FORMATS}")
        
        # Check that common formats are supported
        common_formats = {'.wav', '.mp3', '.m4a'}
        for fmt in common_formats:
            assert fmt in SUPPORTED_FORMATS, f"Missing format: {fmt}"
        
        return True
    except Exception as e:
        print(f"❌ Format test failed: {e}")
        return False

def test_fastapi_app():
    """Test FastAPI app creation"""
    try:
        from app import app as fastapi_app
        
        print("✅ FastAPI app created successfully")
        
        # Check that app has expected endpoints
        routes = [route.path for route in fastapi_app.routes]
        expected_routes = ['/', '/health', '/transcribe', '/transcribe-url', '/models']
        
        for route in expected_routes:
            assert route in routes, f"Missing route: {route}"
        
        print(f"✅ All expected routes found: {routes}")
        return True
    except Exception as e:
        print(f"❌ FastAPI app test failed: {e}")
        return False

def main():
    """Run all basic tests"""
    print("🧪 Running basic tests for WhisperTimestampedFastAPI...")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_device_detection,
        test_supported_formats,
        test_fastapi_app
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
            print()
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            print()
    
    print("=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed!")
        return 0
    else:
        print("❌ Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(main()) 