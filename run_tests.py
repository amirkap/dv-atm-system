#!/usr/bin/env python3
"""
Root Test Runner for ATM System
Simply calls the test runner in the tests directory
"""

import subprocess
import sys
import os

def main():
    """Run the test suite from the tests directory"""
    test_runner_path = os.path.join(os.path.dirname(__file__), "tests", "run_tests.py")
    
    try:
        result = subprocess.run([sys.executable, test_runner_path], cwd=os.path.dirname(__file__))
        sys.exit(result.returncode)
    except Exception as e:
        print(f"Error running tests: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()