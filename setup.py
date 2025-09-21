#!/usr/bin/env python3
"""
Simple setup script for RR QA Automation Assignment
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e}")
        print(f"Error output: {e.stderr}")
        return False

def main():
    """Main setup function."""
    print("🚀 Setting up RR QA Automation Assignment")
    print("=" * 50)
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11+ is required")
        sys.exit(1)
    
    print(f"✅ Python {sys.version_info.major}.{sys.version_info.minor} detected")
    
    # Install requirements
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        sys.exit(1)
    
    # Install Playwright browsers
    if not run_command("playwright install", "Installing Playwright browsers"):
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\nTo run tests:")
    print("  pytest tests/ -v")
    print("\nTo run with HTML report:")
    print("  pytest tests/ --html=reports/html/report.html --self-contained-html")

if __name__ == "__main__":
    main()
