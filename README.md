# fake-useragent: Local-First Implementation

A Python library that provides **offline-first**, **deterministic** user-agent string generation with **zero network dependencies** by default.

## 🎯 Key Features

- **✅ Fully Offline by Default**: Works completely offline using bundled package data
- **✅ Zero Network Calls**: No external HTTP requests unless explicitly enabled
- **✅ Reproducible Builds**: Deterministic behavior across environments
- **✅ Fast**: Instant initialization with no I/O blocking
- **✅ Lightweight**: No runtime dependencies on external services
- **✅ Python 3 Only**: Modern, clean codebase without legacy compatibility layers
- **✅ Extensively Tested**: Comprehensive test suite with 26+ test cases

## 📦 Installation

```bash
pip install fake-useragent
```

## 🚀 Quick Start

### Basic Usage (Offline Mode - Default)

```python
from fake import FakeUserAgent

# Initialize - uses bundled package data, no network calls
ua = FakeUserAgent()

# Get user agents for different browsers
print(ua.chrome)
# Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36...

print(ua.firefox)
# Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko...

print(ua.safari)
# Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)...

# Get random user agent
print(ua.random)
# Returns a random user agent from available browsers
```

### Browser Shortcuts

```python
ua = FakeUserAgent()

# All of these work
ua.chrome
ua.firefox
ua.safari
ua.ie              # Internet Explorer
ua.edge            # Microsoft Edge
ua.opera

# Shortcuts
ua.internetexplorer  # Same as ie
ua.msie              # Same as ie
ua.ff                # Same as firefox
```

### Dictionary-Style Access

```python
ua = FakeUserAgent()

chrome_ua = ua['chrome']
random_ua = ua['random']
```

## 🔧 Configuration

### Default Behavior (Local-First)

By default, fake-useragent uses bundled package data and **never** makes network requests:

```python
# Default: offline mode with bundled data
ua = FakeUserAgent()
```

### External Data Fetching (Opt-In)

To fetch fresh data from external sources, explicitly enable it:

```python
# Fetch data from external sources
ua = FakeUserAgent(use_external_data=True)
```

**⚠️ Warning**: External data fetching requires internet connectivity and may fail if external services are unavailable.

### Using a Fallback

Provide a fallback user-agent for error conditions:

```python
ua = FakeUserAgent(fallback='Mozilla/5.0 (compatible; MyBot/1.0)')

# If an error occurs, fallback is returned instead of raising exception
user_agent = ua.nonexistent_browser  # Returns fallback
```

### Safe Attributes

Prevent certain attributes from triggering user-agent lookup:

```python
ua = FakeUserAgent(safe_attrs=('my_custom_attr',))
ua.my_custom_attr = 'some value'  # Won't trigger UA lookup
```

## 📂 Package Data

### Bundled Data Location

User-agent data is bundled in the package at:
```
data/browsers.json
```

### Data Format

The bundled data uses **JSON Lines** format:
```json
{"chrome": ["Mozilla/5.0 ...", "Mozilla/5.0 ..."]}
{"firefox": ["Mozilla/5.0 ...", "Mozilla/5.0 ..."]}
{"safari": ["Mozilla/5.0 ...", "Mozilla/5.0 ..."]}
```

Each line contains a JSON object mapping browser names to arrays of user-agent strings.

### Supported Browsers

The bundled package includes user agents for:
- Chrome
- Firefox
- Safari
- Edge
- Internet Explorer
- Opera

## 🔄 Migration Guide

### From Previous Versions

If you're migrating from an older version that used `use_cache_server` or external data by default:

**Old Code:**
```python
ua = FakeUserAgent(use_cache_server=False)
```

**New Code:**
```python
# Default is now offline-first, no changes needed
ua = FakeUserAgent()
```

**To Enable External Data (if needed):**
```python
ua = FakeUserAgent(use_external_data=True)
```

### Parameter Changes

| Old Parameter | New Parameter | Notes |
|--------------|---------------|-------|
| `use_cache_server` | `use_external_data` | Renamed for clarity |
| `cache` | `cache` | Still available, only affects external data mode |
| `path` | `path` | Still available, only used with external data |

## 🧪 Testing

### Run All Tests

```bash
# Windows PowerShell
.\run_tests.ps1

# Or directly with Python
python test_fake_useragent.py
```

### Test Coverage

The test suite includes 26+ tests covering:
- ✅ Bundled data loading
- ✅ Offline functionality
- ✅ No network calls by default
- ✅ Browser access methods
- ✅ Random user agent selection
- ✅ Fallback mechanisms
- ✅ Error handling
- ✅ Data integrity
- ✅ API compatibility

## 🏗️ Architecture

### Design Principles

1. **Local-First**: Bundled data is the primary source
2. **Explicit Opt-In**: External requests only when explicitly enabled
3. **Zero Dependencies**: No runtime network requirements
4. **Deterministic**: Same input always produces same output (when using bundled data)
5. **Python 3 Only**: Modern, maintainable codebase

