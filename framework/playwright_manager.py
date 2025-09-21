"""Playwright browser and context management."""

from typing import Optional, Dict, Any
from playwright.async_api import async_playwright, Browser, BrowserContext, Page, Playwright
from config.settings import config
from loguru import logger


class PlaywrightManager:
    """Manages Playwright browser instances and contexts."""
    
    def __init__(self) -> None:
        """Initialize PlaywrightManager."""
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None
    
    async def start_playwright(self) -> None:
        """Start Playwright instance."""
        self.playwright = await async_playwright().start()
        logger.info("Playwright started")
    
    async def launch_browser(self, 
                        browser_name: Optional[str] = None,
                        headless: Optional[bool] = None,
                        slow_mo: Optional[int] = None) -> Browser:
        """Launch browser.
        
        Args:
            browser_name: Browser to launch (chromium, firefox, webkit)
            headless: Run in headless mode
            slow_mo: Slow down operations by specified milliseconds
            
        Returns:
            Browser instance
        """
        browser_name = browser_name or config.browser
        headless = headless if headless is not None else config.headless
        slow_mo = slow_mo or config.slow_mo
        
        browser_args = {
            "headless": headless,
            "slow_mo": slow_mo,
            "args": [
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-extensions"
            ]
        }
        
        if browser_name.lower() == "chromium":
            self.browser = await self.playwright.chromium.launch(**browser_args)
        elif browser_name.lower() == "firefox":
            self.browser = await self.playwright.firefox.launch(**browser_args)
        elif browser_name.lower() == "webkit":
            self.browser = await self.playwright.webkit.launch(**browser_args)
        else:
            raise ValueError(f"Unsupported browser: {browser_name}")
        
        logger.info(f"Browser {browser_name} launched (headless: {headless})")
        return self.browser
    
    async def create_context(self, **kwargs) -> BrowserContext:
        """Create browser context.
        
        Returns:
            BrowserContext instance
        """
        if not self.browser:
            raise RuntimeError("Browser not launched. Call launch_browser() first.")
        
        context_options = {
            "viewport": {"width": 1920, "height": 1080},
            "ignore_https_errors": True,
            "record_video_dir": "reports/videos/",
            "record_video_size": {"width": 1920, "height": 1080},
            **kwargs
        }
        
        self.context = await self.browser.new_context(**context_options)
        logger.info("Browser context created")
        
        # Enable request/response logging
        self.context.on("request", self._log_request)
        self.context.on("response", self._log_response)
        
        return self.context
    
    async def create_page(self) -> Page:
        """Create new page.
        
        Returns:
            Page instance
        """
        if not self.context:
            raise RuntimeError("Context not created. Call create_context() first.")
        
        self.page = await self.context.new_page()
        
        # Set default timeout
        self.page.set_default_timeout(config.timeout)
        
        logger.info("New page created")
        return self.page
    
    async def close_page(self) -> None:
        """Close current page."""
        if self.page:
            await self.page.close()
            self.page = None
            logger.info("Page closed")
    
    async def close_context(self) -> None:
        """Close browser context."""
        if self.context:
            await self.context.close()
            self.context = None
            logger.info("Browser context closed")
    
    async def close_browser(self) -> None:
        """Close browser."""
        if self.browser:
            await self.browser.close()
            self.browser = None
            logger.info("Browser closed")
    
    async def stop_playwright(self) -> None:
        """Stop Playwright instance."""
        if self.playwright:
            await self.playwright.stop()
            self.playwright = None
            logger.info("Playwright stopped")
    
    async def cleanup(self) -> None:
        """Cleanup all resources."""
        await self.close_page()
        await self.close_context()
        await self.close_browser()
        await self.stop_playwright()
    
    def _log_request(self, request) -> None:
        """Log HTTP requests."""
        logger.debug(f"Request: {request.method} {request.url}")
    
    def _log_response(self, response) -> None:
        """Log HTTP responses."""
        logger.debug(f"Response: {response.status} {response.url}")