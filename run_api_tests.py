#!/usr/bin/env python3
"""
Script to run API tests with proper environment variable setting
This ensures TEST_API=1 is set correctly for all platforms
"""

import os
import subprocess
import sys
from pathlib import Path


def main():
    """Run API tests with TEST_API=1 set"""
    print("🚀 Running Local API tests with TEST_API=1...")
    
    # Set environment variable
    os.environ["TEST_API"] = "1"
    
    # Check if we're in the right directory
    if not Path("rest_client").exists():
        print("❌ Error: rest_client directory not found. Please run from project root.")
        sys.exit(1)
    
    # Run pytest with local API tests only
    test_command = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--disable-warnings",
        "-k", "TestLocalApiExample"  # Run only local API tests
    ]
    
    try:
        print(f"Running: {' '.join(test_command)}")
        print(f"TEST_API={os.environ.get('TEST_API', 'not set')}")
        print("⚠️  Make sure test_api.py is running on http://localhost:8000")
        print()
        
        result = subprocess.run(test_command, check=False)
        
        if result.returncode == 0:
            print("\n✅ Local API tests completed successfully!")
        else:
            print(f"\n❌ Local API tests failed with exit code {result.returncode}")
            print("💡 Make sure to start the test API server first:")
            print("   python test_api.py")
        
        return result.returncode
        
    except Exception as e:
        print(f"❌ Error running API tests: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main()) 