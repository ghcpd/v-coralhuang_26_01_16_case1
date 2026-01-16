import utils
from fake import FakeUserAgent


def test_external_fetch_called_only_when_opt_in(monkeypatch):
    called = {}

    def fake_get_browser_user_agents(browser, *, verify_ssl=True):
        called["browser"] = browser
        called["verify_ssl"] = verify_ssl
        return ["ua-external-1", "ua-external-2"]

    # Ensure bundled loader fails to force external path
    def fail_bundled():
        raise utils.FakeUserAgentError("force external")

    monkeypatch.setattr(utils, "load_bundled_browsers", fail_bundled)
    monkeypatch.setattr(utils, "get_browser_user_agents", fake_get_browser_user_agents)

    ua = FakeUserAgent(use_external_data=True, browsers=["chrome"], verify_ssl=False)
    assert ua.chrome in ["ua-external-1", "ua-external-2"]
    assert called["browser"] == "chrome"
    assert called["verify_ssl"] is False


def test_external_not_called_by_default(monkeypatch):
    def fail_external(*args, **kwargs):  # pragma: no cover - shouldn't be called
        raise AssertionError("External loader should not be invoked")

    monkeypatch.setattr(utils, "get_browser_user_agents", fail_external)
    # Should succeed via bundled data
    ua = FakeUserAgent()
    assert isinstance(ua.chrome, str)
