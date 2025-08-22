#!/usr/bin/env python3
"""
Test Runner for ATM System
Runs all tests in sequence with proper reporting
"""

import subprocess
import sys
import time

def run_test(test_name, test_file, description):
    """Run a single test and report results"""
    print(f"\n{'='*60}")
    print(f"🧪 {test_name}")
    print(f"📝 {description}")
    print(f"{'='*60}")
    
    start_time = time.time()
    
    try:
        result = subprocess.run([sys.executable, test_file], 
                              capture_output=True, text=True, timeout=300)
        
        end_time = time.time()
        duration = end_time - start_time
        
        if result.returncode == 0:
            print(f"✅ {test_name} PASSED ({duration:.1f}s)")
            if result.stdout:
                print(result.stdout)
            return True
        else:
            print(f"❌ {test_name} FAILED ({duration:.1f}s)")
            if result.stdout:
                print("STDOUT:", result.stdout)
            if result.stderr:
                print("STDERR:", result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print(f"⏰ {test_name} TIMED OUT (>300s)")
        return False
    except Exception as e:
        print(f"💥 {test_name} ERROR: {e}")
        return False

def main():
    """Main test runner"""
    print("🚀 ATM System Test Suite")
    print("========================")
    
    # Check if system is running
    try:
        result = subprocess.run([sys.executable, "-c", 
                               "import requests; requests.get('http://localhost:8000/health', timeout=5)"],
                               capture_output=True, timeout=10)
        if result.returncode != 0:
            print("❌ ATM system not running. Please start with: uvicorn app.main:app --host 0.0.0.0 --port 8000")
            return False
    except:
        print("❌ Cannot connect to ATM system. Please ensure FastAPI is running on port 8000.")
        return False
    
    # Test suite
    tests = [
        ("Basic API Tests", "tests/test_api.py", 
         "Comprehensive functional tests for all endpoints"),
        ("Advanced Threading Tests", "tests/test_advanced_threading.py", 
         "Comprehensive thread safety and concurrency tests")
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_file, description in tests:
        if run_test(test_name, test_file, description):
            passed += 1
    
    # Summary
    print(f"\n{'='*60}")
    print(f"📊 TEST SUITE SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! ATM System is ready for production.")
        return True
    else:
        print(f"⚠️ {total - passed} test(s) failed. Please review and fix issues.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
