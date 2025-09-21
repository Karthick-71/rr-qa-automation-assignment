"""Tests for known issues mentioned in the assignment."""

import pytest
from playwright.async_api import Page, TimeoutError
from pages.home_page import HomePage
from loguru import logger
from config.settings import config


@pytest.mark.asyncio
class TestKnownIssues:
    """Test class for documenting known issues."""
    
    @pytest.mark.asyncio
    async def test_direct_url_access_popular(self, page: Page):
        """
        Test Case: TC027 - Direct URL Access Issue
        Priority: High
        
        Known Issue: Direct access to specific URLs fails
        URL: https://tmdb-discover.surge.sh/popular
        """
        direct_url = f"{config.base_url}popular"
        logger.info(f"Testing direct access to: {direct_url}")
        
        try:
            await page.goto(direct_url, wait_until="networkidle", timeout=15000)
            
            # Check if we actually got the popular page or were redirected
            current_url = page.url
            logger.info(f"Current URL after navigation: {current_url}")
            
            # Check if page loaded properly
            has_content = await page.locator("img").count() > 0
            has_navigation = await page.locator("text=Popular").is_visible()
            
            if has_content and has_navigation:
                logger.info("Direct URL access worked - issue may be resolved")
                await page.screenshot(path="reports/screenshots/direct_url_success.png")
            else:
                logger.warning("Direct URL access failed as expected (known issue)")
                await page.screenshot(path="reports/screenshots/direct_url_failure.png")
                
        except TimeoutError:
            logger.warning("Direct URL access timed out (known issue confirmed)")
            await page.screenshot(path="reports/screenshots/direct_url_timeout.png")
            
        except Exception as e:
            logger.error(f"Direct URL access failed with error: {e}")
            await page.screenshot(path="reports/screenshots/direct_url_error.png")
    
    @pytest.mark.asyncio
    async def test_navigation_from_home_works(self, home_page: HomePage):
        """
        Test Case: TC028 - Normal Navigation Works
        Priority: High
        
        Verify that normal navigation (not direct URL) works fine
        """
        await home_page.navigate_to_home()
        
        # Click Popular category normally
        await home_page.select_category("popular")
        
        # Verify it worked
        movie_count = await home_page.get_movie_count()
        logger.info(f"Normal navigation to Popular found {movie_count} movies")
        
        assert movie_count > 0, "Normal navigation should work"
        await home_page.take_screenshot("normal_navigation_success")