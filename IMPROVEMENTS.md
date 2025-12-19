# Scanner Improvements

## Key Enhancements

### 1. **SOCKS5 Proxy Support**
- Added all 20 SOCKS5 proxies from your list
- Automatic parsing of SOCKS5 proxy format
- Support for both HTTP and SOCKS5 proxies simultaneously
- Total: 23 proxies (3 HTTP + 20 SOCKS5)

### 2. **Aggressive Retry Logic**
- **Max Retries**: Increased to 10 retries per failed server
- **Retry Queues**: Separate queues for:
  - Failed discovery requests
  - Failed detection requests
  - General failed servers
- **Exponential Backoff**: Smart retry delays that increase with each attempt
- **Continuous Retry Workers**: Dedicated threads that continuously retry failed requests

### 3. **Enhanced Proxy Utilization**
- Better distribution of 60+ cookies across all 23 proxies
- Proxy rotation and health tracking
- More aggressive rate limits in aggressive mode:
  - Discovery: 80 requests/minute (was 45)
  - Detection: 200 requests/minute (was 120)

### 4. **Improved Performance**
- Increased detection workers: 8 per cookie (was 6)
- Larger queues: 500,000 main queue, 100,000 retry queue
- Reduced delays: 0.05s discovery, 0.02s detection
- More tolerance for consecutive errors (10 vs 5)

### 5. **Better Error Recovery**
- Failed servers are tracked and automatically retried
- Discovery failures are queued and retried separately
- Rate limit handling with reduced cooldown (2s vs 5s)
- Health monitoring for all proxies

### 6. **Database Enhancements**
- Added `retry_count` tracking
- New `failed_servers` table for persistent retry tracking
- Better error type classification

## Configuration Changes

```python
'DISCOVERY_DELAY': 0.05,      # Reduced from 0.08
'DETECTION_DELAY': 0.02,      # Reduced from 0.03
'MAX_RETRIES': 10,            # Increased from 3
'QUEUE_MAXSIZE': 500000,      # Increased from 250000
'RETRY_QUEUE_MAXSIZE': 100000, # New
'AGGRESSIVE_MODE': True,      # New
```

## New Components

1. **RetryManager**: Manages exponential backoff retry logic
2. **Retry Discovery Workers**: 3 dedicated threads for retrying failed discovery
3. **Failed Servers Retry Worker**: Continuously retries failed servers
4. **Enhanced Proxy Session**: Supports both HTTP and SOCKS5

## Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Create `config.txt` with your cookies (one per line)

3. Run the scanner:
```bash
python scanner.py
```

## Performance Improvements

- **Discovery Rate**: Up to 80 requests/minute per proxy (vs 45)
- **Detection Rate**: Up to 200 checks/minute (vs 120)
- **Retry Coverage**: All failed requests are retried up to 10 times
- **Proxy Coverage**: All 23 proxies are utilized with 60+ cookies

## Aggressive Features

- **No Thundering Herd Protection**: Disabled for maximum aggression
- **Reduced Cooldowns**: Faster recovery from rate limits
- **More Workers**: 8 detection workers per cookie
- **Larger Queues**: Can handle 500K+ servers in queue
- **Continuous Retries**: Failed servers are retried until success or max attempts
