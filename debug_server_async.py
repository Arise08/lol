import asyncio
import aiohttp
import time
from datetime import datetime
import json
import re
import os
import warnings
from collections import defaultdict
from typing import List, Dict, Optional

# Suppress SSL warnings
warnings.filterwarnings('ignore', category=RuntimeWarning)
asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy() if os.name == 'nt' else asyncio.DefaultEventLoopPolicy())

class AsyncServerDebugger:
    def __init__(self):
        self.proxy_pool = self.load_all_proxies()
        self.cookies = []
        self.results = []
        self.completed = 0
        self.lock = asyncio.Lock()
        self.current_job_id = None  # Store job_id for analyze_results
        
    def load_all_proxies(self):
        """Load all proxies including SOCKS5"""
        proxies = [
            {
                "host": "core-residential.evomi.com",
                "port": 1000,
                "user": "tapinonmam7",
                "pass": "Rilorxcb4nVVTiT3EQsv_country-ES_http3-1_session-IJHMRPCIC",
                "id": "PROXY-ES-HTTP",
                "type": "http"
            },
            {
                "host": "core-residential.evomi.com", 
                "port": 1000,
                "user": "tapinonmam7",
                "pass": "Rilorxcb4nVVTiT3EQsv_http3-1_session-JPL62O1N8",
                "id": "PROXY-GLOBAL-1-HTTP",
                "type": "http"
            },
            {
                "host": "core-residential.evomi.com",
                "port": 1000, 
                "user": "tapinonmam7",
                "pass": "Rilorxcb4nVVTiT3EQsv_http3-1_session-F5O7VT4FD",
                "id": "PROXY-GLOBAL-2-HTTP",
                "type": "http"
            }
        ]
        
        socks5_proxies = [
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-R4SJEN531",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-4R7B80BCD",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-SWLG822T5",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-SJKEJMOZB",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-9KDSMO354",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-3CEUDK8N1",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-STGHUIHEM",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-JGJGNYH7W",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-OOM3BML9H",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-BKFI7C4CX",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-ZA8SXQXWO",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-MK408P5L5",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-3NSH301AN",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-VPSKBMDMO",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-9GY1BWREA",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-AV8K4P3GN",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-ZNJ2E3KK9",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-1P0YWI6W8",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-XDN47YI3T",
            "socks5://core-residential.evomi.com:1002:tapinonmam7:Rilorxcb4nVVTiT3EQsv_session-SAYG1PVO1"
        ]
        
        for i, proxy_str in enumerate(socks5_proxies):
            match = re.match(r'socks5://([^:]+):(\d+):([^:]+):(.+)', proxy_str)
            if match:
                host, port, user, password = match.groups()
                proxies.append({
                    "host": host,
                    "port": int(port),
                    "user": user,
                    "pass": password,
                    "id": f"PROXY-SOCKS5-{i+1}",
                    "type": "socks5"
                })
        
        return proxies
    
    def load_cookies_from_config(self):
        """Load cookies from config file"""
        config_files = ['config.txt', 'Config.txt', 'CONFIG.txt']
        
        for config_file in config_files:
            if os.path.exists(config_file):
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    cookies = []
                    for line in lines:
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if not line.startswith('.ROBLOSECURITY='):
                                line = f".ROBLOSECURITY={line}"
                            cookies.append(line)
                    
                    return cookies
                except Exception as e:
                    print(f"❌ Error reading {config_file}: {e}")
        
        return []
    
    def get_proxy_url(self, proxy_config):
        """Get proxy URL for aiohttp"""
        if proxy_config['type'] == 'socks5':
            # aiohttp SOCKS5 format: socks5://user:pass@host:port
            return f"socks5://{proxy_config['user']}:{proxy_config['pass']}@{proxy_config['host']}:{proxy_config['port']}"
        else:
            # HTTP proxy format
            return f"http://{proxy_config['user']}:{proxy_config['pass']}@{proxy_config['host']}:{proxy_config['port']}"
    
    async def test_server(self, session: aiohttp.ClientSession, game_id: str, job_id: str, 
                          proxy_config: Dict, cookie: str, cookie_num: int, attempt_num: int):
        """Test a single server with specific proxy and cookie (ASYNC)"""
        result = {
            'proxy_id': proxy_config['id'],
            'proxy_type': proxy_config['type'],
            'cookie_num': cookie_num,
            'attempt': attempt_num,
            'timestamp': datetime.now().isoformat(),
            'success': False,
            'status_code': None,
            'response_time': 0,
            'error': None,
            'is_udmux': False,
            'is_non_udmux': False,
            'server_info': None,
            'response_headers': {},
            'response_body': None
        }
        
        start_time = time.time()
        proxy_url = self.get_proxy_url(proxy_config)
        
        try:
            payload = {
                'placeId': int(game_id),
                'gameId': job_id,
                'isPlayTogetherGame': False
            }
            
            headers = {
                'Content-Type': 'application/json',
                'User-Agent': 'Roblox/WinInet',
                'Cookie': cookie,
                'Connection': 'keep-alive'
            }
            
            timeout = aiohttp.ClientTimeout(total=3, connect=2)
            
            # For SOCKS5, we might need special handling, but aiohttp should handle it
            # If SOCKS5 doesn't work, we can fall back to HTTP proxies
            try:
                async with session.post(
                    'https://gamejoin.roblox.com/v1/join-game-instance',
                    json=payload,
                    headers=headers,
                    proxy=proxy_url,
                    timeout=timeout,
                    ssl=False  # Disable SSL verification
                ) as response:
                    result['response_time'] = time.time() - start_time
                    result['status_code'] = response.status
                    result['response_headers'] = dict(response.headers)
                    
                    if response.status == 200:
                        try:
                            data = await response.json()
                            result['response_body'] = data
                            result['success'] = True
                            
                            join_script = data.get('joinScript', {})
                            if join_script:
                                udmux_endpoints = join_script.get('UdmuxEndpoints')
                                if udmux_endpoints:
                                    result['is_udmux'] = True
                                else:
                                    machine_address = join_script.get('MachineAddress', '')
                                    server_port = join_script.get('ServerPort', 0)
                                    if machine_address and server_port:
                                        result['is_non_udmux'] = True
                                        result['server_info'] = {
                                            'machine_address': machine_address,
                                            'server_port': server_port,
                                            'full_address': f"{machine_address}:{server_port}"
                                        }
                        except Exception as e:
                            result['error'] = f'JSON decode error: {str(e)[:100]}'
                            result['response_body'] = (await response.text())[:500]
                    elif response.status == 429:
                        result['error'] = 'Rate Limited'
                        result['retry_after'] = response.headers.get('Retry-After', 'Unknown')
                    elif response.status == 400:
                        result['error'] = 'Bad Request'
                        try:
                            result['response_body'] = await response.json()
                        except:
                            result['response_body'] = (await response.text())[:500]
                    elif response.status == 403:
                        result['error'] = 'Forbidden'
                    elif response.status == 404:
                        result['error'] = 'Server Not Found'
                    elif response.status == 500:
                        result['error'] = 'Server Error'
                    else:
                        result['error'] = f'HTTP {response.status}'
                        try:
                            result['response_body'] = (await response.text())[:500]
                        except:
                            pass
            except aiohttp.ClientProxyConnectionError as e:
                result['error'] = 'Proxy Connection Error'
                result['response_time'] = time.time() - start_time
            except aiohttp.ClientConnectionError as e:
                # Catch SSL errors and connection errors silently
                error_str = str(e)
                if 'SSL' in error_str or 'application data after close notify' in error_str:
                    result['error'] = 'SSL Connection Error'
                else:
                    result['error'] = f'Connection Error: {error_str[:100]}'
                result['response_time'] = time.time() - start_time
                        
        except asyncio.TimeoutError:
            result['error'] = 'Timeout'
            result['response_time'] = time.time() - start_time
        except aiohttp.ClientConnectorError as e:
            error_str = str(e)
            if 'SSL' in error_str or 'application data after close notify' in error_str:
                result['error'] = 'SSL Connection Error'
            else:
                result['error'] = f'Connection Error: {error_str[:100]}'
            result['response_time'] = time.time() - start_time
        except Exception as e:
            error_str = str(e)
            if 'SSL' in error_str or 'application data after close notify' in error_str:
                result['error'] = 'SSL Error'
            else:
                result['error'] = f'Exception: {error_str[:100]}'
            result['response_time'] = time.time() - start_time
        
        return result
    
    async def run_debug(self, game_id: str, job_id: str, num_attempts: int = 1, max_concurrent: int = 500):
        """Run debug test with all proxy-cookie combinations (ULTRA AGGRESSIVE ASYNC)"""
        self.current_job_id = job_id  # Store for analyze_results
        
        print(f"\n{'='*80}")
        print(f"🔍 SERVER DEBUGGER (ULTRA AGGRESSIVE ASYNC MODE)")
        print(f"{'='*80}")
        print(f"Game ID: {game_id}")
        print(f"Job ID: {job_id}")
        print(f"Proxies: {len(self.proxy_pool)}")
        print(f"Cookies: {len(self.cookies)}")
        print(f"Total Combinations: {len(self.proxy_pool) * len(self.cookies)}")
        print(f"Attempts per combination: {num_attempts}")
        print(f"Max Concurrent: {max_concurrent}")
        print(f"{'='*80}\n")
        
        results = []
        total_tests = len(self.proxy_pool) * len(self.cookies) * num_attempts
        completed = 0
        start_time = time.time()
        
        # Prepare all test tasks
        tasks = []
        for proxy in self.proxy_pool:
            for cookie_idx, cookie in enumerate(self.cookies):
                for attempt in range(1, num_attempts + 1):
                    tasks.append((game_id, job_id, proxy, cookie, cookie_idx + 1, attempt))
        
        # Create semaphore to limit concurrent requests
        semaphore = asyncio.Semaphore(max_concurrent)
        
        async def worker_with_semaphore(session, task):
            async with semaphore:
                game_id, job_id, proxy, cookie, cookie_num, attempt_num = task
                result = await self.test_server(session, game_id, job_id, proxy, cookie, cookie_num, attempt_num)
                
                nonlocal completed
                completed += 1
                results.append(result)
                
                if completed % 100 == 0 or completed == total_tests:
                    elapsed = time.time() - start_time
                    rate = completed / elapsed if elapsed > 0 else 0
                    remaining = total_tests - completed
                    eta = remaining / rate if rate > 0 else 0
                    success_count = len([r for r in results if r.get('success')])
                    error_count = len([r for r in results if not r.get('success')])
                    print(f"⏳ Progress: {completed}/{total_tests} ({completed*100//total_tests}%) | "
                          f"Rate: {rate:.0f}/s | ETA: {eta:.0f}s | "
                          f"✅ Success: {success_count} | ❌ Errors: {error_count}", end='\r')
        
        # Create aiohttp session with connection pooling and SSL handling
        connector = aiohttp.TCPConnector(
            limit=max_concurrent,
            limit_per_host=50,
            ttl_dns_cache=300,
            force_close=False,
            enable_cleanup_closed=True,
            ssl=False  # Disable SSL verification for faster connections
        )
        
        print(f"🚀 Starting {len(tasks)} tests with {max_concurrent} concurrent requests...\n")
        
        async with aiohttp.ClientSession(connector=connector) as session:
            # Create all tasks
            coroutines = [worker_with_semaphore(session, task) for task in tasks]
            
            # Run all tasks concurrently with exception handling
            # Use return_exceptions=True to prevent unhandled exceptions from stopping everything
            await asyncio.gather(*coroutines, return_exceptions=True)
        
        elapsed_time = time.time() - start_time
        print(f"\n✅ Completed {completed} tests in {elapsed_time:.1f} seconds")
        print(f"⚡ Average rate: {completed/elapsed_time:.0f} requests/second\n")
        
        return results
    
    def analyze_results(self, results):
        """Analyze and display results"""
        if not results:
            print("❌ No results to analyze")
            return
        
        # Categorize results
        by_status = defaultdict(list)
        by_proxy = defaultdict(list)
        by_cookie = defaultdict(list)
        by_error = defaultdict(list)
        
        successful = []
        udmux = []
        non_udmux = []
        errors = []
        
        for result in results:
            by_status[result['status_code']].append(result)
            by_proxy[result['proxy_id']].append(result)
            by_cookie[result['cookie_num']].append(result)
            
            if result['success']:
                successful.append(result)
                if result['is_udmux']:
                    udmux.append(result)
                elif result['is_non_udmux']:
                    non_udmux.append(result)
            else:
                errors.append(result)
                if result['error']:
                    by_error[result['error']].append(result)
        
        # Print summary
        print(f"{'='*80}")
        print(f"📊 RESULTS SUMMARY")
        print(f"{'='*80}")
        print(f"Total Tests: {len(results)}")
        print(f"✅ Successful: {len(successful)} ({len(successful)*100/len(results):.1f}%)")
        print(f"   ├─ UDMUX: {len(udmux)}")
        print(f"   └─ NON-UDMUX: {len(non_udmux)}")
        print(f"❌ Errors: {len(errors)} ({len(errors)*100/len(results):.1f}%)")
        print(f"{'='*80}\n")
        
        # Status code breakdown
        print(f"📈 STATUS CODE BREAKDOWN:")
        for status_code in sorted(by_status.keys()):
            count = len(by_status[status_code])
            percentage = count * 100 / len(results)
            print(f"   {status_code}: {count} ({percentage:.1f}%)")
        print()
        
        # Error breakdown
        if by_error:
            print(f"❌ ERROR BREAKDOWN:")
            for error_type in sorted(by_error.keys(), key=lambda x: len(by_error[x]), reverse=True):
                count = len(by_error[error_type])
                percentage = count * 100 / len(results)
                print(f"   {error_type}: {count} ({percentage:.1f}%)")
            print()
        
        # Proxy performance
        print(f"🌐 PROXY PERFORMANCE:")
        proxy_stats = []
        for proxy_id, proxy_results in by_proxy.items():
            success_count = sum(1 for r in proxy_results if r['success'])
            success_rate = success_count * 100 / len(proxy_results) if proxy_results else 0
            avg_time = sum(r['response_time'] for r in proxy_results) / len(proxy_results) if proxy_results else 0
            proxy_stats.append({
                'id': proxy_id,
                'total': len(proxy_results),
                'success': success_count,
                'success_rate': success_rate,
                'avg_time': avg_time
            })
        
        for stat in sorted(proxy_stats, key=lambda x: x['success_rate'], reverse=True)[:10]:
            print(f"   {stat['id']}: {stat['success']}/{stat['total']} ({stat['success_rate']:.1f}%) | "
                  f"Avg: {stat['avg_time']*1000:.0f}ms")
        print()
        
        # Cookie performance
        print(f"🍪 COOKIE PERFORMANCE:")
        cookie_stats = []
        for cookie_num, cookie_results in by_cookie.items():
            success_count = sum(1 for r in cookie_results if r['success'])
            success_rate = success_count * 100 / len(cookie_results) if cookie_results else 0
            cookie_stats.append({
                'num': cookie_num,
                'total': len(cookie_results),
                'success': success_count,
                'success_rate': success_rate
            })
        
        for stat in sorted(cookie_stats, key=lambda x: x['success_rate'], reverse=True)[:10]:
            print(f"   Cookie {stat['num']}: {stat['success']}/{stat['total']} ({stat['success_rate']:.1f}%)")
        print()
        
        # Response time analysis
        if successful:
            response_times = [r['response_time'] for r in successful]
            print(f"⏱️ RESPONSE TIME ANALYSIS (Successful requests):")
            print(f"   Min: {min(response_times)*1000:.0f}ms")
            print(f"   Max: {max(response_times)*1000:.0f}ms")
            print(f"   Avg: {sum(response_times)/len(response_times)*1000:.0f}ms")
            print()
        
        # Sample successful results
        if successful:
            print(f"✅ SAMPLE SUCCESSFUL RESULTS:")
            for i, result in enumerate(successful[:5], 1):
                print(f"\n   Result {i}:")
                print(f"      Proxy: {result['proxy_id']} ({result['proxy_type']})")
                print(f"      Cookie: {result['cookie_num']}")
                print(f"      Response Time: {result['response_time']*1000:.0f}ms")
                if result['is_udmux']:
                    print(f"      Type: UDMUX")
                elif result['is_non_udmux']:
                    print(f"      Type: NON-UDMUX")
                    print(f"      Server: {result['server_info']['full_address']}")
            print()
        
        # Sample error results
        if errors:
            print(f"❌ SAMPLE ERROR RESULTS:")
            for i, result in enumerate(errors[:10], 1):
                print(f"\n   Error {i}:")
                print(f"      Proxy: {result['proxy_id']} ({result['proxy_type']})")
                print(f"      Cookie: {result['cookie_num']}")
                print(f"      Status: {result['status_code']}")
                print(f"      Error: {result['error']}")
                if result.get('retry_after'):
                    print(f"      Retry-After: {result['retry_after']}")
            print()
        
        # Save detailed results to file
        job_id = self.current_job_id if self.current_job_id else 'unknown'
        filename = f"debug_results_{job_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"💾 Detailed results saved to: {filename}")
        print(f"{'='*80}\n")


