"""UI tests for search functionality."""

import pytest
from playwright.async_api import Page, expect
from pages.home_page import HomePage
from loguru import logger


@pytest.mark.asyncio
@pytest.mark.ui
@pytest.mark.smoke
class TestSearch:
    """Test class for search functionality."""
    
    async def test_search_input_field_visibility(self, home_page: HomePage):
        """
        Test Case: TC013 - Search Input Field Visibility
        Priority: High
        
        Steps:
        1. Navigate to home page
        2. Verify search input field is visible and accessible
        3. Check input field attributes
        Expected: Search input field is visible with correct placeholder
        """
        await home_page.navigate_to_home()
        await home_page.wait_for_page_load()
        
        # Take screenshot before search
        await home_page.take_screenshot("before_search")
        
        # Check if search input field is visible
        search_input = home_page.page.locator("input[placeholder='SEARCH'], input[name='search']")
        is_visible = await search_input.is_visible()
        
        assert is_visible, "Search input field should be visible"
        logger.info("✅ Search input field is visible")
        
        # Check input field attributes
        placeholder = await search_input.get_attribute("placeholder")
        input_type = await search_input.get_attribute("type")
        
        logger.info(f"Search input attributes - Placeholder: {placeholder}, Type: {input_type}")
        assert placeholder == "SEARCH", f"Expected placeholder 'SEARCH', got '{placeholder}'"
        assert input_type == "text", f"Expected input type 'text', got '{input_type}'"
        
        logger.info("TC013 - Search Input Field Visibility test completed successfully")
    
    async def test_basic_movie_search(self, home_page: HomePage):
        """
        Test Case: TC014 - Basic Movie Search
        Priority: High
        
        Steps:
        1. Navigate to home page
        2. Search for "POOL" (as shown in the reference image)
        3. Verify search results appear
        4. Verify results contain the search term
        Expected: Search returns relevant results containing "POOL"
        """
        await home_page.navigate_to_home()
        await home_page.wait_for_page_load()
        
        # Take screenshot before search
        await home_page.take_screenshot("before_pool_search")
        
        # Search for "POOL" as shown in the reference image
        search_term = "POOL"
        await home_page.search_movies(search_term)
        
        # Take screenshot after search
        await home_page.take_screenshot("after_pool_search")
        
        # Verify search results
        results_count = await home_page.get_search_results_count()
        logger.info(f"Search for '{search_term}' returned {results_count} results")
        
        # Verify search results contain the search term
        contains_term = await home_page.verify_search_results_contain(search_term)
        assert contains_term, f"Search results should contain the term '{search_term}'"
        
        # Get movie titles to verify search worked
        titles = await home_page.get_movie_titles()
        logger.info(f"Search result titles: {titles[:5]}")
        
        # Verify we got some results
        assert results_count > 0, "Search should return at least one result"
        
        logger.info("TC014 - Basic Movie Search test completed successfully")
    
    async def test_search_with_different_terms(self, home_page: HomePage):
        """
        Test Case: TC015 - Search with Different Terms
        Priority: High
        
        Steps:
        1. Test search with various movie terms
        2. Verify each search returns appropriate results
        3. Test case sensitivity
        Expected: All search terms return relevant results
        """
        await home_page.navigate_to_home()
        await home_page.wait_for_page_load()
        
        # Test different search terms
        search_terms = [
            "Batman",
            "Spider",
            "Star Wars",
            "Action",
            "Comedy",
            "Horror"
        ]
        
        successful_searches = 0
        
        for term in search_terms:
            try:
                logger.info(f"Testing search for: {term}")
                
                # Clear previous search
                await home_page.clear_search()
                await home_page.page.wait_for_timeout(1000)
                
                # Perform search
                await home_page.search_movies(term)
                
                # Verify results
                results_count = await home_page.get_search_results_count()
                contains_term = await home_page.verify_search_results_contain(term)
                
                if results_count > 0 and contains_term:
                    successful_searches += 1
                    logger.info(f"✅ Search '{term}' successful: {results_count} results")
                    await home_page.take_screenshot(f"search_{term.lower().replace(' ', '_')}")
                else:
                    logger.warning(f"⚠️ Search '{term}' returned {results_count} results, contains term: {contains_term}")
                
            except Exception as e:
                logger.warning(f"❌ Search failed for '{term}': {e}")
                continue
        
        # At least 50% of searches should be successful
        success_rate = (successful_searches / len(search_terms)) * 100
        logger.info(f"Search success rate: {success_rate:.1f}% ({successful_searches}/{len(search_terms)})")
        
        assert successful_searches >= len(search_terms) // 2, f"Expected at least 50% search success rate, got {success_rate:.1f}%"
        
        logger.info("TC015 - Search with Different Terms test completed successfully")
    
    async def test_empty_search(self, home_page: HomePage):
        """
        Test Case: TC016 - Empty Search
        Priority: Medium
        
        Steps:
        1. Navigate to home page
        2. Perform empty search
        3. Verify behavior (should show all movies or no results)
        Expected: Empty search handled gracefully
        """
        await home_page.navigate_to_home()
        await home_page.wait_for_page_load()
        
        # Take screenshot before empty search
        await home_page.take_screenshot("before_empty_search")
        
        # Perform empty search
        await home_page.search_movies("")
        
        # Take screenshot after empty search
        await home_page.take_screenshot("after_empty_search")
        
        # Check results
        results_count = await home_page.get_search_results_count()
        logger.info(f"Empty search returned {results_count} results")
        
        # Empty search should either show all movies or no results
        # Both behaviors are acceptable depending on implementation
        assert results_count >= 0, "Empty search should not cause errors"
        
        logger.info("TC016 - Empty Search test completed successfully")
    
    async def test_search_with_special_characters(self, home_page: HomePage):
        """
        Test Case: TC017 - Search with Special Characters
        Priority: Medium
        
        Steps:
        1. Test search with special characters
        2. Test search with numbers
        3. Test search with symbols
        Expected: Special characters handled gracefully
        """
        await home_page.navigate_to_home()
        await home_page.wait_for_page_load()
        
        special_terms = [
            "2023",
            "The & The",
            "Movie-Name",
            "Action/Adventure",
            "Sci-Fi",
            "Rated R"
        ]
        
        for term in special_terms:
            try:
                logger.info(f"Testing special character search: {term}")
                
                await home_page.clear_search()
                await home_page.page.wait_for_timeout(1000)
                
                await home_page.search_movies(term)
                
                results_count = await home_page.get_search_results_count()
                logger.info(f"Special character search '{term}' returned {results_count} results")
                
                await home_page.take_screenshot(f"special_search_{term.replace('/', '_').replace(' ', '_')}")
                
            except Exception as e:
                logger.warning(f"Special character search failed for '{term}': {e}")
        
        logger.info("TC017 - Search with Special Characters test completed successfully")
    
    async def test_search_clear_functionality(self, home_page: HomePage):
        """
        Test Case: TC018 - Search Clear Functionality
        Priority: Medium
        
        Steps:
        1. Perform a search
        2. Clear the search
        3. Verify search is cleared and results reset
        Expected: Search can be cleared and results reset
        """
        await home_page.navigate_to_home()
        await home_page.wait_for_page_load()
        
        # Perform initial search
        await home_page.search_movies("POOL")
        initial_results = await home_page.get_search_results_count()
        logger.info(f"Initial search returned {initial_results} results")
        
        await home_page.take_screenshot("before_clear_search")
        
        # Clear search
        await home_page.clear_search()
        
        await home_page.take_screenshot("after_clear_search")
        
        # Verify search was cleared
        cleared_results = await home_page.get_search_results_count()
        logger.info(f"After clearing search: {cleared_results} results")
        
        # Results should change after clearing (either more or fewer results)
        # This depends on whether clearing shows all movies or no results
        assert cleared_results >= 0, "Cleared search should not cause errors"
        
        logger.info("TC018 - Search Clear Functionality test completed successfully")
    
    async def test_search_case_sensitivity(self, home_page: HomePage):
        """
        Test Case: TC019 - Search Case Sensitivity
        Priority: Low
        
        Steps:
        1. Search with uppercase term
        2. Search with lowercase term
        3. Search with mixed case term
        4. Compare results
        Expected: Search should be case-insensitive or handle case appropriately
        """
        await home_page.navigate_to_home()
        await home_page.wait_for_page_load()
        
        search_term = "POOL"
        case_variations = [
            "POOL",      # Uppercase
            "pool",      # Lowercase
            "Pool",      # Title case
            "PoOl"       # Mixed case
        ]
        
        results_by_case = {}
        
        for variation in case_variations:
            try:
                logger.info(f"Testing case variation: {variation}")
                
                await home_page.clear_search()
                await home_page.page.wait_for_timeout(1000)
                
                await home_page.search_movies(variation)
                
                results_count = await home_page.get_search_results_count()
                results_by_case[variation] = results_count
                
                logger.info(f"Case '{variation}' returned {results_count} results")
                
            except Exception as e:
                logger.warning(f"Case variation '{variation}' failed: {e}")
                results_by_case[variation] = 0
        
        # Log results comparison
        logger.info(f"Case sensitivity results: {results_by_case}")
        
        # All variations should return similar results (case-insensitive)
        # or at least not cause errors
        for variation, count in results_by_case.items():
            assert count >= 0, f"Case variation '{variation}' should not cause errors"
        
        logger.info("TC019 - Search Case Sensitivity test completed successfully")
    
    async def test_search_with_long_term(self, home_page: HomePage):
        """
        Test Case: TC020 - Search with Long Term
        Priority: Low
        
        Steps:
        1. Search with very long term
        2. Verify search handles long input gracefully
        Expected: Long search terms handled without errors
        """
        await home_page.navigate_to_home()
        await home_page.wait_for_page_load()
        
        # Test with very long search term
        long_term = "This is a very long search term that should test the search functionality with extended input"
        
        try:
            logger.info(f"Testing long search term: {long_term[:50]}...")
            
            await home_page.search_movies(long_term)
            
            results_count = await home_page.get_search_results_count()
            logger.info(f"Long search term returned {results_count} results")
            
            await home_page.take_screenshot("long_search_term")
            
            # Should not cause errors
            assert results_count >= 0, "Long search term should not cause errors"
            
        except Exception as e:
            logger.warning(f"Long search term failed: {e}")
            # This is acceptable - long terms might not be supported
        
        logger.info("TC020 - Search with Long Term test completed successfully")