import requests
import threading
import time
import queue
from datetime import datetime
import json
import re
import os
from collections import defaultdict
import concurrent.futures

# SOCKS5 support
try:
    import socks
    SOCKS5_AVAILABLE = True
except ImportError:
    SOCKS5_AVAILABLE = False
    print("⚠️ Install PySocks for SOCKS5 support: pip install pysocks requests[socks]")

class ServerDebugger:
    def __init__(self):
        self.proxy_pool = self.load_all_proxies()
        self.cookies = []
        self.results = []
        self.lock = threading.Lock()
        
    def load_all_proxies(self):
        """Load all proxies including SOCKS5"""
        proxies = [
            # Original HTTP proxies
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
        
        # Add all SOCKS5 proxies
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
    
    def create_session(self, proxy_config, cookie):
        """Create a requests session with proxy and cookie (AGGRESSIVE)"""
        session = requests.Session()
        
        # Setup proxy based on type
        if proxy_config['type'] == 'socks5':
            if not SOCKS5_AVAILABLE:
                return None
            proxy_url = f"socks5://{proxy_config['user']}:{proxy_config['pass']}@{proxy_config['host']}:{proxy_config['port']}"
            session.proxies = {'http': proxy_url, 'https': proxy_url}
        else:
            proxy_url = f"http://{proxy_config['user']}:{proxy_config['pass']}@{proxy_config['host']}:{proxy_config['port']}"
            session.proxies = {'http': proxy_url, 'https': proxy_url}
        
        # Aggressive adapter settings
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=10,
            pool_maxsize=20,
            max_retries=0,
            pool_block=False
        )
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Roblox/WinInet',
            'Cookie': cookie,
            'Connection': 'keep-alive'
        })
        
        return session
    
    def test_server(self, game_id, job_id, proxy_config, cookie, cookie_num, attempt_num=1):
        """Test a single server with specific proxy and cookie"""
        session = self.create_session(proxy_config, cookie)
        if not session:
            return None
        
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
        
        try:
            payload = {
                'placeId': int(game_id),
                'gameId': job_id,
                'isPlayTogetherGame': False
            }
            
            response = session.post(
                'https://gamejoin.roblox.com/v1/join-game-instance',
                json=payload,
                timeout=3  # Reduced timeout for faster failures
            )
            
            result['response_time'] = time.time() - start_time
            result['status_code'] = response.status_code
            result['response_headers'] = dict(response.headers)
            
            if response.status_code == 200:
                try:
                    data = response.json()
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
                except json.JSONDecodeError:
                    result['error'] = 'Invalid JSON response'
                    result['response_body'] = response.text[:500]
            elif response.status_code == 429:
                result['error'] = 'Rate Limited'
                retry_after = response.headers.get('Retry-After', 'Unknown')
                result['retry_after'] = retry_after
            elif response.status_code == 400:
                result['error'] = 'Bad Request'
                try:
                    result['response_body'] = response.json()
                except:
                    result['response_body'] = response.text[:500]
            elif response.status_code == 403:
                result['error'] = 'Forbidden'
            elif response.status_code == 404:
                result['error'] = 'Server Not Found'
            elif response.status_code == 500:
                result['error'] = 'Server Error'
            else:
                result['error'] = f'HTTP {response.status_code}'
                try:
                    result['response_body'] = response.text[:500]
                except:
                    pass
                    
        except requests.exceptions.Timeout:
            result['error'] = 'Timeout'
            result['response_time'] = time.time() - start_time
        except requests.exceptions.ConnectionError as e:
            result['error'] = f'Connection Error: {str(e)[:100]}'
            result['response_time'] = time.time() - start_time
        except Exception as e:
            result['error'] = f'Exception: {str(e)[:100]}'
            result['response_time'] = time.time() - start_time
        
        finally:
            session.close()
        
        return result
    
    def run_debug(self, game_id, job_id, num_attempts=1, max_workers=200):
        """Run debug test with all proxy-cookie combinations (AGGRESSIVE PARALLEL)"""
        print(f"\n{'='*80}")
        print(f"🔍 SERVER DEBUGGER (AGGRESSIVE MODE)")
        print(f"{'='*80}")
        print(f"Game ID: {game_id}")
        print(f"Job ID: {job_id}")
        print(f"Proxies: {len(self.proxy_pool)}")
        print(f"Cookies: {len(self.cookies)}")
        print(f"Total Combinations: {len(self.proxy_pool) * len(self.cookies)}")
        print(f"Attempts per combination: {num_attempts}")
        print(f"Max Workers (Parallel): {max_workers}")
        print(f"{'='*80}\n")
        
        results = []
        total_tests = len(self.proxy_pool) * len(self.cookies) * num_attempts
        completed = [0]  # Use list for thread-safe counter
        start_time = time.time()
        lock = threading.Lock()
        
        # Prepare all test tasks
        tasks = []
        for proxy in self.proxy_pool:
            for cookie_idx, cookie in enumerate(self.cookies):
                for attempt in range(1, num_attempts + 1):
                    tasks.append((game_id, job_id, proxy, cookie, cookie_idx + 1, attempt))
        
        def worker(task):
            game_id, job_id, proxy, cookie, cookie_num, attempt_num = task
            result = self.test_server(game_id, job_id, proxy, cookie, cookie_num, attempt_num)
            
            with lock:
                completed[0] += 1
                if result:
                    results.append(result)
                
                if completed[0] % 50 == 0 or completed[0] == total_tests:
                    elapsed = time.time() - start_time
                    rate = completed[0] / elapsed if elapsed > 0 else 0
                    remaining = total_tests - completed[0]
                    eta = remaining / rate if rate > 0 else 0
                    print(f"⏳ Progress: {completed[0]}/{total_tests} ({completed[0]*100//total_tests}%) | "
                          f"Rate: {rate:.0f}/s | ETA: {eta:.0f}s | "
                          f"Success: {len([r for r in results if r.get('success')])} | "
                          f"Errors: {len([r for r in results if not r.get('success')])}", end='\r')
        
        # Run all tasks in parallel
        print(f"🚀 Starting {len(tasks)} tests with {max_workers} parallel workers...\n")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            executor.map(worker, tasks)
        
        elapsed_time = time.time() - start_time
        print(f"\n✅ Completed {completed[0]} tests in {elapsed_time:.1f} seconds")
        print(f"⚡ Average rate: {completed[0]/elapsed_time:.0f} requests/second\n")
        
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
        filename = f"debug_results_{job_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, default=str)
        print(f"💾 Detailed results saved to: {filename}")
        print(f"{'='*80}\n")


def main():
    import os
    
    print("🔍 SERVER DEBUGGER")
    print("=" * 80)
    print("This tool tests a specific server (JOB ID) with all proxies and cookies")
    print("to see how the server reacts to different requests.")
    print("=" * 80)
    
    debugger = ServerDebugger()
    
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
    
    max_workers_input = input(f"⚡ Max parallel workers (default 200, recommended 100-300): ").strip()
    max_workers = int(max_workers_input) if max_workers_input.isdigit() else 200
    
    print(f"\n🚀 Starting AGGRESSIVE debug test...")
    print(f"   Total tests: {len(debugger.proxy_pool) * len(cookies) * num_attempts}")
    print(f"   Parallel workers: {max_workers}")
    print(f"   Expected speed: ~{max_workers * 2}-{max_workers * 5} requests/second")
    
    confirm = input("\n⚠️ Continue? (y/n): ").strip().lower()
    if confirm != 'y':
        print("❌ Cancelled")
        return
    
    # Run debug
    results = debugger.run_debug(game_id, job_id, num_attempts, max_workers)
    
    # Analyze results
    debugger.analyze_results(results)


if __name__ == "__main__":
    main()
