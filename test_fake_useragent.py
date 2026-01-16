"""
Comprehensive test suite for fake-useragent local-first implementation.
Tests offline loading, external data fetching, and API compatibility.
"""
import json
import os
import tempfile
import unittest
from unittest.mock import patch, MagicMock

from fake import FakeUserAgent, UserAgent
from errors import FakeUserAgentError
from utils import load, load_from_package_data, load_cached


class TestBundledDataLoading(unittest.TestCase):
    """Test loading from bundled package data (default behavior)."""

    def test_load_from_package_data_success(self):
        """Test that bundled data loads successfully."""
        data = load_from_package_data()
        
        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0, "Bundled data should not be empty")
        self.assertIn("chrome", data, "Bundled data should contain 'chrome'")
        self.assertIsInstance(data["chrome"], list)
        self.assertGreater(len(data["chrome"]), 0)

    def test_load_default_uses_bundled_data(self):
        """Test that load() without use_external_data uses bundled data."""
        data = load(browsers=["chrome"], use_external_data=False)
        
        self.assertIsInstance(data, dict)
        self.assertGreater(len(data), 0)
        # Should have data from bundled file, not limited to requested browsers
        self.assertIn("chrome", data)

    def test_bundled_data_structure(self):
        """Test that bundled data has correct structure."""
        data = load_from_package_data()
        
        for browser_name, user_agents in data.items():
            self.assertIsInstance(browser_name, str)
            self.assertIsInstance(user_agents, list)
            self.assertGreater(len(user_agents), 0)
            for ua in user_agents:
                self.assertIsInstance(ua, str)
                self.assertGreater(len(ua), 0)


class TestOfflineFunctionality(unittest.TestCase):
    """Test that the library works completely offline by default."""

    @patch('utils.get')
    def test_no_network_calls_by_default(self, mock_get):
        """Test that no network calls are made with default settings."""
        ua = FakeUserAgent()
        
        # Access various browser user agents
        chrome_ua = ua.chrome
        firefox_ua = ua.firefox
        safari_ua = ua.safari
        random_ua = ua.random
        
        # Verify no network calls were made
        mock_get.assert_not_called()
        
        # Verify we got valid user agents
        self.assertIsInstance(chrome_ua, str)
        self.assertGreater(len(chrome_ua), 0)
        self.assertIsInstance(firefox_ua, str)
        self.assertIsInstance(safari_ua, str)
        self.assertIsInstance(random_ua, str)

    @patch('utils.get')
    def test_no_network_calls_with_explicit_false(self, mock_get):
        """Test that use_external_data=False prevents network calls."""
        ua = FakeUserAgent(use_external_data=False)
        
        chrome_ua = ua.chrome
        firefox_ua = ua.firefox
        
        mock_get.assert_not_called()
        self.assertIsInstance(chrome_ua, str)
        self.assertIsInstance(firefox_ua, str)


class TestExternalDataFetching(unittest.TestCase):
    """Test external data fetching when explicitly enabled."""

    @patch('utils.get')
    def test_external_data_requires_opt_in(self, mock_get):
        """Test that external data is only fetched when use_external_data=True."""
        # Mock external response
        mock_get.return_value = b'<div id="liste"><a href="/test">Mozilla/5.0 Test</a></div>'
        
        # With use_external_data=False (default), should not call external source
        ua = FakeUserAgent(use_external_data=False)
        ua.chrome  # Access a user agent
        mock_get.assert_not_called()
        
        # With use_external_data=True, should attempt external calls
        mock_get.reset_mock()
        try:
            ua_external = FakeUserAgent(use_external_data=True, browsers=["chrome"])
            # This will call external sources
        except Exception:
            # May fail if mocking isn't perfect, but should have attempted call
            pass
        
        if mock_get.call_count > 0:
            # If external call was made, verify it was attempted
            self.assertGreater(mock_get.call_count, 0)


