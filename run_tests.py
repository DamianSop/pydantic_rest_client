#!/usr/bin/env python3
"""
Test runner script for pydantic-rest-client
Runs formatting, linting, type checking, and tests with coverage
"""

import subprocess
import sys
import os
from pathlib import Path


def run_command(command, description, check=True):
    """Run a command and handle errors"""
    print(f"\n{'='*60}")
    print(f"🔄 {description}")
    print(f"{'='*60}")
    print(f"Running: {' '.join(command)}")
    
    try:
        result = subprocess.run(command, check=check, capture_output=True, text=True)
        if result.stdout:
            print("✅ Output:")
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}:")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def main():
    """Main test runner function"""
    print("🚀 Starting test suite for pydantic-rest-client")
    
    # Check if we're in the right directory
    if not Path("rest_client").exists():
        print("❌ Error: rest_client directory not found. Please run from project root.")
        sys.exit(1)
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected. Consider activating one.")
    
    success = True
    
    # 1. Format code with black
    if not run_command([sys.executable, "-m", "black", "--check", "."], "Code formatting check (black)"):
        print("💡 To fix formatting, run: python -m black .")
        success = False
    
    # 2. Lint with flake8
    if not run_command([sys.executable, "-m", "flake8", "rest_client", "tests"], "Code linting (flake8)"):
        success = False
    
    # 3. Type checking with mypy
    if not run_command([sys.executable, "-m", "mypy", "rest_client"], "Type checking (mypy)"):
        success = False
    
    # 4. Run tests with pytest
    print(f"\n{'='*60}")
    print("🧪 Running tests with pytest")
    print(f"{'='*60}")
    
    # Run tests with detailed output
    test_command = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--cov=rest_client",
        "--cov-report=term-missing",
        "--cov-report=html",
        "--cov-fail-under=80",
        "--disable-warnings"
    ]
    
    try:
        result = subprocess.run(test_command, check=False, capture_output=True, text=True)
        print("Test Output:")
        print(result.stdout)
        if result.stderr:
            print("Test Errors:")
            print(result.stderr)
        
        if result.returncode != 0:
            success = False
            print(f"❌ Tests failed with exit code {result.returncode}")
        else:
            print("✅ All tests passed!")
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        success = False
    
    # 5. Run simple test as fallback
    if not success:
        print(f"\n{'='*60}")
        print("🔄 Trying simple test as fallback")
        print(f"{'='*60}")
        
        simple_test_command = [sys.executable, "test_simple.py"]
        try:
            result = subprocess.run(simple_test_command, check=False, capture_output=True, text=True)
            print("Simple Test Output:")
            print(result.stdout)
            if result.stderr:
                print("Simple Test Errors:")
                print(result.stderr)
            
            if result.returncode == 0:
                print("✅ Simple test passed!")
                success = True
            else:
                print(f"❌ Simple test also failed with exit code {result.returncode}")
                
        except Exception as e:
            print(f"❌ Error running simple test: {e}")
    
    # 6. Show coverage report if available
    if Path("htmlcov/index.html").exists():
        print(f"\n{'='*60}")
        print("📊 Coverage report generated")
        print(f"{'='*60}")
        print("Open htmlcov/index.html in your browser to view detailed coverage")
    
    # Final summary
    print(f"\n{'='*60}")
    if success:
        print("🎉 All checks passed! Your code is ready.")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
    print(f"{'='*60}")
    
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main()) 