### How It Works

1. **Package Installation**: `data/browsers.json` is installed with the package
2. **First Import**: `importlib.resources` loads data from package
3. **User Agent Access**: Random selection from pre-loaded data
4. **No I/O**: All data is in memory, no disk or network access

### Data Loading Flow

```
┌─────────────────────────────────────┐
│ Initialize FakeUserAgent()          │
└──────────────┬──────────────────────┘
               │
        use_external_data?
               │
       ┌───────┴───────┐
       │               │
      Yes              No (Default)
       │               │
       ▼               ▼
┌──────────────┐  ┌─────────────────────┐
│ Fetch from   │  │ Load from bundled   │
│ external     │  │ data/browsers.json  │
│ sources      │  │ (importlib.resources)│
└──────────────┘  └─────────────────────┘
       │               │
       └───────┬───────┘
               │
               ▼
     ┌──────────────────┐
     │ User Agent Ready │
     └──────────────────┘
```

## 📝 Examples

### Simple Usage

```python
from fake import FakeUserAgent

ua = FakeUserAgent()

# Use in requests
import requests
response = requests.get('https://example.com', headers={'User-Agent': ua.chrome})
```

### Web Scraping

```python
from fake import FakeUserAgent
import requests

ua = FakeUserAgent()

def scrape_page(url):
    headers = {'User-Agent': ua.random}
    response = requests.get(url, headers=headers)
    return response.text

# Each request uses a different random user agent
for url in urls:
    html = scrape_page(url)
    # Process html...
```

### Testing

```python
from fake import FakeUserAgent

def test_api_with_different_browsers():
    ua = FakeUserAgent()
    
    # Test with different browser user agents
    for browser in ['chrome', 'firefox', 'safari']:
        headers = {'User-Agent': getattr(ua, browser)}
        response = api_call(headers)
        assert response.status_code == 200
```

## 🔒 Privacy & Security

### No Telemetry

This library does **not**:
- Make any network requests by default
- Send telemetry or analytics
- Track usage
- Phone home

### Offline Operation

The library is designed to work completely offline:
- All data bundled with package
- No external service dependencies
- No network timeouts or failures
- Predictable, deterministic behavior

## 📄 API Reference

### FakeUserAgent Class

```python
class FakeUserAgent:
    def __init__(
        self,
        cache=True,
        use_external_data=False,
        path=settings.DB,
        fallback=None,
        browsers=["chrome", "edge", "internet explorer", "firefox", "safari", "opera"],
        verify_ssl=True,
        safe_attrs=tuple(),
    )
```

**Parameters:**
- `cache` (bool): Enable filesystem caching (only relevant with `use_external_data=True`)
- `use_external_data` (bool): If True, fetch data from external sources. Default: False
- `path` (str): Path for cache file (only used with `cache=True` and `use_external_data=True`)
- `fallback` (str): Fallback user-agent string if retrieval fails
- `browsers` (list): List of browser names (only used with `use_external_data=True`)
- `verify_ssl` (bool): SSL verification for external requests
- `safe_attrs` (tuple): Safe attributes to access without triggering user-agent lookup

### Methods

#### Browser Access

```python
ua.chrome       # Get Chrome user agent
ua.firefox      # Get Firefox user agent
ua.safari       # Get Safari user agent
ua.ie           # Get Internet Explorer user agent
ua.edge         # Get Edge user agent
ua.opera        # Get Opera user agent
ua.random       # Get random user agent
```

#### Dictionary Access

```python
ua['chrome']    # Same as ua.chrome
ua['random']    # Same as ua.random
```

## 🤝 Contributing

Contributions are welcome! Areas for contribution:
- Additional bundled user agents
- New browser types
- Bug fixes
- Documentation improvements
- Test coverage

## 📜 License

This project is licensed under the Apache License 2.0.

## 🔗 Links

- **GitHub**: [fake-useragent](https://github.com/hellysmile/fake-useragent)
- **PyPI**: [fake-useragent](https://pypi.org/project/fake-useragent/)

## ✨ Changelog

### Version 2.0.0 (Local-First Release)

#### Breaking Changes
- **Default behavior is now offline-first**: No network requests by default
- Removed `use_cache_server` parameter (replaced with `use_external_data`)
- Removed Python 2 support
- Removed cache server URL dependency

#### New Features
- ✅ Bundled package data using `importlib.resources`
- ✅ Zero network dependencies by default
- ✅ Deterministic, reproducible builds
- ✅ Fast initialization (no I/O blocking)
- ✅ Comprehensive test suite (26+ tests)

#### Improvements
- Cleaner, modern Python 3-only codebase
- Better error messages
- Improved documentation
- Explicit opt-in for external data fetching

## 🙏 Acknowledgments

Thanks to all contributors who have helped make this library better!

---

**Made with ❤️ for the Python community**
