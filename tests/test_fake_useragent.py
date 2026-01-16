import pathlib
import sys
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import fake
import utils
from errors import FakeUserAgentError


class FakeUserAgentTests(unittest.TestCase):
    def test_bundled_data_used_by_default(self):
        with patch("utils.get_browser_user_agents") as external_fetch:
            agent = fake.FakeUserAgent()
            self.assertIn("chrome", agent.data_browsers)
            external_fetch.assert_not_called()

    def test_external_fetch_requires_opt_in(self):
        with patch("utils.load_bundled_data", side_effect=FakeUserAgentError("missing")):
            with self.assertRaises(FakeUserAgentError):
                fake.FakeUserAgent()

    def test_external_fetch_used_when_enabled(self):
        with patch("utils.load_bundled_data", side_effect=FakeUserAgentError("missing")):
            with patch("utils.get_browser_user_agents", return_value=["ua-value"]) as external_fetch:
                agent = fake.FakeUserAgent(use_external_data=True, browsers=["testbrowser"])
                self.assertEqual(agent.data_browsers["testbrowser"], ["ua-value"])
                external_fetch.assert_called_once_with("testbrowser", verify_ssl=True)


class UtilsLoadTests(unittest.TestCase):
    def test_load_returns_bundled_json_lines(self):
        data = utils.load(["chrome"], use_external_data=False)
        self.assertIn("chrome", data)
        self.assertIsInstance(data["chrome"], list)


if __name__ == "__main__":
    unittest.main()
