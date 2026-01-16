import importlib
import types

import pytest

import utils
from fake import FakeUserAgent
from errors import FakeUserAgentError


def test_parse_json_lines_accepts_json_object_line():
    data = '{"chrome": ["ua1", "ua2"], "firefox": ["ua3"]}\n'
    parsed = utils.parse_json_lines(data.splitlines())
    assert parsed["chrome"] == ["ua1", "ua2"]
    assert parsed["firefox"] == ["ua3"]


def test_parse_json_lines_requires_lists_of_strings():
    bad_line = '{"chrome": [123]}\n'
    with pytest.raises(FakeUserAgentError):
        utils.parse_json_lines(bad_line.splitlines())


def test_load_bundled_browsers_reads_package_resource():
    # ensure the data package is importable
    data_pkg = importlib.import_module("data")
    assert isinstance(data_pkg, types.ModuleType)

    bundled = utils.load_bundled_browsers()
    assert isinstance(bundled, dict)
    assert "chrome" in bundled  # dataset shipped with at least chrome
    assert isinstance(bundled["chrome"], list)
    assert len(bundled["chrome"]) > 0

    # subset_browsers with None returns all
    all_data = utils.subset_browsers(bundled, None)
    assert all_data == bundled


def test_fake_useragent_defaults_to_bundled_data_offline(monkeypatch):
    # If a network call would occur, force it to explode
    def boom(*args, **kwargs):  # pragma: no cover - we don't expect this
        raise AssertionError("Network access attempted")

    monkeypatch.setattr(utils, "get", boom)
    monkeypatch.setattr(utils, "get_browser_user_agents", boom)

    ua = FakeUserAgent()
    # Should be able to fetch a chrome UA from bundled data
    assert isinstance(ua.chrome, str)
    # Random should also work
    assert isinstance(ua.random, str)


def test_missing_browser_raises_error():
    with pytest.raises(FakeUserAgentError):
        FakeUserAgent(browsers=["nonexistent-browser"])


def test_missing_browser_with_fallback_returns_fallback():
    ua = FakeUserAgent(browsers=["nonexistent-browser"], fallback="fallback-ua")
    assert ua.random == "fallback-ua"
