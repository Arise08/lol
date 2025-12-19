
import sys
import os
import requests
import threading
import time
import random
import queue
from datetime import datetime, timedelta
import concurrent.futures
import json
import hashlib
import sqlite3
import re
from collections import defaultdict, deque
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Set, Tuple, Any
from enum import Enum

# Windows console setup
if sys.platform == "win32":
    os.system('')

# =============================================================================
# ANSI COLOR CODES
# =============================================================================
class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    DIM = '\033[2m'
    RESET = '\033[0m'
    
    @staticmethod
    def success(text): return f"{Colors.GREEN}{text}{Colors.RESET}"
    @staticmethod
    def error(text): return f"{Colors.RED}{text}{Colors.RESET}"
    @staticmethod
    def warning(text): return f"{Colors.YELLOW}{text}{Colors.RESET}"
    @staticmethod
    def info(text): return f"{Colors.CYAN}{text}{Colors.RESET}"
    @staticmethod
    def highlight(text): return f"{Colors.BOLD}{Colors.WHITE}{text}{Colors.RESET}"
    @staticmethod
    def target(text): return f"{Colors.BOLD}{Colors.GREEN}{text}{Colors.RESET}"
    @staticmethod
    def dim(text): return f"{Colors.DIM}{text}{Colors.RESET}"

def print_banner():
    banner = f"""
{Colors.CYAN}{'='*80}
{Colors.BOLD}                    NON-UDMUX SERVER SCANNER v3.0 (Advanced)
{Colors.RESET}{Colors.CYAN}{'='*80}
{Colors.WHITE}  Target: AWS direct-connection servers
  Features: Smart Cookie Rotation, Auto-Retry, Status 22 Handling
{'='*80}{Colors.RESET}
"""
    print(banner)

def print_section(title):
    print(f"\n{Colors.CYAN}{'─'*80}")
    print(f"{Colors.BOLD}{Colors.WHITE}  {title}")
    print(f"{Colors.CYAN}{'─'*80}{Colors.RESET}")

# =============================================================================
# CONFIGURATION
# =============================================================================
@dataclass
class ScannerConfig:
    discovery_timeout: float = 5.0
    detection_timeout: float = 6.0
    
    # Delays
    discovery_delay: float = 0.15
    detection_delay: float = 0.05
    
    # Queue
    queue_maxsize: int = 500000
    
    # Concurrency
    max_threads: int = 100  # Total worker threads cap
    
    # Retry Logic
    max_retries: int = 5
    max_job_retries: int = 3  # How many times to retry a specific server if it returns Status 22
    
    # Cooldowns
    cookie_cooldown_success: float = 2.0  # Seconds to wait before reusing a cookie after success
    cookie_cooldown_error: float = 10.0   # Seconds to wait after rate limit/error
    
    # Discovery
    exhaust_all_cursors: bool = True

