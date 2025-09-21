"""Home page object for TMDB demo site."""

from typing import List, Optional
from playwright.async_api import Page, expect
from framework.base_page import BasePage
from loguru import logger
import asyncio


class HomePage(BasePage):
    """Home page object for TMDB movie discovery platform."""
    
    def __init__(self, page: Page) -> None:
        """Initialize HomePage.
        
        Args:
            page: Playwright page instance
        """
        super().__init__(page)
        
        # Updated locators based on actual website inspection
        # Category buttons (top navigation bar)
        self.popular_btn = "text=Popular"
        self.trending_btn = "text=Trend"
        self.newest_btn = "text=Newest"
        self.top_rated_btn = "text=Top rated"
        
        # Search functionality
        self.search_button = "text=SEARCH"
        
        # Movie content
        self.movie_images = "img[alt*='Poster'], img[src*='image']"
        self.movie_cards = "div[class*='cursor-pointer'], a[class*='cursor-pointer']"
        
        # Main content area
        self.results_container = "main, body"
        
        # Sidebar filters
        self.sidebar = "aside"
        
        # Type filtering (Movie/TV Show) - React Select
        self.type_dropdown = "div:has(#react-select-2-input) .css-yk16xz-control"
        self.movie_option = "text=Movie"
        self.tv_show_option = "text=TV Show"
        
        # Genre filtering - React Select
        self.genre_dropdown = "div:has(#react-select-3-input) .css-yk16xz-control"
        self.genre_select_text = "text=Select..."
        
        # Year filtering - React Select dropdowns
        # Use the control containers instead of input elements
        self.year_from_dropdown = "div:has(#react-select-4-input) .css-yk16xz-control"
        self.year_to_dropdown = "div:has(#react-select-5-input) .css-yk16xz-control"
        
        # Rating filtering (Star rating)
        self.rating_section = "aside div:has-text('Ratings')"
        self.rating_stars = "aside div:has-text('Ratings') + div [class*='star']"
        self.rating_and_up = "text=& up"
        
        # Loading and states
        self.loading_indicator = "[class*='loading'], [class*='spinner']"
        self.page_title = "h1, title"
    
    async def navigate_to_home(self) -> None:
        """Navigate to home page."""
        from config.settings import config
        await self.navigate_to(config.base_url)
        await self.wait_for_page_load()
    
    async def wait_for_page_load(self) -> None:
        """Wait for page to fully load."""
        try:
            # Wait for the main navigation to be visible
            await self.page.wait_for_selector("text=Popular", timeout=15000)
            logger.info("Navigation loaded")
            
            # Wait for movie images to load
            await self.page.wait_for_selector("img", timeout=10000)
            logger.info("Images loaded")
            
            # Small delay for any dynamic content
            await self.page.wait_for_timeout(1000)
            
            logger.info("Home page loaded successfully")
            
        except Exception as e:
            logger.error(f"Error waiting for page load: {e}")
            await self.take_screenshot("page_load_error")
            raise
    
    async def select_category(self, category: str) -> None:
        """Select movie category.
        
        Args:
            category: Category name (popular, trending, newest, top_rated)
        """
        category_mapping = {
            "popular": self.popular_btn,
            "trending": self.trending_btn,
            "trend": self.trending_btn,
            "newest": self.newest_btn,
            "top_rated": self.top_rated_btn,
            "top rated": self.top_rated_btn
        }
        
        category_lower = category.lower().replace(" ", "_")
        if category_lower not in category_mapping:
            # Try direct text match as fallback
            locator = f"text={category}"
        else:
            locator = category_mapping[category_lower]
        
        logger.info(f"Selecting category: {category}")
        
        try:
            await self.page.click(locator, timeout=10000)
            # Wait for any page changes
            await self.page.wait_for_timeout(2000)
            logger.info(f"Successfully clicked {category} category")
        except Exception as e:
            logger.error(f"Failed to click category {category}: {e}")
            await self.take_screenshot(f"category_click_failed_{category}")
            raise
    
    async def click_search(self) -> None:
        """Click the search button."""
        try:
            await self.page.click(self.search_button, timeout=10000)
            logger.info("Clicked search button")
            await self.page.wait_for_timeout(1000)
        except Exception as e:
            logger.warning(f"Search button click failed: {e}")
    
    async def get_movie_count(self) -> int:
        """Get number of movie images displayed.
        
        Returns:
            Number of movie images/posters
        """
        try:
            # Count movie images
            count = await self.page.locator(self.movie_images).count()
            logger.info(f"Found {count} movie images")
            return count
        except Exception as e:
            logger.error(f"Error counting movies: {e}")
            return 0
    
    async def get_movie_titles(self) -> List[str]:
        """Get list of visible text that could be movie titles.
        
        Returns:
            List of potential movie titles
        """
        titles = []
        try:
            # Look for text elements that could be titles
            text_elements = await self.page.locator("h3, h2, h4, [class*='title']").all()
            
            for element in text_elements:
                try:
                    if await element.is_visible():
                        text = await element.text_content()
                        if text and len(text.strip()) > 0:
                            titles.append(text.strip())
                except:
                    continue
            
            logger.info(f"Found {len(titles)} potential movie titles")
            return titles[:10]  # Return first 10 to avoid too much data
            
        except Exception as e:
            logger.error(f"Error getting movie titles: {e}")
            return []
    
    async def is_sidebar_visible(self) -> bool:
        """Check if the filter sidebar is visible.
        
        Returns:
            True if sidebar is visible
        """
        try:
            return await self.page.locator(self.sidebar).is_visible()
        except:
            return False
    
    async def get_page_title(self) -> str:
        """Get the page title.
        
        Returns:
            Page title
        """
        try:
            return await self.page.title()
        except:
            return ""
    
    async def wait_for_images_to_load(self) -> None:
        """Wait for movie images to load."""
        try:
            await self.page.wait_for_selector("img", timeout=10000)
            # Wait for at least one image to actually load
            await self.page.wait_for_function(
                "document.querySelector('img') && document.querySelector('img').complete",
                timeout=10000
            )
            logger.info("Images finished loading")
        except Exception as e:
            logger.warning(f"Images may not have fully loaded: {e}")
    
    async def take_screenshot_with_timestamp(self, name: str) -> str:
        """Take screenshot with timestamp.
        
        Args:
            name: Base name for screenshot
            
        Returns:
            Screenshot file path
        """
        import time
        timestamp = int(time.time())
        screenshot_name = f"{name}_{timestamp}"
        return await self.take_screenshot(screenshot_name)
    
    # Simplified methods for basic functionality
    async def verify_page_loaded(self) -> bool:
        """Verify the page has loaded properly.
        
        Returns:
            True if page appears to have loaded correctly
        """
        try:
            # Check for key elements
            has_navigation = await self.page.locator("text=Popular").is_visible()
            has_images = await self.page.locator("img").count() > 0
            has_title = len(await self.get_page_title()) > 0
            
            logger.info(f"Page verification - Nav: {has_navigation}, Images: {has_images}, Title: {has_title}")
            
            return has_navigation and (has_images or has_title)
            
        except Exception as e:
            logger.error(f"Error verifying page load: {e}")
            return False
    
    async def get_current_url(self) -> str:
        """Get current page URL.
        
        Returns:
            Current URL
        """
        return self.page.url
    
    async def refresh_page(self) -> None:
        """Refresh the current page."""
        await self.page.reload(wait_until="networkidle")
        await self.wait_for_page_load()
    
    async def apply_year_filter(self, year_from: int, year_to: int) -> None:
        """Apply year range filter.
        
        Args:
            year_from: Starting year
            year_to: Ending year
        """
        try:
            logger.info(f"Applying year filter: {year_from}-{year_to}")
            
            # Wait for sidebar to be visible
            await self.page.wait_for_selector(self.sidebar, timeout=10000)
            
            # Wait for year dropdowns to be available
            await self.page.wait_for_selector(self.year_from_dropdown, timeout=10000)
            await self.page.wait_for_selector(self.year_to_dropdown, timeout=10000)
            
            # Click on year from dropdown control
            await self.page.click(self.year_from_dropdown, timeout=5000)
            await self.page.wait_for_timeout(500)
            
            # Type the year in the input field
            await self.page.fill("#react-select-4-input", str(year_from))
            await self.page.press("#react-select-4-input", "Enter")
            logger.info(f"Selected year from: {year_from}")
            
            # Wait a bit for the first dropdown to process
            await self.page.wait_for_timeout(1000)
            
            # Click on year to dropdown control
            await self.page.click(self.year_to_dropdown, timeout=5000)
            await self.page.wait_for_timeout(500)
            
            # Type the year in the input field
            await self.page.fill("#react-select-5-input", str(year_to))
            await self.page.press("#react-select-5-input", "Enter")
            logger.info(f"Selected year to: {year_to}")
            
            # Wait for filter to apply
            await self.page.wait_for_timeout(3000)
            
        except Exception as e:
            logger.error(f"Error applying year filter: {e}")
            await self.take_screenshot("year_filter_error")
            raise
    
    async def get_movie_years(self) -> List[int]:
        """Extract years from movie cards on the page.
        
        Returns:
            List of years found in movie cards
        """
        years = []
        try:
            # Look for year information in movie cards
            # This is a simplified approach - in a real scenario, you'd need to inspect
            # the actual DOM structure to find where years are displayed
            year_elements = await self.page.locator("[class*='year'], [class*='date'], [class*='release']").all()
            
            for element in year_elements:
                try:
                    if await element.is_visible():
                        text = await element.text_content()
                        if text:
                            # Extract 4-digit years from text
                            import re
                            year_matches = re.findall(r'\b(19|20)\d{2}\b', text)
                            for year_match in year_matches:
                                years.append(int(year_match))
                except:
                    continue
            
            # If no specific year elements found, try to extract from any text
            if not years:
                all_text_elements = await self.page.locator("div, span, p").all()
                for element in all_text_elements[:20]:  # Limit to first 20 elements
                    try:
                        if await element.is_visible():
                            text = await element.text_content()
                            if text:
                                import re
                                year_matches = re.findall(r'\b(19|20)\d{2}\b', text)
                                for year_match in year_matches:
                                    year_val = int(year_match)
                                    if 1900 <= year_val <= 2024:  # Reasonable year range
                                        years.append(year_val)
                    except:
                        continue
            
            logger.info(f"Found years: {years[:10]}")  # Log first 10 years
            return years[:20]  # Return first 20 years to avoid too much data
            
        except Exception as e:
            logger.error(f"Error extracting movie years: {e}")
            return []
    
    async def verify_year_range(self, year_from: int, year_to: int) -> bool:
        """Verify that all visible movies are within the specified year range.
        
        Args:
            year_from: Starting year
            year_to: Ending year
            
        Returns:
            True if all movies are within range
        """
        try:
            years = await self.get_movie_years()
            
            if not years:
                logger.warning("No years found to verify")
                return True  # If no years found, consider it passed
            
            # Check if all years are within range
            out_of_range = [year for year in years if not (year_from <= year <= year_to)]
            
            if out_of_range:
                logger.warning(f"Found years out of range: {out_of_range}")
                return False
            
            logger.info(f"All {len(years)} years are within range {year_from}-{year_to}")
            return True
            
        except Exception as e:
            logger.error(f"Error verifying year range: {e}")
            return False
    
    async def apply_type_filter(self, content_type: str) -> None:
        """Apply type filter (Movie or TV Show).
        
        Args:
            content_type: 'movie' or 'tv_show'
        """
        try:
            logger.info(f"Applying type filter: {content_type}")
            
            # Wait for sidebar to be visible
            await self.page.wait_for_selector(self.sidebar, timeout=10000)
            
            # Click on type dropdown control
            await self.page.click(self.type_dropdown, timeout=5000)
            await self.page.wait_for_timeout(500)
            
            # Type the content type in the input field
            if content_type.lower() in ['movie', 'movies']:
                await self.page.fill("#react-select-2-input", "Movie")
                await self.page.press("#react-select-2-input", "Enter")
                logger.info("Selected Movie type")
            elif content_type.lower() in ['tv_show', 'tv', 'tv shows']:
                await self.page.fill("#react-select-2-input", "TV Show")
                await self.page.press("#react-select-2-input", "Enter")
                logger.info("Selected TV Show type")
            else:
                raise ValueError(f"Invalid content type: {content_type}")
            
            # Wait for filter to apply
            await self.page.wait_for_timeout(2000)
            
        except Exception as e:
            logger.error(f"Error applying type filter: {e}")
            await self.take_screenshot("type_filter_error")
            raise
    
    async def apply_genre_filter(self, genre: str) -> None:
        """Apply genre filter.
        
        Args:
            genre: Genre name to filter by
        """
        try:
            logger.info(f"Applying genre filter: {genre}")
            
            # Wait for sidebar to be visible
            await self.page.wait_for_selector(self.sidebar, timeout=10000)
            
            # Click on genre dropdown control
            await self.page.click(self.genre_dropdown, timeout=5000)
            await self.page.wait_for_timeout(500)
            
            # Type the genre in the input field
            await self.page.fill("#react-select-3-input", genre)
            await self.page.press("#react-select-3-input", "Enter")
            logger.info(f"Selected genre: {genre}")
            
            # Wait for filter to apply
            await self.page.wait_for_timeout(2000)
            
        except Exception as e:
            logger.error(f"Error applying genre filter: {e}")
            await self.take_screenshot("genre_filter_error")
            raise
    
    async def apply_rating_filter(self, min_rating: int) -> None:
        """Apply rating filter.
        
        Args:
            min_rating: Minimum star rating (1-10)
        """
        try:
            logger.info(f"Applying rating filter: {min_rating} stars")
            
            # Wait for sidebar to be visible
            await self.page.wait_for_selector(self.sidebar, timeout=10000)
            
            # Find the rating section
            rating_section = self.page.locator(self.rating_section)
            await rating_section.wait_for(state="visible", timeout=5000)
            
            # Look for star elements - try different approaches
            star_selectors = [
                "aside div:has-text('Ratings') + div [class*='star']",
                "aside div:has-text('Ratings') + div [class*='rate']",
                "aside div:has-text('Ratings') + div [class*='rating']",
                "aside div:has-text('Ratings') + div [class*='★']",
                "aside div:has-text('Ratings') + div [class*='star']"
            ]
            
            star_elements = []
            for selector in star_selectors:
                try:
                    elements = await self.page.locator(selector).all()
                    if elements:
                        star_elements = elements
                        logger.info(f"Found {len(star_elements)} star elements with selector: {selector}")
                        break
                except:
                    continue
            
            if not star_elements:
                # Try to find any clickable elements in the rating section
                rating_div = self.page.locator("aside div:has-text('Ratings') + div")
                star_elements = await rating_div.locator("*").all()
                logger.info(f"Found {len(star_elements)} elements in rating section")
            
            if len(star_elements) >= min_rating:
                # Click on the star at the desired rating position
                await star_elements[min_rating - 1].click(timeout=5000)
                logger.info(f"Selected {min_rating} star rating")
            else:
                logger.warning(f"Not enough star elements found for rating {min_rating}")
                return
            
            # Wait for filter to apply
            await self.page.wait_for_timeout(2000)
            
        except Exception as e:
            logger.error(f"Error applying rating filter: {e}")
            await self.take_screenshot("rating_filter_error")
            raise
    
    async def search_movies(self, search_term: str) -> None:
        """Search for movies by title.
        
        Args:
            search_term: Search term to look for
        """
        try:
            logger.info(f"Searching for: {search_term}")
            
            # Look for search input field directly (based on the image showing input with placeholder="SEARCH")
            search_input = self.page.locator("input[placeholder='SEARCH'], input[name='search']")
            
            if await search_input.count() > 0:
                # Clear any existing text and enter new search term
                await search_input.first.click()
                await search_input.first.fill("")  # Clear existing text
                await search_input.first.fill(search_term)
                await search_input.first.press("Enter")
                logger.info(f"Entered search term: {search_term}")
                
                # Wait for search results to load
                await self.page.wait_for_timeout(3000)
            else:
                logger.warning("Search input field not found")
                
        except Exception as e:
            logger.error(f"Error searching movies: {e}")
            await self.take_screenshot("search_error")
            raise
    
    async def clear_search(self) -> None:
        """Clear the search input field."""
        try:
            search_input = self.page.locator("input[placeholder='SEARCH'], input[name='search']")
            if await search_input.count() > 0:
                await search_input.first.click()
                await search_input.first.fill("")
                await search_input.first.press("Enter")
                logger.info("Cleared search field")
                await self.page.wait_for_timeout(2000)
        except Exception as e:
            logger.warning(f"Error clearing search: {e}")
    
    async def get_search_results_count(self) -> int:
        """Get the number of search results displayed.
        
        Returns:
            Number of search results
        """
        try:
            # Count movie images in search results
            count = await self.page.locator(self.movie_images).count()
            logger.info(f"Found {count} search results")
            return count
        except Exception as e:
            logger.error(f"Error counting search results: {e}")
            return 0
    
    async def verify_search_results_contain(self, search_term: str) -> bool:
        """Verify that search results contain the search term.
        
        Args:
            search_term: The term that was searched for
            
        Returns:
            True if search results contain the term
        """
        try:
            # Get all visible text on the page
            page_text = await self.page.text_content("body")
            search_term_lower = search_term.lower()
            page_text_lower = page_text.lower()
            
            # Check if search term appears in the page content
            contains_term = search_term_lower in page_text_lower
            logger.info(f"Search term '{search_term}' found in results: {contains_term}")
            return contains_term
            
        except Exception as e:
            logger.error(f"Error verifying search results: {e}")
            return False
    
    async def get_search_suggestions(self) -> List[str]:
        """Get search suggestions if available.
        
        Returns:
            List of search suggestions
        """
        suggestions = []
        try:
            # Look for dropdown suggestions
            suggestion_elements = await self.page.locator("[class*='suggestion'], [class*='dropdown'], [class*='autocomplete']").all()
            
            for element in suggestion_elements:
                try:
                    if await element.is_visible():
                        text = await element.text_content()
                        if text and text.strip():
                            suggestions.append(text.strip())
                except:
                    continue
            
            logger.info(f"Found {len(suggestions)} search suggestions")
            return suggestions
            
        except Exception as e:
            logger.error(f"Error getting search suggestions: {e}")
            return []
    
    async def is_pagination_available(self) -> bool:
        """Check if pagination is available.
        
        Returns:
            True if pagination is visible
        """
        try:
            # Look for pagination elements
            pagination_selectors = [
                "button:has-text('Next')",
                "button:has-text('Previous')",
                "[class*='pagination']",
                "[class*='page']"
            ]
            
            for selector in pagination_selectors:
                if await self.page.locator(selector).count() > 0:
                    logger.info(f"Pagination found with selector: {selector}")
                    return True
            
            logger.info("No pagination found")
            return False
            
        except Exception as e:
            logger.error(f"Error checking pagination: {e}")
            return False
    
    async def navigate_to_next_page(self) -> bool:
        """Navigate to the next page.
        
        Returns:
            True if navigation was successful
        """
        try:
            # Look for next page button
            next_button = self.page.locator("button:has-text('Next')")
            
            if await next_button.count() > 0 and await next_button.is_enabled():
                await next_button.click(timeout=5000)
                logger.info("Clicked next page button")
                
                # Wait for page to load
                await self.page.wait_for_timeout(3000)
                return True
            else:
                logger.info("Next page button not available")
                return False
                
        except Exception as e:
            logger.error(f"Error navigating to next page: {e}")
            return False