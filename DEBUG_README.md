# Debug Script Usage

## Two Versions Available

### 1. `debug_server.py` (Threading - Slower)
- Uses `requests` library with threading
- Works with basic setup
- Slower: ~0.8-2 requests/second

### 2. `debug_server_async.py` (Async - MUCH FASTER) ⚡
- Uses `aiohttp` for async requests
- **MUCH faster**: 500-5000+ requests/second
- Requires additional packages

## Installation for Async Version

```bash
pip install aiohttp aiosocks
```

Or install all requirements:
```bash
pip install -r requirements.txt
```

## Usage

### Async Version (Recommended):
```bash
python debug_server_async.py
```

### Threading Version:
```bash
python debug_server.py
```

## Performance Comparison

For 138,000 tests:
- **Threading version**: ~48 hours (0.8 req/s)
- **Async version (500 concurrent)**: ~2-5 minutes (500-1000 req/s)
- **Async version (1000 concurrent)**: ~1-2 minutes (1000-2000 req/s)

## Recommended Settings

- **Concurrent requests**: 300-1000 (start with 500)
- **Attempts per combination**: 1-10 (start with 1 to see patterns)
- **Total tests**: proxies × cookies × attempts

## What It Shows

1. **Success rates** by proxy and cookie
2. **Error breakdown** (rate limits, timeouts, etc.)
3. **Response times** analysis
4. **Status codes** distribution
5. **Sample successful/error results**

## Troubleshooting

If async version has SOCKS5 issues:
- Install `aiosocks`: `pip install aiosocks`
- Or use HTTP proxies only for testing
- Check proxy credentials are correct
