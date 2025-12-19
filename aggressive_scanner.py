import requests
import threading
import time
import random
import queue
from datetime import datetime, timedelta
import concurrent.futures
import os
import sys
import json
import hashlib
import sqlite3
from collections import defaultdict, deque

class AggressiveNonUDMUXScanner:
    def __init__(self):
        self.optimize_system()
        
        # EXPANDED PROXY POOL - 20+ SOCKS5 proxies for maximum throughput
        self.proxy_pool = [
            # Original HTTP proxies
            {
                "host": "core-residential.evomi.com",
                "port": 1000,
                "user": "tapinonmam7",
                "pass": "Rilorxcb4nVVTiT3EQsv_country-ES_http3-1_session-IJHMRPCIC",
                "id": "PROXY-ES",
                "type": "http",
                "health": 100,
                "last_used": 0,
                "errors": 0,
                "success": 0,
            },
            {
                "host": "core-residential.evomi.com", 
                "port": 1000,
                "user": "tapinonmam7",
                "pass": "Rilorxcb4nVVTiT3EQsv_http3-1_session-JPL62O1N8",
                "id": "PROXY-GLOBAL-1",
                "type": "http",
                "health": 100,
                "last_used": 0,
                "errors": 0,
                "success": 0,
            },
            {
                "host": "core-residential.evomi.com",
                "port": 1000, 
                "user": "tapinonmam7",
                "pass": "Rilorxcb4nVVTiT3EQsv_http3-1_session-F5O7VT4FD",
                "id": "PROXY-GLOBAL-2",
                "type": "http",
                "health": 100,
                "last_used": 0,
                "errors": 0,
                "success": 0,
            },
            # NEW SOCKS5 PROXIES - 20 additional proxies
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-R4SJEN531", "id": "SOCKS5-01", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-4R7B80BCD", "id": "SOCKS5-02", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-SWLG822T5", "id": "SOCKS5-03", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-SJKEJMOZB", "id": "SOCKS5-04", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-9KDSMO354", "id": "SOCKS5-05", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-3CEUDK8N1", "id": "SOCKS5-06", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-STGHUIHEM", "id": "SOCKS5-07", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-JGJGNYH7W", "id": "SOCKS5-08", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-OOM3BML9H", "id": "SOCKS5-09", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-BKFI7C4CX", "id": "SOCKS5-10", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-ZA8SXQXWO", "id": "SOCKS5-11", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-MK408P5L5", "id": "SOCKS5-12", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-3NSH301AN", "id": "SOCKS5-13", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-VPSKBMDMO", "id": "SOCKS5-14", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-9GY1BWREA", "id": "SOCKS5-15", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-AV8K4P3GN", "id": "SOCKS5-16", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-ZNJ2E3KK9", "id": "SOCKS5-17", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-1P0YWI6W8", "id": "SOCKS5-18", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-XDN47YI3T", "id": "SOCKS5-19", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
            {"host": "core-residential.evomi.com", "port": 1002, "user": "tapinonmam7", "pass": "Rilorxcb4nVVTiT3EQsv_session-SAYG1PVO1", "id": "SOCKS5-20", "type": "socks5", "health": 100, "last_used": 0, "errors": 0, "success": 0},
        ]
        
        # AGGRESSIVE configuration - minimal delays, maximum throughput
        self.config = {
            'DISCOVERY_TIMEOUT': 5,
            'DETECTION_TIMEOUT': 4,
            'DISCOVERY_DELAY': 0.02,      # Very aggressive - 20ms between requests
            'DETECTION_DELAY': 0.01,       # Ultra aggressive - 10ms between checks
            'QUEUE_MAXSIZE': 500000,       # Larger queue for more servers
            'MAX_RETRIES': 5,              # Retry failed servers up to 5 times
            'RETRY_DELAY_BASE': 0.5,       # Base delay for retries
            'RETRY_DELAY_MAX': 3.0,        # Max retry delay
            'WORKERS_PER_COOKIE': 8,       # More workers per cookie
            'DISCOVERY_WORKERS_PER_PROXY': 3,  # Multiple discovery workers per proxy
            'PARALLEL_CURSORS': True,      # Use multiple cursors simultaneously
            'INFINITE_RETRY_MODE': True,   # Keep retrying until success
        }
        
        # State management
        self.cookies = []
        self.proxy_cookie_pairs = []
        self.found_count = 0
        self.total_checked = 0
        self.total_retried = 0
        self.scanned_servers = set()
        self.failed_servers = set()  # Track permanently failed servers
        self.non_udmux_servers = []
        self.udmux_servers = []
        self.proxy_stats = {}
        self.lock = threading.Lock()
        
        # Multiple queues for priority handling
        self.server_queue = queue.PriorityQueue(maxsize=self.config['QUEUE_MAXSIZE'])
        self.retry_queue = queue.Queue(maxsize=100000)  # Dedicated retry queue
        
        # Advanced components
        self.rate_limiter = AggressiveRateLimiter()
        self.edge_detector = EdgeCenterDetector()
        self.cellular_analyzer = CellularAnalyzer()
        self.performance_monitor = PerformanceMonitor()
        self.matchmaking_sim = MatchmakingSimulator()
        self.proxy_rotator = ProxyRotator(self.proxy_pool)
        
        # Initialize database
        self.init_database()
        
        print(f"🔥 AGGRESSIVE MODE: {len(self.proxy_pool)} proxies loaded")

    def optimize_system(self):
        """System optimization for maximum performance"""
        try:
            threading.stack_size(2**21)  # 2MB stack
            
            if sys.platform == "win32":
                try:
                    import psutil
                    p = psutil.Process(os.getpid())
                    p.nice(psutil.HIGH_PRIORITY_CLASS)
                    p.cpu_affinity(list(range(psutil.cpu_count())))
                    print("✅ HIGH PRIORITY + Full CPU affinity + 2MB stack")
                except ImportError:
                    print("⚠️ Install psutil for optimal performance: pip install psutil")
            else:
                try:
                    os.nice(-10)  # Higher priority on Linux
                    print("✅ Higher priority set on Linux")
                except:
                    pass
        except Exception as e:
            print(f"⚠️ System optimization: {e}")

    def init_database(self):
        """SQLite database for persistent server tracking"""
        self.db_conn = sqlite3.connect('nonudmux_servers.db', check_same_thread=False)
        self.db_lock = threading.Lock()
        
        with self.db_lock:
            cursor = self.db_conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS nonudmux_servers (
                    job_id TEXT PRIMARY KEY,
                    game_id TEXT,
                    server_ip TEXT,
                    server_port INTEGER,
                    machine_address TEXT,
                    player_count INTEGER,
                    max_players INTEGER,
                    first_seen TIMESTAMP,
                    last_seen TIMESTAMP,
                    edge_center TEXT,
                    aws_region TEXT,
                    cellular_pattern TEXT,
                    connection_quality REAL,
                    is_verified BOOLEAN DEFAULT 0
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS scan_history (
                    scan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    game_id TEXT,
                    start_time TIMESTAMP,
                    end_time TIMESTAMP,
                    total_discovered INTEGER,
                    total_checked INTEGER,
                    total_retried INTEGER,
                    nonudmux_found INTEGER,
                    udmux_found INTEGER,
                    scan_efficiency REAL
                )
            ''')
            self.db_conn.commit()

    def load_cookies_from_config(self):
        """Load cookies with support for large cookie files"""
        config_files = ['config.txt', 'Config.txt', 'CONFIG.txt', 'cookies.txt', 'Cookies.txt']
        
        for config_file in config_files:
            if os.path.exists(config_file):
                print(f"📁 Found config file: {config_file}")
                try:
                    with open(config_file, 'r', encoding='utf-8') as f:
                        lines = f.readlines()
                    
                    cookies = []
                    for i, line in enumerate(lines, 1):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            if not line.startswith('.ROBLOSECURITY='):
                                line = f".ROBLOSECURITY={line}"
                            cookies.append(line)
                    
                    if cookies:
                        print(f"🍪 Loaded {len(cookies)} cookies from {config_file}")
                        # Show first few
                        for i, cookie in enumerate(cookies[:5]):
                            print(f"   Cookie {i+1}: {cookie[:40]}...")
                        if len(cookies) > 5:
                            print(f"   ... and {len(cookies)-5} more cookies")
                        return cookies
                        
                except Exception as e:
                    print(f"❌ Error reading {config_file}: {e}")
        
        print("❌ No config file found. Create 'config.txt' with your cookies.")
        return []

    def verify_cookies(self, cookie_list):
        """Verify cookies work - parallel verification for speed"""
        print(f"\n🔍 Verifying {len(cookie_list)} cookies in parallel...")
        
        def verify_single_cookie(args):
            cookie_data, index = args
            try:
                session = requests.Session()
                session.headers.update({
                    'Cookie': cookie_data,
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                })
                
                r = session.get('https://users.roblox.com/v1/users/authenticated', timeout=10)
                if r.status_code == 200:
                    user_data = r.json()
                    username = user_data.get('name', 'Unknown')
                    user_id = user_data.get('id', 'Unknown')
                    return (True, cookie_data, f"✅ Cookie {index+1}: {username} (ID: {user_id})")
                else:
                    return (False, None, f"❌ Cookie {index+1}: HTTP {r.status_code}")
            except Exception as e:
                return (False, None, f"❌ Cookie {index+1}: {str(e)[:30]}")
        
        # Verify all cookies in parallel with more workers
        valid_cookies = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            args_list = [(cookie, i) for i, cookie in enumerate(cookie_list)]
            results = list(executor.map(verify_single_cookie, args_list))
        
        for is_valid, cookie_data, message in results:
            print(message)
            if is_valid:
                valid_cookies.append(cookie_data)
        
        print(f"\n🎯 Result: {len(valid_cookies)}/{len(cookie_list)} cookies are valid")
        return valid_cookies

    def create_proxy_cookie_pairs(self):
        """Create optimized proxy-cookie pairs with load balancing"""
        self.proxy_cookie_pairs = []
        self.proxy_stats = {}
        
        num_cookies = len(self.cookies)
        num_proxies = len(self.proxy_pool)
        
        # Create multiple pairs per proxy to maximize throughput
        # Each proxy gets cookies distributed evenly
        for i, cookie in enumerate(self.cookies):
            # Round-robin proxy assignment
            proxy = self.proxy_pool[i % num_proxies]
            pair_id = f"{proxy['id']}-C{i+1}"
            
            pair = {
                'proxy': proxy,
                'cookie': cookie,
                'pair_id': pair_id,
                'cookie_num': i + 1,
                'session': None
            }
            
            self.proxy_cookie_pairs.append(pair)
            self.proxy_stats[pair_id] = {
                "requests": 0, 
                "errors": 0, 
                "servers_found": 0,
                "retries": 0,
                "response_time_avg": 0,
                "last_success": 0
            }
        
        # Summary
        proxy_usage = defaultdict(int)
        for pair in self.proxy_cookie_pairs:
            proxy_usage[pair['proxy']['id']] += 1
        
        print(f"\n🔗 Created {len(self.proxy_cookie_pairs)} proxy-cookie pairs:")
        print(f"   {num_cookies} cookies distributed across {num_proxies} proxies")
        print(f"   Average cookies per proxy: {num_cookies/num_proxies:.1f}")
        
        for proxy_id, count in sorted(proxy_usage.items()):
            print(f"   {proxy_id}: {count} cookies")

    def aggressive_discovery_worker(self, game_id, pair, worker_id, cursor_offset=0):
        """Ultra-aggressive discovery worker with parallel cursor handling"""
        pair_id = pair['pair_id']
        proxy_session = AggressiveProxySession(
            pair['proxy'], 
            pair['cookie'], 
            self.rate_limiter, 
            self.performance_monitor
        )
        
        print(f"⚡ Discovery Worker {worker_id} started ({pair_id}) [Cursor offset: {cursor_offset}]")
        
        # Multiple strategies to hit different server pools
        strategies = [
            {'sortOrder': 1, 'excludeFullGames': 'false'},
            {'sortOrder': 2, 'excludeFullGames': 'false'},
            {'sortOrder': 1, 'excludeFullGames': 'true'},
            {'sortOrder': 2, 'excludeFullGames': 'true'},
        ]
        
        # Stagger start times
        time.sleep(worker_id * 0.05)
        
        current_strategy = (worker_id + cursor_offset) % len(strategies)
        cursor = ""
        cycle = 0
        total_discovered = 0
        consecutive_empty = 0
        max_empty_cycles = 5  # More aggressive - keep trying longer
        
        while consecutive_empty < max_empty_cycles:
            cycle += 1
            strategy = strategies[current_strategy % len(strategies)]
            
            try:
                result = proxy_session.discover_servers(game_id, cursor, strategy)
                
                with self.lock:
                    self.proxy_stats[pair_id]["requests"] += 1
                
                if result['success']:
                    servers = result['servers']
                    
                    if not servers:
                        consecutive_empty += 1
                        cursor = ""
                        current_strategy += 1
                        time.sleep(0.1)  # Brief pause before next strategy
                        continue
                    
                    new_servers = 0
                    for server in servers:
                        job_id = server.get('id')
                        player_count = server.get('playing', 0)
                        max_players = server.get('maxPlayers', 0)
                        
                        if job_id:
                            should_prioritize = self.matchmaking_sim.should_prioritize_server(server)
                            
                            with self.lock:
                                if job_id not in self.scanned_servers and job_id not in self.failed_servers:
                                    try:
                                        # Priority queue: lower number = higher priority
                                        priority = 0 if should_prioritize else 1
                                        priority_data = (priority, time.time(), {
                                            'job_id': job_id,
                                            'player_count': player_count,
                                            'max_players': max_players,
                                            'discovered_by': pair_id,
                                            'retry_count': 0
                                        })
                                        self.server_queue.put_nowait(priority_data)
                                        new_servers += 1
                                    except queue.Full:
                                        pass
                    
                    total_discovered += new_servers
                    consecutive_empty = 0
                    
                    with self.lock:
                        self.proxy_stats[pair_id]["servers_found"] += new_servers
                        self.proxy_stats[pair_id]["last_success"] = time.time()
                    
                    if cycle % 10 == 0:  # Less verbose logging
                        print(f"⚡ Worker {worker_id}: Cycle {cycle}, +{new_servers} servers, Total: {total_discovered}")
                    
                    cursor = result.get('next_cursor', '')
                    if not cursor:
                        cursor = ""
                        current_strategy += 1
                        time.sleep(0.05)
                    else:
                        time.sleep(self.config['DISCOVERY_DELAY'])
                    
                else:
                    with self.lock:
                        self.proxy_stats[pair_id]["errors"] += 1
                    
                    if result.get('retry_after'):
                        wait_time = min(float(result['retry_after']), 3)
                        time.sleep(wait_time)
                    else:
                        time.sleep(0.3)
                    
                    # Don't increment consecutive_empty on rate limits - keep trying
                    if result.get('error') != 'rate_limited':
                        consecutive_empty += 1
                    
            except Exception as e:
                with self.lock:
                    self.proxy_stats[pair_id]["errors"] += 1
                time.sleep(0.5)
                consecutive_empty += 1
        
        print(f"⚡ Discovery Worker {worker_id} ({pair_id}) FINISHED: {total_discovered} servers discovered")

    def aggressive_detection_worker(self, game_id, worker_id):
        """Aggressive detection worker with retry support"""
        worker_cookie = self.cookies[worker_id % len(self.cookies)]
        worker_proxy = self.proxy_pool[worker_id % len(self.proxy_pool)]
        
        detection_session = AggressiveDetectionSession(
            worker_cookie,
            worker_proxy,
            self.edge_detector, 
            self.cellular_analyzer, 
            self.performance_monitor
        )
        
        cookie_num = (worker_id % len(self.cookies)) + 1
        proxy_id = worker_proxy['id']
        print(f"🔍 Detection Worker {worker_id} started (Cookie {cookie_num}, {proxy_id})")
        
        processed = 0
        non_udmux_found = 0
        retried = 0
        
        while True:
            try:
                # Try main queue first
                try:
                    priority, timestamp, server_data = self.server_queue.get(timeout=1)
                except queue.Empty:
                    # Try retry queue
                    try:
                        server_data = self.retry_queue.get(timeout=5)
                        retried += 1
                    except queue.Empty:
                        continue
                
                if server_data is None:
                    break
                
                job_id = server_data['job_id']
                player_count = server_data['player_count']
                max_players = server_data['max_players']
                retry_count = server_data.get('retry_count', 0)
                
                with self.lock:
                    if job_id in self.scanned_servers:
                        continue
                    if job_id in self.failed_servers:
                        continue
                
                analysis = detection_session.analyze_server(game_id, job_id, player_count, max_players)
                processed += 1
                
                # Handle different results
                if analysis.get('status') == 'rate_limited':
                    # Re-queue for retry with backoff
                    if retry_count < self.config['MAX_RETRIES']:
                        server_data['retry_count'] = retry_count + 1
                        try:
                            self.retry_queue.put_nowait(server_data)
                            with self.lock:
                                self.total_retried += 1
                        except queue.Full:
                            pass
                    retry_after = analysis.get('retry_after', 1)
                    time.sleep(min(retry_after, 2))
                    continue
                
                if analysis.get('status') in ['error', 'exception']:
                    # Retry on errors
                    if retry_count < self.config['MAX_RETRIES']:
                        server_data['retry_count'] = retry_count + 1
                        delay = min(self.config['RETRY_DELAY_BASE'] * (2 ** retry_count), 
                                   self.config['RETRY_DELAY_MAX'])
                        time.sleep(delay * 0.1)  # Brief delay before retry
                        try:
                            self.retry_queue.put_nowait(server_data)
                            with self.lock:
                                self.total_retried += 1
                        except queue.Full:
                            pass
                    else:
                        # Max retries reached - mark as failed
                        with self.lock:
                            self.failed_servers.add(job_id)
                    continue
                
                # Mark as scanned on success
                with self.lock:
                    self.scanned_servers.add(job_id)
                    self.total_checked += 1
                
                if analysis.get('is_target_server'):
                    with self.lock:
                        self.found_count += 1
                        non_udmux_found += 1
                        
                        server_info = analysis['server_info']
                        server_ip = f"{server_info['machine_address']}:{server_info['server_port']}"
                        
                        print(f"🎯 NON-UDMUX #{self.found_count}: {server_ip} ({player_count}/{max_players}) [Edge: {analysis.get('edge_center', '?')}]")
                        
                        self.save_nonudmux_server(game_id, analysis)
                        self.save_to_file(game_id, analysis)
                        self.non_udmux_servers.append(analysis)
                
                elif analysis.get('is_udmux'):
                    self.udmux_servers.append(analysis)
                
                # Minimal delay for aggressive scanning
                time.sleep(self.config['DETECTION_DELAY'])
                
            except queue.Empty:
                # Check if we should continue
                if self.server_queue.empty() and self.retry_queue.empty():
                    time.sleep(2)
                    if self.server_queue.empty() and self.retry_queue.empty():
                        break
            except Exception as e:
                time.sleep(0.1)
        
        print(f"🔍 Detection Worker {worker_id}: {processed} analyzed, {non_udmux_found} non-UDMUX, {retried} retried")

    def retry_worker(self, game_id, worker_id):
        """Dedicated retry worker for failed servers"""
        worker_cookie = self.cookies[worker_id % len(self.cookies)]
        worker_proxy = self.proxy_pool[(worker_id + 5) % len(self.proxy_pool)]  # Different proxy rotation
        
        detection_session = AggressiveDetectionSession(
            worker_cookie,
            worker_proxy,
            self.edge_detector, 
            self.cellular_analyzer, 
            self.performance_monitor
        )
        
        print(f"🔄 Retry Worker {worker_id} started")
        
        retried = 0
        recovered = 0
        
        while True:
            try:
                server_data = self.retry_queue.get(timeout=10)
                
                if server_data is None:
                    break
                
                job_id = server_data['job_id']
                retry_count = server_data.get('retry_count', 0)
                
                with self.lock:
                    if job_id in self.scanned_servers or job_id in self.failed_servers:
                        continue
                
                # Exponential backoff delay
                delay = min(self.config['RETRY_DELAY_BASE'] * (1.5 ** retry_count), 
                           self.config['RETRY_DELAY_MAX'])
                time.sleep(delay)
                
                analysis = detection_session.analyze_server(
                    game_id, job_id, 
                    server_data['player_count'], 
                    server_data['max_players']
                )
                
                retried += 1
                
                if analysis.get('status') in ['rate_limited', 'error', 'exception']:
                    if retry_count < self.config['MAX_RETRIES']:
                        server_data['retry_count'] = retry_count + 1
                        try:
                            self.retry_queue.put_nowait(server_data)
                        except queue.Full:
                            pass
                    else:
                        with self.lock:
                            self.failed_servers.add(job_id)
                    continue
                
                # Success!
                with self.lock:
                    self.scanned_servers.add(job_id)
                    self.total_checked += 1
                    recovered += 1
                
                if analysis.get('is_target_server'):
                    with self.lock:
                        self.found_count += 1
                        server_info = analysis['server_info']
                        server_ip = f"{server_info['machine_address']}:{server_info['server_port']}"
                        print(f"🎯 RETRY SUCCESS #{self.found_count}: {server_ip}")
                        self.save_nonudmux_server(game_id, analysis)
                        self.save_to_file(game_id, analysis)
                        self.non_udmux_servers.append(analysis)
                
            except queue.Empty:
                if self.server_queue.empty():
                    break
            except Exception:
                time.sleep(0.5)
        
        print(f"🔄 Retry Worker {worker_id}: {retried} retried, {recovered} recovered")

    def save_nonudmux_server(self, game_id, analysis):
        """Save non-UDMUX server to database"""
        try:
            with self.db_lock:
                cursor = self.db_conn.cursor()
                server_info = analysis['server_info']
                
                cursor.execute('''
                    INSERT OR REPLACE INTO nonudmux_servers 
                    (job_id, game_id, server_ip, server_port, machine_address, 
                     player_count, max_players, first_seen, last_seen, 
                     edge_center, aws_region, cellular_pattern, connection_quality, is_verified)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    analysis['job_id'],
                    game_id,
                    server_info['machine_address'],
                    server_info['server_port'],
                    server_info['full_address'],
                    analysis['player_count'],
                    analysis['max_players'],
                    analysis['timestamp'],
                    analysis['timestamp'],
                    analysis.get('edge_center', 'Unknown'),
                    'aws',
                    analysis.get('port_pattern', 'unknown'),
                    analysis.get('response_time', 0),
                    1
                ))
                self.db_conn.commit()
        except Exception as e:
            pass  # Silent fail for database errors

    def save_to_file(self, game_id, analysis):
        """Save non-UDMUX server to text file"""
        filename = f"NonUDMUX_Servers_{game_id}.txt"
        
        try:
            server_info = analysis['server_info']
            join_command = f'Roblox.GameLauncher.joinGameInstance({game_id}, "{analysis["job_id"]}")'
            
            with open(filename, 'a', encoding='utf-8') as f:
                f.write(f"NON-UDMUX SERVER #{self.found_count}\n")
                f.write(f"Game ID: {game_id}\n")
                f.write(f"Job ID: {analysis['job_id']}\n")
                f.write(f"Server IP: {server_info['machine_address']}:{server_info['server_port']}\n")
                f.write(f"Players: {analysis['player_count']}/{analysis['max_players']}\n")
                f.write(f"Edge Center: {analysis.get('edge_center', 'Unknown')}\n")
                f.write(f"Response Time: {analysis.get('response_time', 0):.3f}s\n")
                f.write(f"Discovered: {analysis['timestamp']}\n")
                f.write(f"Join Command: {join_command}\n")
                f.write("-" * 70 + "\n\n")
        except:
            pass

    def run_aggressive_scan(self, game_id):
        """Main aggressive scan with all workers"""
        num_proxies = len(self.proxy_pool)
        num_cookies = len(self.cookies)
        workers_per_cookie = self.config['WORKERS_PER_COOKIE']
        discovery_per_proxy = self.config['DISCOVERY_WORKERS_PER_PROXY']
        
        total_discovery = len(self.proxy_cookie_pairs) * discovery_per_proxy
        total_detection = num_cookies * workers_per_cookie
        total_retry = max(4, num_cookies // 10)
        
        print(f"\n🚀 AGGRESSIVE NON-UDMUX SCANNER - Game {game_id}")
        print(f"🌍 Targeting AWS servers (34.x.x.x, 52.x.x.x, etc.)")
        print(f"⚡ {total_discovery} discovery workers ({num_proxies} proxies × {discovery_per_proxy})")
        print(f"🔍 {total_detection} detection workers ({num_cookies} cookies × {workers_per_cookie})")
        print(f"🔄 {total_retry} dedicated retry workers")
        print(f"📊 Queue size: {self.config['QUEUE_MAXSIZE']:,}")
        print(f"🔁 Max retries per server: {self.config['MAX_RETRIES']}")
        print("=" * 80)
        
        # Reset state
        self.found_count = 0
        self.total_checked = 0
        self.total_retried = 0
        self.scanned_servers.clear()
        self.failed_servers.clear()
        self.non_udmux_servers.clear()
        self.udmux_servers.clear()
        
        # Clear queues
        while not self.server_queue.empty():
            try:
                self.server_queue.get_nowait()
            except:
                break
        while not self.retry_queue.empty():
            try:
                self.retry_queue.get_nowait()
            except:
                break
        
        # Initialize result file
        filename = f"NonUDMUX_Servers_{game_id}.txt"
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"AGGRESSIVE NON-UDMUX SCANNER RESULTS\n")
            f.write(f"Game ID: {game_id}\n")
            f.write(f"Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Proxies: {num_proxies}\n")
            f.write(f"Cookies: {num_cookies}\n")
            f.write(f"Discovery Workers: {total_discovery}\n")
            f.write(f"Detection Workers: {total_detection}\n")
            f.write(f"Retry Workers: {total_retry}\n")
            f.write("=" * 80 + "\n\n")
        
        # Start discovery workers - multiple per proxy for maximum throughput
        discovery_threads = []
        worker_id = 0
        for pair in self.proxy_cookie_pairs:
            for cursor_offset in range(discovery_per_proxy):
                t = threading.Thread(
                    target=self.aggressive_discovery_worker, 
                    args=(game_id, pair, worker_id, cursor_offset)
                )
                t.daemon = True
                t.start()
                discovery_threads.append(t)
                worker_id += 1
        
        # Start detection workers
        detection_threads = []
        for i in range(total_detection):
            t = threading.Thread(target=self.aggressive_detection_worker, args=(game_id, i))
            t.daemon = True
            t.start()
            detection_threads.append(t)
        
        # Start retry workers
        retry_threads = []
        for i in range(total_retry):
            t = threading.Thread(target=self.retry_worker, args=(game_id, i))
            t.daemon = True
            t.start()
            retry_threads.append(t)
        
        # Monitor progress
        start_time = time.time()
        last_checked = 0
        last_found = 0
        last_report_time = time.time()
        
        try:
            while True:
                time.sleep(2)
                
                current_time = time.time()
                elapsed = current_time - start_time
                
                current_checked = self.total_checked
                current_found = self.found_count
                queue_size = self.server_queue.qsize()
                retry_size = self.retry_queue.qsize()
                
                active_discovery = sum(1 for t in discovery_threads if t.is_alive())
                active_detection = sum(1 for t in detection_threads if t.is_alive())
                active_retry = sum(1 for t in retry_threads if t.is_alive())
                
                rate = (current_checked - last_checked) / 2
                found_rate = (current_found - last_found) / 2
                last_checked = current_checked
                last_found = current_found
                
                print(f"🚀 Q:{queue_size:5d} R:{retry_size:4d} | Chk:{current_checked:5d} | "
                      f"NON:{self.found_count:3d} UDMUX:{len(self.udmux_servers):4d} | "
                      f"Rate:{rate:4.0f}/s | D/D/R:{active_discovery}/{active_detection}/{active_retry}")
                
                # Periodic detailed report
                if current_time - last_report_time > 30:
                    print("\n" + "="*80)
                    print(f"📊 STATUS REPORT (Uptime: {elapsed:.0f}s)")
                    print(f"   Servers discovered: {len(self.scanned_servers) + queue_size}")
                    print(f"   Servers checked: {self.total_checked}")
                    print(f"   Servers retried: {self.total_retried}")
                    print(f"   Failed (max retries): {len(self.failed_servers)}")
                    print(f"   NON-UDMUX found: {self.found_count}")
                    print(f"   UDMUX servers: {len(self.udmux_servers)}")
                    if self.total_checked > 0:
                        print(f"   Success rate: {(self.found_count/self.total_checked*100):.2f}%")
                    print(f"   Check rate: {self.total_checked/max(elapsed,1):.0f}/s")
                    print("="*80 + "\n")
                    last_report_time = current_time
                
                # Exit conditions
                if active_discovery == 0 and queue_size == 0 and retry_size == 0:
                    print("🎯 All queues empty, finishing...")
                    time.sleep(5)
                    break
                    
        except KeyboardInterrupt:
            print("\n⚠️ Scan interrupted by user")
        
        # Shutdown workers
        for _ in range(total_detection + total_retry + 10):
            try:
                self.server_queue.put_nowait((999, 0, None))
            except:
                pass
            try:
                self.retry_queue.put_nowait(None)
            except:
                pass
        
        # Wait for threads
        for t in detection_threads + retry_threads:
            t.join(timeout=3)
        
        elapsed_time = time.time() - start_time
        
        # Save scan history
        with self.db_lock:
            cursor = self.db_conn.cursor()
            cursor.execute('''
                INSERT INTO scan_history 
                (game_id, start_time, end_time, total_discovered, total_checked, 
                 total_retried, nonudmux_found, udmux_found, scan_efficiency)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                game_id,
                datetime.fromtimestamp(start_time).isoformat(),
                datetime.now().isoformat(),
                len(self.scanned_servers),
                self.total_checked,
                self.total_retried,
                self.found_count,
                len(self.udmux_servers),
                (self.found_count / max(self.total_checked, 1)) * 100
            ))
            self.db_conn.commit()
        
        # Final report
        with open(filename, 'a', encoding='utf-8') as f:
            f.write(f"\n" + "=" * 80 + "\n")
            f.write(f"SCAN COMPLETE - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Total time: {elapsed_time:.1f}s\n")
            f.write(f"Servers checked: {self.total_checked}\n")
            f.write(f"Servers retried: {self.total_retried}\n")
            f.write(f"Failed servers: {len(self.failed_servers)}\n")
            f.write(f"NON-UDMUX found: {self.found_count}\n")
            f.write(f"UDMUX detected: {len(self.udmux_servers)}\n")
            f.write(f"Success rate: {(self.found_count/max(self.total_checked,1)*100):.2f}%\n")
            f.write(f"Check rate: {self.total_checked/elapsed_time:.0f}/s\n")
        
        print(f"\n🎉 AGGRESSIVE SCAN COMPLETE!")
        print(f"⏱️ Time: {elapsed_time:.1f}s")
        print(f"🔍 Total checked: {self.total_checked}")
        print(f"🔄 Total retried: {self.total_retried}")
        print(f"❌ Failed (max retries): {len(self.failed_servers)}")
        print(f"🎯 NON-UDMUX found: {self.found_count}")
        print(f"📊 Success rate: {(self.found_count/max(self.total_checked,1)*100):.2f}%")
        print(f"🚀 Check rate: {self.total_checked/elapsed_time:.0f}/s")
        print(f"💾 Results saved to: {filename}")


class AggressiveRateLimiter:
    """Minimal rate limiting for aggressive mode"""
    def __init__(self):
        self.last_429 = defaultdict(float)
        self.request_counts = defaultdict(int)
        
    def can_make_request(self, endpoint, proxy_id):
        now = time.time()
        key = f"{endpoint}_{proxy_id}"
        
        # Only block if we got a 429 very recently
        if now - self.last_429[key] < 1:
            return False
        return True
    
    def record_request(self, endpoint, proxy_id, success, response_time, status_code=None):
        key = f"{endpoint}_{proxy_id}"
        self.request_counts[key] += 1
        
        if status_code == 429:
            self.last_429[key] = time.time()
    
    def get_delay(self, endpoint, proxy_id):
        key = f"{endpoint}_{proxy_id}"
        if time.time() - self.last_429[key] < 2:
            return 0.5
        return 0.01


class ProxyRotator:
    """Intelligent proxy rotation for load balancing"""
    def __init__(self, proxy_pool):
        self.proxy_pool = proxy_pool
        self.usage_counts = defaultdict(int)
        self.error_counts = defaultdict(int)
        self.last_used = defaultdict(float)
        self.lock = threading.Lock()
    
    def get_next_proxy(self):
        with self.lock:
            # Sort by usage count (least used first)
            sorted_proxies = sorted(
                self.proxy_pool,
                key=lambda p: (self.error_counts[p['id']], self.usage_counts[p['id']])
            )
            proxy = sorted_proxies[0]
            self.usage_counts[proxy['id']] += 1
            self.last_used[proxy['id']] = time.time()
            return proxy
    
    def report_error(self, proxy_id):
        with self.lock:
            self.error_counts[proxy_id] += 1
    
    def report_success(self, proxy_id):
        with self.lock:
            self.error_counts[proxy_id] = max(0, self.error_counts[proxy_id] - 1)


class EdgeCenterDetector:
    def __init__(self):
        self.edge_centers = {
            'US-East-1': {'prefixes': ['34.', '52.', '54.', '3.', '18.']},
            'US-West-2': {'prefixes': ['35.', '44.', '54.']},
            'EU-West-1': {'prefixes': ['18.', '3.', '15.', '52.']},
            'Asia-Pacific': {'prefixes': ['13.', '52.', '54.']},
        }
        self.server_distribution = defaultdict(int)
        self.port_analysis = defaultdict(int)
    
    def detect_edge_center(self, server_ip):
        if not server_ip:
            return "Unknown"
        for center_name, info in self.edge_centers.items():
            for prefix in info['prefixes']:
                if server_ip.startswith(prefix):
                    self.server_distribution[center_name] += 1
                    return center_name
        self.server_distribution["Unknown"] += 1
        return "Unknown"
    
    def analyze_port_patterns(self, port):
        self.port_analysis[port] += 1
        if 53640 <= port <= 53660:
            return "legacy_range_1"
        elif 64000 <= port <= 65000:
            return "legacy_range_2"
        elif 56000 <= port <= 57000:
            return "udmux_range"
        return f"custom"


class CellularAnalyzer:
    def __init__(self):
        self.ip_clusters = defaultdict(list)
        
    def analyze_server_clustering(self, servers):
        for server in servers:
            if 'machine_address' in server:
                ip = server['machine_address']
                ip_parts = ip.split('.')
                if len(ip_parts) >= 3:
                    subnet = '.'.join(ip_parts[:3])
                    self.ip_clusters[subnet].append(server)


class PerformanceMonitor:
    def __init__(self):
        self.start_time = time.time()
        self.metrics = defaultdict(list)
        
    def record_discovery(self, proxy_id, count, response_time):
        self.metrics['discovery'].append((time.time(), count))
    
    def record_detection(self, proxy_id, success, response_time):
        self.metrics['detection'].append((time.time(), 1 if success else 0))


class MatchmakingSimulator:
    def should_prioritize_server(self, server_info):
        player_count = server_info.get('playing', 0)
        max_players = server_info.get('maxPlayers', 0)
        if max_players > 0 and player_count >= max_players:
            return False
        return 1 <= player_count <= 30


class AggressiveProxySession:
    """Aggressive proxy session with minimal delays"""
    def __init__(self, proxy_config, cookie, rate_limiter, performance_monitor):
        self.proxy_config = proxy_config
        self.cookie = cookie
        self.rate_limiter = rate_limiter
        self.performance_monitor = performance_monitor
        self.session = requests.Session()
        self.consecutive_errors = 0
        
        # Build proxy URL based on type
        proxy_type = proxy_config.get('type', 'http')
        if proxy_type == 'socks5':
            proxy_url = f"socks5://{proxy_config['user']}:{proxy_config['pass']}@{proxy_config['host']}:{proxy_config['port']}"
        else:
            proxy_url = f"http://{proxy_config['user']}:{proxy_config['pass']}@{proxy_config['host']}:{proxy_config['port']}"
        
        self.session.proxies = {'http': proxy_url, 'https': proxy_url}
        
        # Aggressive connection pooling
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=100,
            pool_maxsize=200,
            max_retries=0,
            pool_block=False
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
            'Accept': 'application/json',
            'Cookie': cookie,
            'Connection': 'keep-alive',
        })
    
    def discover_servers(self, game_id, cursor="", strategy=None):
        start_time = time.time()
        
        try:
            url = f'https://games.roblox.com/v1/games/{game_id}/servers/0'
            params = {
                'sortOrder': strategy.get('sortOrder', 1) if strategy else 1,
                'excludeFullGames': strategy.get('excludeFullGames', 'false') if strategy else 'false',
                'limit': 100,
                'cursor': cursor
            }
            
            response = self.session.get(url, params=params, timeout=5)
            response_time = time.time() - start_time
            
            if response.status_code == 200:
                data = response.json()
                self.consecutive_errors = 0
                return {
                    'success': True,
                    'servers': data.get('data', []),
                    'next_cursor': data.get('nextPageCursor', ''),
                    'response_time': response_time
                }
            else:
                self.consecutive_errors += 1
                return {
                    'success': False,
                    'error': 'rate_limited' if response.status_code == 429 else f"HTTP {response.status_code}",
                    'retry_after': response.headers.get('Retry-After', 1)
                }
                
        except Exception as e:
            self.consecutive_errors += 1
            return {'success': False, 'error': str(e)}
    
    def is_healthy(self):
        return self.consecutive_errors < 10


class AggressiveDetectionSession:
    """Aggressive detection session with proxy support"""
    def __init__(self, cookie, proxy_config, edge_detector, cellular_analyzer, performance_monitor):
        self.cookie = cookie
        self.proxy_config = proxy_config
        self.edge_detector = edge_detector
        self.cellular_analyzer = cellular_analyzer
        self.performance_monitor = performance_monitor
        self.session = requests.Session()
        
        # Build proxy URL
        proxy_type = proxy_config.get('type', 'http')
        if proxy_type == 'socks5':
            proxy_url = f"socks5://{proxy_config['user']}:{proxy_config['pass']}@{proxy_config['host']}:{proxy_config['port']}"
        else:
            proxy_url = f"http://{proxy_config['user']}:{proxy_config['pass']}@{proxy_config['host']}:{proxy_config['port']}"
        
        self.session.proxies = {'http': proxy_url, 'https': proxy_url}
        
        adapter = requests.adapters.HTTPAdapter(
            pool_connections=50,
            pool_maxsize=100,
            max_retries=0,
            pool_block=False
        )
        self.session.mount('http://', adapter)
        self.session.mount('https://', adapter)
        
        self.session.headers.update({
            'Content-Type': 'application/json',
            'User-Agent': 'Roblox/WinInet',
            'Cookie': cookie,
            'Connection': 'keep-alive'
        })
    
    def analyze_server(self, game_id, job_id, player_count, max_players):
        start_time = time.time()
        
        try:
            payload = {
                'placeId': int(game_id),
                'gameId': job_id,
                'isPlayTogetherGame': False
            }
            
            response = self.session.post(
                'https://gamejoin.roblox.com/v1/join-game-instance',
                json=payload,
                timeout=4
            )
            
            response_time = time.time() - start_time
            
            if response.status_code == 429:
                return {
                    'status': 'rate_limited',
                    'retry_after': int(response.headers.get('Retry-After', 1))
                }
            
            if response.status_code != 200:
                return {'status': 'error', 'code': response.status_code}
            
            data = response.json()
            join_script = data.get('joinScript', {})
            
            analysis = {
                'job_id': job_id,
                'player_count': player_count,
                'max_players': max_players,
                'response_time': response_time,
                'timestamp': datetime.now().isoformat(),
                'is_udmux': False,
                'is_target_server': False,
                'server_info': {}
            }
            
            if join_script:
                udmux_endpoints = join_script.get('UdmuxEndpoints')
                if udmux_endpoints:
                    analysis['is_udmux'] = True
                else:
                    machine_address = join_script.get('MachineAddress', '')
                    server_port = join_script.get('ServerPort', 0)
                    
                    if machine_address and server_port:
                        analysis['server_info'] = {
                            'machine_address': machine_address,
                            'server_port': server_port,
                            'full_address': f"{machine_address}:{server_port}",
                            'data_center_id': join_script.get('DataCenterId', ''),
                            'country_code': join_script.get('CountryCode', ''),
                        }
                        
                        analysis['edge_center'] = self.edge_detector.detect_edge_center(machine_address)
                        analysis['port_pattern'] = self.edge_detector.analyze_port_patterns(server_port)
                        analysis['is_target_server'] = True
            
            return analysis
            
        except Exception as e:
            return {'status': 'exception', 'error': str(e)}


def main():
    print("🔥 AGGRESSIVE NON-UDMUX SCANNER")
    print("🎯 Maximum throughput mode with 23 proxies")
    print("🔄 Automatic retry for failed servers")
    print("🌍 Multi-proxy, Multi-cookie, Multi-threaded")
    print("=" * 80)
    
    # Check for PySocks
    try:
        import socks
        print("✅ PySocks installed - SOCKS5 proxies enabled")
    except ImportError:
        print("⚠️ Installing PySocks for SOCKS5 support...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "PySocks", "-q"])
        print("✅ PySocks installed")
    
    scanner = AggressiveNonUDMUXScanner()
    
    cookies = scanner.load_cookies_from_config()
    if not cookies:
        input("❌ No cookies found. Press Enter to exit...")
        return
    
    valid_cookies = scanner.verify_cookies(cookies)
    if not valid_cookies:
        input("❌ No valid cookies. Press Enter to exit...")
        return
    
    scanner.cookies = valid_cookies
    scanner.create_proxy_cookie_pairs()
    
    print("\n" + "="*80)
    game_id = input('🎮 Enter Game ID to scan: ').strip()
    
    if not game_id.isdigit():
        print("❌ Invalid game ID")
        return
    
    num_proxies = len(scanner.proxy_pool)
    num_cookies = len(valid_cookies)
    
    print(f"\n✅ AGGRESSIVE SCANNER READY!")
    print(f"🍪 {num_cookies} valid cookies")
    print(f"🌐 {num_proxies} proxies (3 HTTP + 20 SOCKS5)")
    print(f"⚡ {len(scanner.proxy_cookie_pairs) * 3} discovery workers")
    print(f"🔍 {num_cookies * 8} detection workers")
    print(f"🔄 {max(4, num_cookies // 10)} retry workers")
    print(f"🎯 Target: NON-UDMUX AWS servers")
    
    input("\n🚀 Press Enter to start AGGRESSIVE scan...")
    
    scanner.run_aggressive_scan(game_id)


if __name__ == "__main__":
    main()
