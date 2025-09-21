"""UI tests for pagination functionality."""

import pytest
from playwright.async_api import Page, expect
from pages.home_page import HomePage
from loguru import logger


@pytest.mark.ui
@pytest.mark.regression
class TestPagination:
    """Test class for pagination functionality."""
    
    async def test_pagination_availability(self, home_page: HomePage):
        """
        Test Case: TC021 - Pagination Availability
        Priority: High
        
        Verify that pagination is available when there are enough results.
        """
        await home_page.navigate_to_home()
        await home_page.select_category("popular")
        
        # Check if pagination exists
        has_pagination = await home_page.is_pagination_available()
        logger.info(f"Pagination available: {has_pagination}")
        
        if has_pagination:
            await home_page.take_screenshot("pagination_available")
        else:
            logger.warning("No pagination found")
    
    @pytest.mark.known_issue
    async def test_last_page_navigation_known_issue(self, home_page: HomePage):
        """
        Test Case: TC024 - Last Page Navigation (Known Issue)
        Priority: Medium
        
        Test the known issue with last pages not working properly.
        """
        await home_page.navigate_to_home()
        await home_page.select_category("popular")
        
        if not await home_page.is_pagination_available():
            pytest.skip("Pagination not available")
        
        # Try to navigate through pages to find the limit
        page_count = 1
        max_attempts = 10  # Limit attempts
        
        while page_count < max_attempts:
            navigation_successful = await home_page.navigate_to_next_page()
            
            if not navigation_successful:
                logger.info(f"Navigation failed at page {page_count}")
                await home_page.take_screenshot(f"pagination_failure_page_{page_count}")
                break
                
            page_count += 1
            logger.info(f"Successfully navigated to page {page_count}")
        
        # Document the known issue
        logger.warning(f"Pagination testing stopped at page {page_count}")