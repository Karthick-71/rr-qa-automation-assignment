"""Base page class with common functionality."""

from typing import Optional, List, Any
from playwright.async_api import Page, Locator, expect
from loguru import logger
import asyncio


class BasePage:
    """Base page class for all page objects."""
    
    def __init__(self, page: Page) -> None:
        """Initialize base page.
        
        Args:
            page: Playwright page instance
        """
        self.page = page
        self.timeout = 30000  # 30 seconds default timeout
    
    async def navigate_to(self, url: str) -> None:
        """Navigate to a specific URL.
        
        Args:
            url: URL to navigate to
        """
        logger.info(f"Navigating to: {url}")
        await self.page.goto(url, wait_until="networkidle")
        await self.page.wait_for_load_state("domcontentloaded")
    
    async def click_element(self, locator: str, timeout: Optional[int] = None) -> None:
        """Click an element.
        
        Args:
            locator: Element locator
            timeout: Optional timeout override
        """
        timeout = timeout or self.timeout
        logger.info(f"Clicking element: {locator}")
        await self.page.locator(locator).click(timeout=timeout)
    
    async def fill_input(self, locator: str, text: str, timeout: Optional[int] = None) -> None:
        """Fill input field.
        
        Args:
            locator: Input field locator
            text: Text to fill
            timeout: Optional timeout override
        """
        timeout = timeout or self.timeout
        logger.info(f"Filling input {locator} with: {text}")
        await self.page.locator(locator).fill(text, timeout=timeout)
    
    async def get_text(self, locator: str, timeout: Optional[int] = None) -> str:
        """Get text from element.
        
        Args:
            locator: Element locator
            timeout: Optional timeout override
            
        Returns:
            Element text content
        """
        timeout = timeout or self.timeout
        element = self.page.locator(locator)
        await element.wait_for(state="visible", timeout=timeout)
        return await element.text_content()
    
    async def wait_for_element(self, locator: str, state: str = "visible", timeout: Optional[int] = None) -> Locator:
        """Wait for element to be in specified state.
        
        Args:
            locator: Element locator
            state: Element state to wait for
            timeout: Optional timeout override
            
        Returns:
            Locator object
        """
        timeout = timeout or self.timeout
        element = self.page.locator(locator)
        await element.wait_for(state=state, timeout=timeout)
        return element
    
    async def is_visible(self, locator: str, timeout: Optional[int] = None) -> bool:
        """Check if element is visible.
        
        Args:
            locator: Element locator
            timeout: Optional timeout override
            
        Returns:
            True if visible, False otherwise
        """
        try:
            await self.wait_for_element(locator, "visible", timeout or 5000)
            return True
        except Exception:
            return False
    
    async def get_elements_count(self, locator: str) -> int:
        """Get count of elements matching locator.
        
        Args:
            locator: Element locator
            
        Returns:
            Number of matching elements
        """
        return await self.page.locator(locator).count()
    
    async def scroll_to_element(self, locator: str) -> None:
        """Scroll element into view.
        
        Args:
            locator: Element locator
        """
        await self.page.locator(locator).scroll_into_view_if_needed()
    
    async def take_screenshot(self, name: str) -> str:
        """Take screenshot and save it.
        
        Args:
            name: Screenshot name
            
        Returns:
            Screenshot file path
        """
        screenshot_path = f"reports/screenshots/{name}.png"
        await self.page.screenshot(path=screenshot_path)
        logger.info(f"Screenshot saved: {screenshot_path}")
        return screenshot_path
    
    async def wait_for_network_idle(self, timeout: Optional[int] = None) -> None:
        """Wait for network to be idle.
        
        Args:
            timeout: Optional timeout override
        """
        await self.page.wait_for_load_state("networkidle", timeout=timeout or self.timeout)
    
    async def hover_element(self, locator: str) -> None:
        """Hover over element.
        
        Args:
            locator: Element locator
        """
        await self.page.locator(locator).hover()
    
    async def select_dropdown_option(self, locator: str, option: str) -> None:
        """Select dropdown option.
        
        Args:
            locator: Dropdown locator
            option: Option to select
        """
        await self.page.locator(locator).select_option(option)
    
    async def press_key(self, key: str) -> None:
        """Press keyboard key.
        
        Args:
            key: Key to press
        """
        await self.page.keyboard.press(key)
    
    async def get_page_title(self) -> str:
        """Get page title.
        
        Returns:
            Page title
        """
        return await self.page.title()
    
    async def get_current_url(self) -> str:
        """Get current URL.
        
        Returns:
            Current page URL
        """
        return self.page.url
    
    async def reload_page(self) -> None:
        """Reload current page."""
        await self.page.reload(wait_until="networkidle")