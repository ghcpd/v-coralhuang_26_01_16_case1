import sys
import unittest
from unittest.mock import patch, MagicMock

sys.path.insert(0, '.')

from fake import UserAgent, FakeUserAgent
from utils import load, load_local_data, str_types
from errors import FakeUserAgentError


class TestLocalDataLoading(unittest.TestCase):
    
    def test_load_local_data_returns_dict(self):
        data = load_local_data()
        self.assertIsInstance(data, dict)
    
    def test_load_local_data_has_browsers(self):
        data = load_local_data()
        self.assertIn("chrome", data)
    
    def test_load_local_data_browsers_have_user_agents(self):
        data = load_local_data()
        for browser, user_agents in data.items():
            self.assertIsInstance(user_agents, list)
            self.assertGreater(len(user_agents), 0)
            for ua in user_agents:
                self.assertIsInstance(ua, str)
    
    def test_default_load_uses_local_data(self):
        data = load(use_external_data=False)
        self.assertIsInstance(data, dict)
        self.assertIn("chrome", data)
    
    def test_user_agent_initialization_offline(self):
        ua = UserAgent()
        self.assertIsInstance(ua.data_browsers, dict)
        self.assertGreater(len(ua.data_browsers), 0)


class TestNoNetworkByDefault(unittest.TestCase):
    
    @patch('utils.urlopen')
    def test_load_default_no_urlopen(self, mock_urlopen):
        load(use_external_data=False)
        mock_urlopen.assert_not_called()
    
    @patch('utils.urlopen')
    def test_user_agent_default_no_urlopen(self, mock_urlopen):
        ua = UserAgent()
        mock_urlopen.assert_not_called()
    
    @patch('utils.urlopen')
    def test_user_agent_get_chrome_no_urlopen(self, mock_urlopen):
        ua = UserAgent()
        _ = ua.chrome
        mock_urlopen.assert_not_called()
    
    @patch('utils.urlopen')
    def test_user_agent_get_random_no_urlopen(self, mock_urlopen):
        ua = UserAgent()
        _ = ua.random
        mock_urlopen.assert_not_called()
    
    @patch('utils.urlopen')
    def test_refresh_no_urlopen(self, mock_urlopen):
        ua = UserAgent()
        ua.refresh()
        mock_urlopen.assert_not_called()


class TestExternalDataFetching(unittest.TestCase):
    
    @patch('utils.urlopen')
    def test_load_external_calls_urlopen(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Network disabled for test")
        with self.assertRaises(FakeUserAgentError):
            load(use_external_data=True)
        mock_urlopen.assert_called()
    
    @patch('utils.urlopen')
    def test_user_agent_external_calls_urlopen(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Network disabled for test")
        with self.assertRaises(FakeUserAgentError):
            UserAgent(use_external_data=True)
        mock_urlopen.assert_called()


class TestUserAgentFunctionality(unittest.TestCase):
    
    def setUp(self):
        self.ua = UserAgent()
    
    def test_chrome_returns_string(self):
        result = self.ua.chrome
        self.assertIsInstance(result, str)
        self.assertIn("Chrome", result)
    
    def test_firefox_returns_string(self):
        result = self.ua.firefox
        self.assertIsInstance(result, str)
        self.assertIn("Firefox", result)
    
    def test_random_returns_string(self):
        result = self.ua.random
        self.assertIsInstance(result, str)
        self.assertGreater(len(result), 0)
    
    def test_item_access(self):
        result = self.ua["chrome"]
        self.assertIsInstance(result, str)
        self.assertIn("Chrome", result)
    
    def test_fallback_on_missing_browser(self):
        fallback = "Mozilla/5.0 Fallback"
        ua = UserAgent(fallback=fallback)
        result = ua.nonexistent_browser_xyz
        self.assertEqual(result, fallback)
    
    def test_error_on_missing_browser_without_fallback(self):
        ua = UserAgent(fallback=None)
        with self.assertRaises(FakeUserAgentError):
            _ = ua.nonexistent_browser_xyz
    
    def test_shortcuts_work(self):
        result = self.ua.ff
        self.assertIsInstance(result, str)
        result = self.ua.google
        self.assertIsInstance(result, str)


class TestAPIParameters(unittest.TestCase):
    
    def test_use_external_data_must_be_bool(self):
        with self.assertRaises(AssertionError):
            UserAgent(use_external_data="yes")
    
    def test_fallback_must_be_string_or_none(self):
        with self.assertRaises(AssertionError):
            UserAgent(fallback=123)
    
    def test_browsers_must_be_list_or_string(self):
        with self.assertRaises(AssertionError):
            UserAgent(browsers=123)
    
    def test_verify_ssl_must_be_bool(self):
        with self.assertRaises(AssertionError):
            UserAgent(verify_ssl="yes")
    
    def test_safe_attrs_must_be_sequence(self):
        with self.assertRaises(AssertionError):
            UserAgent(safe_attrs="invalid")


class TestBackwardsCompatibility(unittest.TestCase):
    
    def test_user_agent_alias_exists(self):
        from fake import UserAgent
        self.assertTrue(callable(UserAgent))
    
    def test_fake_user_agent_exists(self):
        from fake import FakeUserAgent
        self.assertTrue(callable(FakeUserAgent))
    
    def test_user_agent_is_fake_user_agent(self):
        from fake import UserAgent, FakeUserAgent
        self.assertIs(UserAgent, FakeUserAgent)


class TestStrTypes(unittest.TestCase):
    
    def test_str_types_is_tuple(self):
        self.assertIsInstance(str_types, tuple)
    
    def test_str_types_contains_str(self):
        self.assertIn(str, str_types)


class TestDataIntegrity(unittest.TestCase):
    
    def test_bundled_data_not_empty(self):
        data = load_local_data()
        self.assertGreater(len(data), 0)
    
    def test_all_browsers_have_valid_user_agents(self):
        data = load_local_data()
        for browser, user_agents in data.items():
            for ua_string in user_agents:
                self.assertTrue(len(ua_string) > 0)


def run_tests():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestLocalDataLoading))
    suite.addTests(loader.loadTestsFromTestCase(TestNoNetworkByDefault))
    suite.addTests(loader.loadTestsFromTestCase(TestExternalDataFetching))
    suite.addTests(loader.loadTestsFromTestCase(TestUserAgentFunctionality))
    suite.addTests(loader.loadTestsFromTestCase(TestAPIParameters))
    suite.addTests(loader.loadTestsFromTestCase(TestBackwardsCompatibility))
    suite.addTests(loader.loadTestsFromTestCase(TestStrTypes))
    suite.addTests(loader.loadTestsFromTestCase(TestDataIntegrity))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(run_tests())