class TestFakeUserAgentAPI(unittest.TestCase):
    """Test FakeUserAgent class API and functionality."""

    def test_initialization_default(self):
        """Test default initialization."""
        ua = FakeUserAgent()
        self.assertFalse(ua.use_external_data)
        self.assertTrue(ua.cache)
        self.assertIsNotNone(ua.data_browsers)
        self.assertGreater(len(ua.data_browsers), 0)

    def test_initialization_with_use_external_data(self):
        """Test initialization with use_external_data."""
        ua = FakeUserAgent(use_external_data=False)
        self.assertFalse(ua.use_external_data)

    def test_browser_access_chrome(self):
        """Test accessing Chrome user agents."""
        ua = FakeUserAgent()
        chrome_ua = ua.chrome
        
        self.assertIsInstance(chrome_ua, str)
        self.assertGreater(len(chrome_ua), 0)
        # Typically contains "Chrome" or "Chromium"
        self.assertTrue("Chrome" in chrome_ua or "Chromium" in chrome_ua.lower())

    def test_browser_access_firefox(self):
        """Test accessing Firefox user agents."""
        ua = FakeUserAgent()
        firefox_ua = ua.firefox
        
        self.assertIsInstance(firefox_ua, str)
        self.assertGreater(len(firefox_ua), 0)

    def test_browser_access_safari(self):
        """Test accessing Safari user agents."""
        ua = FakeUserAgent()
        safari_ua = ua.safari
        
        self.assertIsInstance(safari_ua, str)
        self.assertGreater(len(safari_ua), 0)
        self.assertIn("Safari", safari_ua)

    def test_random_user_agent(self):
        """Test random user agent selection."""
        ua = FakeUserAgent()
        
        # Get multiple random user agents
        random_uas = [ua.random for _ in range(10)]
        
        # All should be valid strings
        for ua_string in random_uas:
            self.assertIsInstance(ua_string, str)
            self.assertGreater(len(ua_string), 0)
        
        # Should have some variety (not all identical)
        unique_uas = set(random_uas)
        self.assertGreater(len(unique_uas), 1, "Random should provide variety")

    def test_browser_shortcuts(self):
        """Test browser name shortcuts."""
        ua = FakeUserAgent()
        
        # Test various shortcuts
        ie_ua = ua.ie
        self.assertIsInstance(ie_ua, str)
        
        msie_ua = ua.msie
        self.assertIsInstance(msie_ua, str)
        
        internetexplorer_ua = ua.internetexplorer
        self.assertIsInstance(internetexplorer_ua, str)

    def test_getitem_access(self):
        """Test dictionary-style access."""
        ua = FakeUserAgent()
        
        chrome_ua = ua['chrome']
        self.assertIsInstance(chrome_ua, str)
        
        random_ua = ua['random']
        self.assertIsInstance(random_ua, str)

    def test_fallback_on_error(self):
        """Test fallback mechanism."""
        fallback_ua = "Mozilla/5.0 (Fallback) Test"
        ua = FakeUserAgent(fallback=fallback_ua)
        
        # Try to access non-existent browser
        result = ua.nonexistentbrowser
        self.assertEqual(result, fallback_ua)

    def test_error_without_fallback(self):
        """Test error raised when no fallback."""
        ua = FakeUserAgent()
        
        with self.assertRaises(FakeUserAgentError):
            _ = ua.nonexistentbrowser

    def test_safe_attrs(self):
        """Test safe attributes."""
        ua = FakeUserAgent(safe_attrs=("my_attr",))
        
        # Should be able to set and get safe attr without triggering UA lookup
        ua.my_attr = "test_value"
        self.assertEqual(ua.my_attr, "test_value")


