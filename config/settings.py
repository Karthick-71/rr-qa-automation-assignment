"""Configuration management for the test framework."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class TestConfig:
    """Simple test configuration."""
    
    def __init__(self):
        self.base_url = os.getenv("BASE_URL", "https://tmdb-discover.surge.sh/")
        self.browser = os.getenv("BROWSER", "chromium")
        self.headless = os.getenv("HEADLESS", "false").lower() == "true"
        self.timeout = int(os.getenv("TIMEOUT", "30000"))
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.log_file = os.getenv("LOG_FILE", "logs/test_execution.log")

# Global config instance
config = TestConfig()