# =============================================================================
# PROXY MANAGER
# =============================================================================
class ProxyPool:
    def __init__(self, proxy_file='proxies.txt'):
        self.proxies = []
        self.lock = threading.Lock()
        self._load_proxies(proxy_file)
        
    def _load_proxies(self, path):
        if not os.path.exists(path):
            # Fallback to hardcoded for demo/testing if file missing
            self.proxies = [
                self._make_proxy_dict("core-residential.evomi.com", 1000, "tapinonmam7", "Rilorxcb4nVVTiT3EQsv", "ES"),
                self._make_proxy_dict("core-residential.evomi.com", 1000, "tapinonmam7", "Rilorxcb4nVVTiT3EQsv", "Global"),
            ]
            return

        with open(path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'): continue
                
                # Format: host:port:user:pass or user:pass@host:port
                try:
                    if '@' in line:
                        userpass, hostport = line.split('@')
                        user, password = userpass.split(':')
                        host, port = hostport.split(':')
                    elif line.count(':') == 3:
                        host, port, user, password = line.split(':')
                    else:
                        continue
                        
                    self.proxies.append(self._make_proxy_dict(host, int(port), user, password, "File"))
                except:
                    pass
        
        print(Colors.info(f"[Proxy] Loaded {len(self.proxies)} proxies"))

    def _make_proxy_dict(self, host, port, user, base_pass, region):
        session_id = hashlib.md5(str(time.time() + random.random()).encode()).hexdigest()[:8]
        # Handle Evomi specific session logic if needed, otherwise use as is
        # For general compatibility, we'll store basic auth
        return {
            "host": host, "port": port, "user": user, "pass": base_pass,
            "id": f"{host[:10]}-{session_id}",
            "health": 100, "errors": 0, "last_used": 0
        }

    def get_proxy(self):
        with self.lock:
            if not self.proxies: return None
            # Simple Round Robin or Random
            return random.choice(self.proxies)
            
    def get_formatted_proxy(self, proxy):
        return f"http://{proxy['user']}:{proxy['pass']}@{proxy['host']}:{proxy['port']}"

# =============================================================================
# COOKIE / ACCOUNT MANAGER
# =============================================================================
class CookieManager:
    """Manages a pool of cookies, handling rotation and cooldowns"""
    def __init__(self, cookies: List[str], config: ScannerConfig):
        self.config = config
        self.cookies = []
        self.lock = threading.Lock()
        
        for i, c in enumerate(cookies):
            self.cookies.append({
                'cookie': c,
                'id': i,
                'ready_at': 0,
                'errors': 0,
                'csrf_token': None,
                'user_agent': f'Roblox/WinInet (Scanner v3; {i})'
            })
            
    def get_cookie(self) -> Optional[Dict]:
        """Returns a cookie that is ready to use. Returns None if all are busy."""
        now = time.time()
        best_cookie = None
        
        with self.lock:
            # Find a cookie where ready_at <= now
            available = [c for c in self.cookies if c['ready_at'] <= now]
            
            if available:
                # Pick one with least errors or random
                best_cookie = random.choice(available)
                # Mark it as busy briefly to prevent immediate reuse by another thread
                # The worker should update the ready_at when done
                best_cookie['ready_at'] = now + 1.0 
                return best_cookie
                
        return None

    def release_cookie(self, cookie_id: int, status: str, backoff_mult: float = 1.0):
        """
        status: 'success', 'rate_limit', 'error'
        """
        now = time.time()
        with self.lock:
            for c in self.cookies:
                if c['id'] == cookie_id:
                    if status == 'success':
                        c['ready_at'] = now + self.config.cookie_cooldown_success
                        c['errors'] = max(0, c['errors'] - 1)
                    elif status == 'rate_limit':
                        # Status 22 or 429
                        wait = self.config.cookie_cooldown_error * backoff_mult
                        c['ready_at'] = now + wait
                        c['errors'] += 1
                    else: # error
                        c['ready_at'] = now + 1.0
                        c['errors'] += 1
                    break
    
    def update_csrf(self, cookie_id: int, token: str):
        with self.lock:
            for c in self.cookies:
                if c['id'] == cookie_id:
                    c['csrf_token'] = token
                    break

# =============================================================================
# SERVER ANALYZER
# =============================================================================
class ServerAnalyzer:
    # (Same logic as before, condensed for brevity but fully functional)
    UDMUX_PATTERNS = {'internal_ip': r'^10\.', 'udmux_ranges': ['128.116.']}
    AWS_PREFIXES = ['34.', '35.', '44.', '52.', '54.', '3.', '13.', '15.', '18.', '98.']
    
    def is_udmux_server(self, join_data: dict) -> Tuple[bool, dict]:
        join_script = join_data.get('joinScript', {})
        if not join_script: return True, {'reason': 'no_joinscript'}
        
        # Check UdmuxEndpoints
        if join_script.get('UdmuxEndpoints'):
            return True, {'reason': 'udmux_endpoints_present'}
            
        machine_address = join_script.get('MachineAddress', '')
        if not machine_address or machine_address.startswith('10.'):
            return True, {'reason': 'internal_ip'}
            
        # Check AWS
        is_aws = any(machine_address.startswith(p) for p in self.AWS_PREFIXES)
        
        return False, {
            'reason': 'direct_connection',
            'server_info': {
                'ip': machine_address,
                'port': join_script.get('ServerPort'),
                'id': join_script.get('MachineAddress')
            },
            'is_aws': is_aws
        }

# =============================================================================
# DATABASE
# =============================================================================
class DatabaseManager:
    def __init__(self, db_path='scanner_v3.db'):
        self.db_path = db_path
        self.lock = threading.Lock()
        self._init_db()
        
    def _init_db(self):
        with sqlite3.connect(self.db_path) as conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS servers 
                          (job_id TEXT PRIMARY KEY, ip TEXT, port INTEGER, 
                           game_id TEXT, timestamp TIMESTAMP)''')
    
    def save_server(self, data):
        with self.lock:
            with sqlite3.connect(self.db_path) as conn:
                conn.execute('INSERT OR REPLACE INTO servers VALUES (?,?,?,?,?)',
                           (data['job_id'], data['ip'], data['port'], 
                            data['game_id'], datetime.now()))

# =============================================================================
# DISCOVERY WORKER
# =============================================================================
class DiscoveryWorker:
    def __init__(self, worker_id, proxy_pool, cookie_manager, queue, seen_set, stats, game_id, config):
        self.id = worker_id
        self.proxy_pool = proxy_pool
        self.cookie_manager = cookie_manager
        self.queue = queue
        self.seen = seen_set
        self.stats = stats
        self.game_id = game_id
        self.config = config
        self.running = True

    def run(self):
        # Discovery uses a dedicated cookie or rotates? 
        # For simplicity, let's grab one cookie per worker loop
        cursor = None
        
        while self.running:
            cookie_data = self.cookie_manager.get_cookie()
            if not cookie_data:
                time.sleep(1)
                continue
                
            proxy = self.proxy_pool.get_proxy()
            if not proxy: 
                time.sleep(1)
                continue
                
            try:
                url = f'https://games.roblox.com/v1/games/{self.game_id}/servers/0'
                params = {'limit': 100, 'excludeFullGames': 'false'}
                if cursor: params['cursor'] = cursor
                
                proxies = {'https': self.proxy_pool.get_formatted_proxy(proxy)}
                headers = {'Cookie': cookie_data['cookie']}
                
                resp = requests.get(url, params=params, headers=headers, proxies=proxies, timeout=5)
                
                if resp.status_code == 200:
                    data = resp.json()
                    servers = data.get('data', [])
                    
                    for s in servers:
                        jid = s.get('id')
                        if jid and jid not in self.seen:
                            self.seen.add(jid)
                            self.queue.put({
                                'job_id': jid,
                                'retries': 0,
                                'player_count': s.get('playing', 0),
                                'max_players': s.get('maxPlayers', 0)
                            })
                            self.stats['discovered'] += 1
                            
                    cursor = data.get('nextPageCursor')
                    if not cursor and self.config.exhaust_all_cursors:
                        break # Done
                        
                    self.cookie_manager.release_cookie(cookie_data['id'], 'success')
                elif resp.status_code == 429:
                    self.cookie_manager.release_cookie(cookie_data['id'], 'rate_limit')
                    time.sleep(1)
                else:
                    self.cookie_manager.release_cookie(cookie_data['id'], 'error')
                    
            except Exception as e:
                self.cookie_manager.release_cookie(cookie_data['id'], 'error')
                
            time.sleep(self.config.discovery_delay)

# =============================================================================
# DETECTION WORKER
# =============================================================================
class DetectionWorker:
    def __init__(self, worker_id, proxy_pool, cookie_manager, queue, db, stats, game_id, config):
        self.id = worker_id
        self.proxy_pool = proxy_pool
        self.cookie_manager = cookie_manager
        self.queue = queue
        self.db = db
        self.stats = stats
        self.game_id = game_id
        self.config = config
        self.running = True
        self.analyzer = ServerAnalyzer()

    def run(self):
        while self.running:
            try:
                # 1. Get Job
                try:
                    job = self.queue.get(timeout=1)
                except queue.Empty:
                    if not self.running: break
                    continue
                
                # 2. Get Cookie
                cookie_data = self.cookie_manager.get_cookie()
                if not cookie_data:
                    # No cookies available, put job back and wait
                    self.queue.put(job)
                    time.sleep(0.5)
                    continue

                # 3. Process
                self._process_job(job, cookie_data)
                
            except Exception as e:
                print(f"Worker {self.id} error: {e}")

    def _process_job(self, job, cookie_data):
        job_id = job['job_id']
        proxy = self.proxy_pool.get_proxy()
        
        session = requests.Session()
        session.cookies.update({'.ROBLOSECURITY': cookie_data['cookie'].replace('.ROBLOSECURITY=', '')})
        session.headers.update({
            'User-Agent': cookie_data['user_agent'],
            'Referer': f'https://www.roblox.com/games/{self.game_id}/',
            'Origin': 'https://www.roblox.com'
        })
        
        if cookie_data['csrf_token']:
            session.headers['X-CSRF-TOKEN'] = cookie_data['csrf_token']
            
        proxy_url = self.proxy_pool.get_formatted_proxy(proxy)
        session.proxies = {'http': proxy_url, 'https': proxy_url}

        try:
            payload = {'placeId': int(self.game_id), 'gameId': job_id, 'isTeleport': False}
            url = 'https://gamejoin.roblox.com/v1/join-game-instance'
            
            resp = session.post(url, json=payload, timeout=self.config.detection_timeout)
            
            # Handle CSRF
            if resp.status_code == 403 and 'X-CSRF-TOKEN' in resp.headers:
                token = resp.headers['X-CSRF-TOKEN']
                self.cookie_manager.update_csrf(cookie_data['id'], token)
                session.headers['X-CSRF-TOKEN'] = token
                resp = session.post(url, json=payload, timeout=self.config.detection_timeout)

            # Analyze Response
            if resp.status_code == 200:
                data = resp.json()
                
                # Check for Status 22 / Flooded in Body
                if data.get('jobId') is None and (data.get('status') == 22 or data.get('message') == 'Flooded'):
                    self._handle_retry(job, cookie_data, 'rate_limit')
                    return

                is_udmux, info = self.analyzer.is_udmux_server(data)
                self.stats['checked'] += 1
                
                if not is_udmux:
                    self.stats['nonudmux'] += 1
                    s_info = info['server_info']
                    print(Colors.target(f"[FOUND] {s_info['ip']}:{s_info['port']} (Players: {job.get('player_count')})"))
                    self.db.save_server({
                        'job_id': job_id, 'ip': s_info['ip'], 'port': s_info['port'], 
                        'game_id': self.game_id
                    })
                else:
                    self.stats['udmux'] += 1
                
                self.cookie_manager.release_cookie(cookie_data['id'], 'success')
                
            elif resp.status_code == 429:
                self._handle_retry(job, cookie_data, 'rate_limit')
            else:
                # Generic error, maybe invalid cookie or server issue
                self.cookie_manager.release_cookie(cookie_data['id'], 'error')
                
        except Exception as e:
            self._handle_retry(job, cookie_data, 'error')

    def _handle_retry(self, job, cookie_data, status):
        """Put job back in queue if retries remain"""
        self.cookie_manager.release_cookie(cookie_data['id'], status)
        
        if job['retries'] < self.config.max_job_retries:
            job['retries'] += 1
            # Add a small delay/jitter to this job so we don't spam it immediately
            # In a real priority queue we'd set a time, but here we just put it at the back
            self.queue.put(job)

# =============================================================================
# MAIN CLASS
# =============================================================================
class ScannerV3:
    def __init__(self):
        self.config = ScannerConfig()
        self.stats = defaultdict(int)
        self.seen_jobs = set()
        self.job_queue = queue.Queue(maxsize=self.config.queue_maxsize)
        self.db = DatabaseManager()
        self.proxy_pool = ProxyPool()
        
    def load_cookies(self):
        cookies = []
        if os.path.exists('config.txt'):
            with open('config.txt', 'r') as f:
                for line in f:
                    if '_|WARNING:-DO-NOT-SHARE-THIS.' in line:
                        cookies.append(line.strip())
        return cookies

    def start(self):
        print_banner()
        cookies = self.load_cookies()
        if not cookies:
            print(Colors.error("No cookies found in config.txt"))
            return

        print(Colors.info(f"Loaded {len(cookies)} cookies"))
        game_id = input(f"{Colors.CYAN}Enter Game ID: {Colors.RESET}").strip()
        
        self.cookie_manager = CookieManager(cookies, self.config)
        
        # Start Discovery
        print_section("STARTING DISCOVERY")
        d_worker = DiscoveryWorker(0, self.proxy_pool, self.cookie_manager, 
                                 self.job_queue, self.seen_jobs, self.stats, game_id, self.config)
        threading.Thread(target=d_worker.run, daemon=True).start()
        
        # Start Detection Workers
        # We cap threads but ensure we use our cookies efficiently
        num_workers = min(self.config.max_threads, len(cookies) * 5)
        print(Colors.info(f"Spawning {num_workers} detection workers..."))
        
        workers = []
        for i in range(num_workers):
            w = DetectionWorker(i, self.proxy_pool, self.cookie_manager,
                              self.job_queue, self.db, self.stats, game_id, self.config)
            t = threading.Thread(target=w.run, daemon=True)
            t.start()
            workers.append(w)
            
        # Monitor
        start_time = time.time()
        try:
            while True:
                time.sleep(1)
                elapsed = time.time() - start_time
                q_size = self.job_queue.qsize()
                
                print(f"\rQueue: {q_size} | Checked: {self.stats['checked']} | "
                      f"Found: {Colors.GREEN}{self.stats['nonudmux']}{Colors.RESET} | "
                      f"UDMUX: {Colors.RED}{self.stats['udmux']}{Colors.RESET} | "
                      f"Rate: {self.stats['checked']/elapsed:.1f}/s", end="")
                      
                if q_size == 0 and elapsed > 10 and self.stats['discovered'] > 0:
                    # Simple exit condition for demo
                    pass
                    
        except KeyboardInterrupt:
            print("\nStopping...")

if __name__ == "__main__":
    ScannerV3().start()