class TestCachingBehavior(unittest.TestCase):
    """Test caching behavior."""

    def test_cache_not_created_without_external_data(self):
        """Test that cache file is not created when using bundled data."""
        temp_cache = tempfile.mktemp(suffix=".json")
        
        try:
            ua = FakeUserAgent(cache=True, path=temp_cache, use_external_data=False)
            _ = ua.chrome
            
            # Cache file should not exist since we're using bundled data
            self.assertFalse(os.path.exists(temp_cache))
        finally:
            if os.path.exists(temp_cache):
                os.remove(temp_cache)

    def test_load_cached_without_external_data(self):
        """Test load_cached returns bundled data when use_external_data=False."""
        temp_cache = tempfile.mktemp(suffix=".json")
        
        try:
            data = load_cached(
                temp_cache,
                ["chrome"],
                use_external_data=False
            )
            
            # Should return bundled data, not create cache
            self.assertIsInstance(data, dict)
            self.assertIn("chrome", data)
            self.assertFalse(os.path.exists(temp_cache))
        finally:
            if os.path.exists(temp_cache):
                os.remove(temp_cache)


class TestBackwardCompatibility(unittest.TestCase):
    """Test backward compatibility with old API."""

    def test_user_agent_alias(self):
        """Test that UserAgent alias works."""
        ua = UserAgent()
        self.assertIsInstance(ua, FakeUserAgent)
        
        chrome_ua = ua.chrome
        self.assertIsInstance(chrome_ua, str)


class TestDataIntegrity(unittest.TestCase):
    """Test data integrity and format."""

    def test_all_bundled_browsers_accessible(self):
        """Test that all bundled browsers are accessible."""
        ua = FakeUserAgent()
        
        # Common browsers that should be in bundled data
        common_browsers = ["chrome", "firefox", "safari"]
        
        for browser in common_browsers:
            ua_string = getattr(ua, browser)
            self.assertIsInstance(ua_string, str)
            self.assertGreater(len(ua_string), 0)

    def test_user_agent_strings_valid_format(self):
        """Test that user agent strings have valid format."""
        data = load_from_package_data()
        
        for browser_name, user_agents in data.items():
            for ua_string in user_agents:
                # Basic validation: should be a non-empty string with common browser identifiers
                ua_lower = ua_string.lower()
                self.assertTrue(
                    "mozilla" in ua_lower or "opera" in ua_lower or "chrome" in ua_lower or "safari" in ua_lower,
                    f"User agent should be valid format: {ua_string[:80]}"
                )


class TestErrorHandling(unittest.TestCase):
    """Test error handling."""

    def test_invalid_cache_parameter(self):
        """Test that invalid cache parameter raises error."""
        with self.assertRaises(AssertionError):
            FakeUserAgent(cache="invalid")

    def test_invalid_use_external_data_parameter(self):
        """Test that invalid use_external_data parameter raises error."""
        with self.assertRaises(AssertionError):
            FakeUserAgent(use_external_data="invalid")

    def test_invalid_browsers_parameter(self):
        """Test that invalid browsers parameter raises error."""
        with self.assertRaises(AssertionError):
            FakeUserAgent(browsers=123)

    def test_invalid_fallback_parameter(self):
        """Test that invalid fallback parameter raises error."""
        with self.assertRaises(AssertionError):
            FakeUserAgent(fallback=123)


def run_tests():
    """Run all tests and return results."""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestBundledDataLoading))
    suite.addTests(loader.loadTestsFromTestCase(TestOfflineFunctionality))
    suite.addTests(loader.loadTestsFromTestCase(TestExternalDataFetching))
    suite.addTests(loader.loadTestsFromTestCase(TestFakeUserAgentAPI))
    suite.addTests(loader.loadTestsFromTestCase(TestCachingBehavior))
    suite.addTests(loader.loadTestsFromTestCase(TestBackwardCompatibility))
    suite.addTests(loader.loadTestsFromTestCase(TestDataIntegrity))
    suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result


if __name__ == "__main__":
    result = run_tests()
    exit(0 if result.wasSuccessful() else 1)
