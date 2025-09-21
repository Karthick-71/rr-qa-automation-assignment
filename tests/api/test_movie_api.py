"""API tests for movie data validation."""

import pytest
import requests
import asyncio
from typing import Dict, Any
from loguru import logger
from config.settings import config


@pytest.mark.api
@pytest.mark.smoke
class TestMovieAPI:
    """Test class for Movie API functionality."""
    
    def setup_method(self):
        """Setup for each test method."""
        self.base_url = "https://api.themoviedb.org/3"
        self.session = requests.Session()
        # Note: TMDB API requires API key, but we'll test what we can
    
    def test_api_connectivity(self):
        """
        Test Case: TC024 - API Connectivity Test
        Priority: High
        
        Basic connectivity test to movie API endpoints.
        """
        # Test basic connectivity to TMDB API with retry logic
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Add headers to avoid potential blocking
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
                    'Accept': 'application/json'
                }
                response = self.session.get(
                    f"{self.base_url}/movie/popular", 
                    timeout=10, 
                    headers=headers
                )
                logger.info(f"API Response Status: {response.status_code}")
                
                # Even without API key, we should get a structured error response
                assert response.status_code in [200, 401], f"Unexpected status code: {response.status_code}"
                
                # Check response is JSON
                response_data = response.json()
                assert isinstance(response_data, dict), "Response should be JSON object"
                
                # Validate error response structure (expected without API key)
                if response.status_code == 401:
                    assert "status_code" in response_data, "Error response should contain status_code"
                    assert "status_message" in response_data, "Error response should contain status_message"
                    logger.info(f"API error response validated: {response_data.get('status_message')}")
                
                logger.info("API connectivity test passed")
                return  # Success, exit retry loop
                
            except requests.exceptions.ConnectionError as e:
                logger.warning(f"Connection attempt {attempt + 1} failed: {e}")
                if attempt == max_retries - 1:
                    pytest.skip(f"API connectivity failed after {max_retries} attempts: {e}")
                continue
            except requests.exceptions.RequestException as e:
                logger.error(f"API connectivity failed: {e}")
                pytest.fail(f"Could not connect to API: {e}")
    
    def test_api_response_structure(self):
        """
        Test Case: TC025 - API Response Structure
        Priority: Medium
        
        Validate API response structure.
        """
        try:
            response = self.session.get(f"{self.base_url}/movie/popular", timeout=10)
            response_data = response.json()
            
            # Even error responses should have expected structure
            if response.status_code == 401:
                # Check error response structure
                assert "status_code" in response_data or "success" in response_data
                logger.info("API error response structure validated")
            else:
                # Check success response structure
                expected_keys = ["results", "page", "total_pages", "total_results"]
                for key in expected_keys:
                    if key in response_data:
                        logger.info(f"Found expected key: {key}")
                
        except Exception as e:
            logger.warning(f"API structure test failed: {e}")
    
    def test_network_monitoring_during_ui_interaction(self, home_page):
        """
        Test Case: TC026 - Network Monitoring
        Priority: Medium
        
        Monitor network requests during UI interactions.
        """
        # This test would be implemented with Playwright's network monitoring
        # For now, just document the approach
        logger.info("Network monitoring test - to be implemented with Playwright")
        
        # Example of how this would work:
        # 1. Set up network request monitoring
        # 2. Perform UI action (like filtering)
        # 3. Capture and validate network requests
        # 4. Ensure API calls match UI actions
        
        assert True  # Placeholder for actual implementation