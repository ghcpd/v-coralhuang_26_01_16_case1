# fake-useragent

A Python library for generating random, valid User-Agent HTTP headers.

## Overview

`fake-useragent` provides a simple way to generate random user-agent strings for various browsers. The library works **offline by default**, loading user-agent data from bundled package resources without requiring any network access.

## Installation

```bash
pip install fake-useragent
```

## Quick Start

```python
from fake import UserAgent

# Create a UserAgent instance (works offline by default)
ua = UserAgent()

# Get a random user-agent for a specific browser
print(ua.chrome)
print(ua.firefox)
print(ua.safari)
print(ua.edge)
print(ua.opera)

# Get a completely random user-agent from any browser
print(ua.random)
```

## Features

- **Offline-first design**: Works without network access using bundled data
- **No runtime dependencies on external services**: Default usage requires no HTTP requests
- **Simple API**: Easy-to-use interface for generating user-agents
- **Multiple browser support**: Chrome, Firefox, Safari, Edge, Opera, and Internet Explorer

## Default Behavior (Local-First)

By default, `fake-useragent` loads user-agent data from a bundled JSON file included with the package. This ensures:

- **Offline functionality**: No network access required
- **Reproducible builds**: Same data across all installations
- **Fast initialization**: No HTTP latency
- **Reliability**: No dependency on external servers

```python
from fake import UserAgent

# This works completely offline
ua = UserAgent()
print(ua.chrome)  # Returns a random Chrome user-agent string
```

## Package Data Location and Format

The bundled user-agent data is stored in:

```
data/browsers.json
```

### Data Format

The file uses JSON format mapping browser names to arrays of user-agent strings:

```json
{"chrome": ["Mozilla/5.0 (Windows NT 10.0; ...", "Mozilla/5.0 (Macintosh; ..."]}
{"firefox": ["Mozilla/5.0 (Windows NT 10.0; rv:...", ...]}
```

## Enabling External Data Fetching

If you need to fetch fresh user-agent data from external sources, you can explicitly enable it:

```python
from fake import UserAgent

# Enable external data fetching (makes network requests)
ua = UserAgent(use_external_data=True)
```

**Warning**: Setting `use_external_data=True` will:
- Make HTTP requests to external servers
- Require network connectivity
- May be slower due to network latency
- Could fail if external servers are unavailable

This option should only be used when you specifically need the latest user-agent strings and are willing to accept the trade-offs.

## API Reference

### `UserAgent` class

```python
UserAgent(
    use_external_data=False,  # Enable external data fetching
    fallback=None,            # Fallback user-agent string on errors
    browsers=None,            # List of browsers to use
    verify_ssl=True,          # Verify SSL for external requests
    safe_attrs=tuple(),       # Attributes to pass to parent __getattr__
)
```

### Parameters

- **`use_external_data`** (bool, default=`False`):
  - `False`: Load from bundled package data (default, offline)
  - `True`: Fetch from external sources (requires network)

- **`fallback`** (str, optional): A fallback user-agent string to return if an error occurs. If `None`, errors will raise exceptions.

- **`browsers`** (list, optional): List of browser names to include. Default: `["chrome", "edge", "internet explorer", "firefox", "safari", "opera"]`

- **`verify_ssl`** (bool, default=`True`): Whether to verify SSL certificates when fetching external data. Only relevant when `use_external_data=True`.

- **`safe_attrs`** (tuple/list/set, optional): Attribute names that should use the parent class's `__getattr__` instead of returning user-agents.

### Properties/Attributes

Access user-agents by browser name:

- `ua.chrome` - Random Chrome user-agent
- `ua.firefox` - Random Firefox user-agent
- `ua.safari` - Random Safari user-agent
- `ua.edge` - Random Edge user-agent
- `ua.opera` - Random Opera user-agent
- `ua.ie` / `ua.internetexplorer` - Random Internet Explorer user-agent
- `ua.random` - Random user-agent from any browser

### Methods

- **`refresh()`**: Reload user-agent data from the current source

## Browser Aliases

The following aliases are supported for convenience:

| Alias | Browser |
|-------|---------|
| `ie`, `msie`, `internetexplorer` | Internet Explorer |
| `ff` | Firefox |
| `google`, `googlechrome` | Chrome |
| `microsoft edge` | Edge |

## Error Handling

```python
from fake import UserAgent
from errors import FakeUserAgentError

# Using fallback (errors suppressed)
ua = UserAgent(fallback="Mozilla/5.0 (compatible; Bot/1.0)")

# Without fallback (errors raised)
try:
    ua = UserAgent()
    print(ua.nonexistent_browser)
except FakeUserAgentError as e:
    print(f"Error: {e}")
```

## Requirements

- Python 3.7+
- No external runtime dependencies for default (offline) usage

## License

MIT License
