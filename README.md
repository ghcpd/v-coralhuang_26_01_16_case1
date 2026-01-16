# fake-useragent (local-first)

✅ **Default offline behavior** — ships with bundled `data/browsers.json` and never hits the network unless you ask for it.

## 🚀 Usage

```python
from fake import FakeUserAgent

ua = FakeUserAgent()  # offline by default, loads bundled data
print(ua.chrome)
print(ua.random)
```

### Opt-in external fetching

```python
ua = FakeUserAgent(use_external_data=True)
```

When `use_external_data=True`, the library may fetch data from `https://useragentstring.com/...` using the legacy scraping flow. Network access will **never** occur unless this flag is set.

## 📂 Bundled data

- Location: `data/browsers.json`
- Accessed via `importlib.resources.files("data").joinpath("browsers.json")`
- Format: **JSON Lines** (one JSON object per line), e.g.

  ```json
  {"chrome": ["UA1", "UA2"], "firefox": ["UA3"]}
  {"safari": ["UA4"]}
  ```

> 💡 The parser is tolerant of a single JSON object on one line (for backwards compatibility).

## 🔧 API changes

- ❌ Removed parameters: `cache`, `use_cache_server`, `path`
- ✅ New parameter: `use_external_data: bool = False`
- Python 3 only; Python 2 compatibility shims removed

## 🔒 No network by default

- Offline environments work out of the box
- Deterministic builds & reproducible runs
- Network only when `use_external_data=True`

## 🧪 Tests

Run all tests with the one-click script:

```bash
./run_tests  # on Unix-like
# or on Windows
python run_tests
```

Tests cover:
- Loading from bundled package data
- Ensuring no network access by default
- Opt-in external fetching when requested

## 🗂 Packaging notes

- `data` is a Python package (`data/__init__.py`) to support `importlib.resources`
- `pyproject.toml` includes `data/browsers.json` as package data
- For Python < 3.9, `importlib-resources` is declared as a dependency

## 🔁 Migration guide

| Old parameter        | New parameter          | Notes |
|----------------------|------------------------|-------|
| `cache`              | _removed_              | Bundled data is used directly; no temp cache file |
| `use_cache_server`   | _removed_              | Cache server logic removed |
| `path`               | _removed_              | No filesystem cache |
| _(none)_             | `use_external_data`    | Explicit opt-in for network access |

If you previously relied on the cache server or runtime scraping, set `use_external_data=True` and consider persisting the fetched data yourself.