async def main_async():
    print("🔍 SERVER DEBUGGER (ASYNC)")
    print("=" * 80)
    print("This tool tests a specific server (JOB ID) with all proxies and cookies")
    print("to see how the server reacts to different requests.")
    print("=" * 80)
    
    debugger = AsyncServerDebugger()
    
    # Load cookies
    cookies = debugger.load_cookies_from_config()
    if not cookies:
        print("❌ No cookies found in config.txt")
        return
    
    debugger.cookies = cookies
    print(f"✅ Loaded {len(cookies)} cookies")
    print(f"✅ Loaded {len(debugger.proxy_pool)} proxies")
    
    # Get inputs
    print("\n" + "="*80)
    game_id = input("🎮 Enter Game ID: ").strip()
    if not game_id.isdigit():
        print("❌ Invalid game ID")
        return
    
    job_id = input("🔑 Enter Job ID: ").strip()
    if not job_id:
        print("❌ Invalid job ID")
        return
    
    num_attempts_input = input("🔄 Number of attempts per combination (default 1): ").strip()
    num_attempts = int(num_attempts_input) if num_attempts_input.isdigit() else 1
    
    max_concurrent_input = input(f"⚡ Max concurrent requests (default 500, recommended 300-1000): ").strip()
    max_concurrent = int(max_concurrent_input) if max_concurrent_input.isdigit() else 500
    
    print(f"\n🚀 Starting ULTRA AGGRESSIVE async debug test...")
    print(f"   Total tests: {len(debugger.proxy_pool) * len(cookies) * num_attempts}")
    print(f"   Concurrent requests: {max_concurrent}")
    print(f"   Expected speed: ~{max_concurrent * 2}-{max_concurrent * 10} requests/second")
    
    confirm = input("\n⚠️ Continue? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    # Run debug
    results = await debugger.run_debug(game_id, job_id, num_attempts, max_concurrent)
    
    # Analyze results
    debugger.analyze_results(results)


def main():
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
