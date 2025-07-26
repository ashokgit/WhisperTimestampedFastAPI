#!/usr/bin/env python3
"""
Basic tests for WhisperTimestampedFastAPI
These tests don't require models or actual API calls
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_basic_imports():
    """Test that basic modules can be imported without heavy dependencies"""
    try:
        # Test basic Python imports
        import tempfile
        import asyncio
        import logging
        print("✅ Basic Python modules import successfully")
        
        # Test FastAPI imports (optional for CI)
        try:
            from fastapi import FastAPI
            print("✅ FastAPI imports successfully")
        except ImportError:
            print("⚠️  FastAPI not available (expected in minimal CI environment)")
        
        return True
    except ImportError as e:
        print(f"❌ Basic import failed: {e}")
        return False

def test_app_structure():
    """Test app structure without importing heavy dependencies"""
    try:
        # Read the app.py file to check structure
        with open('app.py', 'r') as f:
            content = f.read()
        
        # Check for expected components
        expected_components = [
            'FastAPI',
            'SUPPORTED_FORMATS',
            'get_device_info',
            'get_optimal_device',
            'load_model'
        ]
        
        for component in expected_components:
            if component in content:
                print(f"✅ Found component: {component}")
            else:
                print(f"❌ Missing component: {component}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ App structure test failed: {e}")
        return False

def test_supported_formats():
    """Test supported audio formats by reading the constant"""
    try:
        # Read the SUPPORTED_FORMATS from app.py
        with open('app.py', 'r') as f:
            content = f.read()
        
        # Extract SUPPORTED_FORMATS line
        for line in content.split('\n'):
            if 'SUPPORTED_FORMATS' in line and '=' in line:
                print(f"✅ Found SUPPORTED_FORMATS definition: {line.strip()}")
                return True
        
        print("❌ SUPPORTED_FORMATS not found in app.py")
        return False
    except Exception as e:
        print(f"❌ Format test failed: {e}")
        return False

def test_endpoints_defined():
    """Test that expected endpoints are defined in app.py"""
    try:
        with open('app.py', 'r') as f:
            content = f.read()
        
        expected_endpoints = [
            '@app.get("/")',
            '@app.get("/health")',
            '@app.post("/transcribe")',
            '@app.post("/transcribe-url")',
            '@app.get("/models")'
        ]
        
        for endpoint in expected_endpoints:
            if endpoint in content:
                print(f"✅ Found endpoint: {endpoint}")
            else:
                print(f"❌ Missing endpoint: {endpoint}")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Endpoints test failed: {e}")
        return False

def test_requirements():
    """Test that requirements.txt exists and has expected dependencies"""
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read()
        
        expected_deps = [
            'fastapi',
            'uvicorn',
            'torch',
            'whisper-timestamped'
        ]
        
        for dep in expected_deps:
            if dep in content:
                print(f"✅ Found dependency: {dep}")
            else:
                print(f"⚠️  Missing dependency: {dep}")
        
        return True
    except Exception as e:
        print(f"❌ Requirements test failed: {e}")
        return False

def main():
    """Run all basic tests"""
    print("🧪 Running basic tests for WhisperTimestampedFastAPI...")
    print("=" * 50)
    
    tests = [
        test_basic_imports,
        test_app_structure,
        test_supported_formats,
        test_endpoints_defined,
        test_requirements
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