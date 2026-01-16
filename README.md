# fake-useragent (local-first)

This package now ships a pre-generated user-agent dataset to work fully offline by default.

## Default behavior
- Loads user-agent strings from the bundled dataset at `data/browsers.json` via `importlib.resources`.
- No network or cache-server calls are performed unless explicitly enabled.
- The bundled file is formatted as JSON Lines (one JSON object per line mapping a browser name to a list of user agents).

## Enabling external fetching (opt-in)
Set `use_external_data=True` to allow network access when bundled data is missing:

```python
from fake import FakeUserAgent

agent = FakeUserAgent(use_external_data=True)
print(agent.chrome)
```

## Migration notes
- Deprecated parameters `cache` and `use_cache_server` were removed; use `use_external_data` instead.
- Cache-server URLs and Python 2 compatibility branches have been removed.
- The local dataset is the authoritative default source; external fetching is only used as a fallback when enabled.

## Tests
Run the full test suite with:

```bash
./run_tests
```
