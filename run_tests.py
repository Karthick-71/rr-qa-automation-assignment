#!/usr/bin/env python3
"""Test runner script with different execution modes."""

import subprocess
import sys
import argparse
from pathlib import Path
import time


def run_pytest(command, description):
    """Run pytest command and show results."""
    print(f"\n🧪 {description}")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        result = subprocess.run(command, shell=True)
        duration = time.time() - start_time
        
        if result.returncode == 0:
            print(f"✅ {description} PASSED ({duration:.2f}s)")
        else:
            print(f"❌ {description} FAILED ({duration:.2f}s)")
            
        return result.returncode == 0
        
    except Exception as e:
        print(f"💥 Error running {description}: {e}")
        return False


def main():
    """Main test runner function."""
    parser = argparse.ArgumentParser(description="RR QA Automation Test Runner")
    parser.add_argument("--suite", choices=["smoke", "regression", "api", "ui", "all"], 
                       default="smoke", help="Test suite to run")
    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"], 
                       default="chromium", help="Browser to use")
    parser.add_argument("--headed", action="store_true", help="Run in headed mode")
    parser.add_argument("--parallel", type=int, default=1, help="Number of parallel workers")
    
    args = parser.parse_args()
    
    print("🎭 RR QA Automation Test Runner")
    print("=" * 50)
    print(f"Suite: {args.suite}")
    print(f"Browser: {args.browser}")
    print(f"Mode: {'Headed' if args.headed else 'Headless'}")
    print(f"Workers: {args.parallel}")
    
    # Ensure reports directory exists
    Path("reports/html").mkdir(parents=True, exist_ok=True)
    
    # Base pytest command
    base_cmd = [
        "pytest",
        "-v",
        f"--browser={args.browser}",
        "--html=reports/html/report.html",
        "--self-contained-html"
    ]
    
    if args.headed:
        base_cmd.append("--headed")
    
    if args.parallel > 1:
        base_cmd.extend(["-n", str(args.parallel)])
    
    # Define test commands based on suite
    test_commands = {
        "smoke": base_cmd + ["-m", "smoke"],
        "regression": base_cmd + ["-m", "regression"],
        "api": base_cmd + ["tests/api/"],
        "ui": base_cmd + ["tests/ui/"],
        "all": base_cmd + ["tests/"]
    }
    
    # Run the selected test suite
    command = " ".join(test_commands[args.suite])
    success = run_pytest(command, f"Running {args.suite.upper()} tests")
    
    # Show results location
    print(f"\n📊 Test reports available at:")
    print(f"   HTML Report: reports/html/report.html")
    print(f"   Screenshots: reports/screenshots/")
    print(f"   Logs: logs/")
    
    if not success:
        sys.exit(1)
    
    print(f"\n🎉 {args.suite.upper()} test suite completed successfully!")


if __name__ == "__main__":
    main()