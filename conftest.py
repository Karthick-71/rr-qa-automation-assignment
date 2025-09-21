"""Simplified pytest configuration and fixtures."""

import asyncio
import pytest
import pytest_asyncio
from playwright.async_api import async_playwright, Page
from pages.home_page import HomePage
from utils.logger import setup_logger


def pytest_configure(config):
    """Configure pytest - correct signature."""
    setup_logger()


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for the session."""
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def browser():
    """Browser fixture."""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        yield browser
        await browser.close()


@pytest_asyncio.fixture
async def context(browser):
    """Browser context fixture."""
    context = await browser.new_context(
        viewport={"width": 1920, "height": 1080}
    )
    yield context
    await context.close()


@pytest_asyncio.fixture
async def page(context):
    """Page fixture."""
    page = await context.new_page()
    yield page
    await page.close()


@pytest_asyncio.fixture
async def home_page(page: Page) -> HomePage:
    """Home page fixture."""
    return HomePage(page)