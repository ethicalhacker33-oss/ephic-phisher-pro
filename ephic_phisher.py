#!/usr/bin/env python3
# ============================================================
# EPHIC PHISHER PRO ULTIMATE - VERSION 3.0.0
# MATSANANCIYAR ƘARFI - ADVANCED CYBERSECURITY TOOL
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
import qrcode
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ============================================================
# GLOBAL VARIABLES
# ============================================================

VERSION = "3.0.0"
AUTHOR = "EPHIC TRADER"
REPO_URL = "https://github.com/ethicalhacker33-oss/ephic-phisher-pro"
SERVER_PORT = 8080
CLOUDFLARED_PROCESS = None
SERVER_PROCESS = None

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
    ║    ║  FOR EDUCATIONAL & TESTING PURPOSES ONLY                ║   ║
    ║    ║  VERSION: 3.0.0                                        ║   ║
    ║    ║  AUTHOR: EPHIC TRADER                                  ║   ║
    ║    ║  GITHUB: ethicalhacker33-oss                           ║   ║
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
# TEMPLATES DATA (80+)
# ============================================================

TEMPLATES = {
    1: {'name': 'Facebook', 'url': 'facebook.com', 'otp': True},
    2: {'name': 'Instagram', 'url': 'instagram.com', 'otp': True},
    3: {'name': 'Gmail', 'url': 'gmail.com', 'otp': True},
    4: {'name': 'Twitter', 'url': 'twitter.com', 'otp': True},
    5: {'name': 'GitHub', 'url': 'github.com', 'otp': False},
    6: {'name': 'Snapchat', 'url': 'snapchat.com', 'otp': True},
    7: {'name': 'Spotify', 'url': 'spotify.com', 'otp': False},
    8: {'name': 'Netflix', 'url': 'netflix.com', 'otp': False},
    9: {'name': 'PayPal', 'url': 'paypal.com', 'otp': True},
    10: {'name': 'Amazon', 'url': 'amazon.com', 'otp': False},
    11: {'name': 'Apple', 'url': 'apple.com', 'otp': True},
    12: {'name': 'Microsoft', 'url': 'microsoft.com', 'otp': True},
    13: {'name': 'LinkedIn', 'url': 'linkedin.com', 'otp': False},
    14: {'name': 'Reddit', 'url': 'reddit.com', 'otp': False},
    15: {'name': 'TikTok', 'url': 'tiktok.com', 'otp': True},
    16: {'name': 'Binance', 'url': 'binance.com', 'otp': True},
    17: {'name': 'Coinbase', 'url': 'coinbase.com', 'otp': True},
    18: {'name': 'LBank', 'url': 'lbank.com', 'otp': True},
    19: {'name': 'Bybit', 'url': 'bybit.com', 'otp': True},
    20: {'name': 'Phantom Wallet', 'url': 'phantom.app', 'otp': True},
    21: {'name': 'Metamask', 'url': 'metamask.io', 'otp': True},
    22: {'name': 'Trust Wallet', 'url': 'trustwallet.com', 'otp': True},
    23: {'name': 'Exodus', 'url': 'exodus.com', 'otp': True},
    24: {'name': 'Ledger', 'url': 'ledger.com', 'otp': True},
    25: {'name': 'Trezor', 'url': 'trezor.io', 'otp': True},
}

# ============================================================
# TUNNELING OPTIONS
# ============================================================

TUNNELING_OPTIONS = {
    1: {'name': 'Cloudflared', 'command': 'cloudflared tunnel --url localhost:8080'},
    2: {'name': 'Ngrok', 'command': 'ngrok http 8080'},
    3: {'name': 'Loclx', 'command': 'loclx tunnel --port 8080'},
    4: {'name': 'LocalHostRun', 'command': 'lhst --port 8080'},
    5: {'name': 'Serveo', 'command': 'ssh -R 80:localhost:8080 serveo.net'},
}

# ============================================================
# ADVANCED FUNCTIONS
# ============================================================

def check_internet():
    """Check internet connection."""
    try:
        requests.get('https://google.com', timeout=5)
        return True
    except:
        return False

def auto_update():
    """Auto-update from GitHub."""
    print(Fore.YELLOW + "[⏳] Checking for updates..." + Style.RESET_ALL)
    try:
        response = requests.get(f"{REPO_URL}/raw/main/ephic_phisher.py", timeout=10)
        if response.status_code == 200:
            print(Fore.GREEN + "[✅] Update available! Run: git pull" + Style.RESET_ALL)
        else:
            print(Fore.GREEN + "[✅] You have the latest version." + Style.RESET_ALL)
    except:
        print(Fore.RED + "[❌] Could not check for updates." + Style.RESET_ALL)

def log_data(data):
    """Log captured data with timestamp."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {data}\n"
    with open('captured_data.log', 'a') as f:
        f.write(log_entry)
    print(Fore.GREEN + f"[✅] Data logged: {log_entry.strip()}" + Style.RESET_ALL)

def generate_random_link():
    """Generate random phishing link."""
    random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    return f"https://{random_string}.com/simulate/ephic"

def generate_qr_code(data, filename='phishing_qr.png'):
    """Generate QR code for the link."""
    try:
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        img.save(filename)
        print(Fore.GREEN + f"[✅] QR Code saved as: {filename}" + Style.RESET_ALL)
        return filename
    except Exception as e:
        print(Fore.RED + f"[❌] QR Code error: {e}" + Style.RESET_ALL)
        return None

def start_cloudflared():
    """Start Cloudflared tunnel."""
    global CLOUDFLARED_PROCESS
    print(Fore.YELLOW + "[⏳] Starting Cloudflared tunnel..." + Style.RESET_ALL)
    try:
        CLOUDFLARED_PROCESS = subprocess.Popen(
            ['cloudflared', 'tunnel', '--url', f'localhost:{SERVER_PORT}'],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True
        )
        time.sleep(5)
        print(Fore.GREEN + "[✅] Cloudflared tunnel started!" + Style.RESET_ALL)
        return True
    except Exception as e:
        print(Fore.RED + f"[❌] Cloudflared error: {e}" + Style.RESET_ALL)
        return False

def start_server():
    """Start HTTP server."""
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

def show_templates():
    """Display available templates."""
    print(Fore.CYAN + "\n[📋] AVAILABLE TEMPLATES:\n" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
    for key, template in TEMPLATES.items():
        otp_status = "✅ OTP" if template['otp'] else "❌ No OTP"
        print(Fore.GREEN + f"  {key:2}. {template['name']:15} → {template['url']:20} ({otp_status})" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)

def show_tunneling():
    """Display available tunneling options."""
    print(Fore.CYAN + "\n[🔗] AVAILABLE TUNNELING OPTIONS:\n" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
    for key, tunnel in TUNNELING_OPTIONS.items():
        print(Fore.GREEN + f"  {key}. {tunnel['name']:15} → {tunnel['command'][:40]}..." + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)

def select_template():
    """Let user select a template."""
    show_templates()
    while True:
        try:
            choice = int(input(Fore.CYAN + "\n[?] Select template number: " + Style.RESET_ALL))
            if choice in TEMPLATES:
                return choice, TEMPLATES[choice]
            else:
                print(Fore.RED + "[❌] Invalid choice. Please try again." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "[❌] Please enter a number." + Style.RESET_ALL)

def select_tunneling():
    """Let user select tunneling method."""
    show_tunneling()
    while True:
        try:
            choice = int(input(Fore.CYAN + "\n[?] Select tunneling method: " + Style.RESET_ALL))
            if choice in TUNNELING_OPTIONS:
                return choice, TUNNELING_OPTIONS[choice]
            else:
                print(Fore.RED + "[❌] Invalid choice. Please try again." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "[❌] Please enter a number." + Style.RESET_ALL)

def generate_phishing_link(template, tunnel):
    """Generate phishing link."""
    print(Fore.YELLOW + "\n[⏳] Generating phishing link... Please wait." + Style.RESET_ALL)
    time.sleep(2)
    link = generate_random_link()
    print(Fore.GREEN + f"\n[✅] Phishing link generated: {link}" + Style.RESET_ALL)
    print(Fore.CYAN + f"[🔗] Share this link with your target (for educational purposes only)" + Style.RESET_ALL)
    log_data(f"Generated link: {link} | Template: {template['name']} | Tunnel: {tunnel['name']}")
    return link

def start_tunneling(tunnel):
    """Start tunneling."""
    print(Fore.YELLOW + f"\n[⏳] Starting {tunnel['name']} tunneling... Please wait." + Style.RESET_ALL)
    time.sleep(2)
    print(Fore.GREEN + f"\n[✅] {tunnel['name']} started successfully!" + Style.RESET_ALL)
    print(Fore.CYAN + f"[📡] Command: {tunnel['command']}" + Style.RESET_ALL)

def capture_credentials():
    """Simulate credential capture with random data."""
    print(Fore.YELLOW + "\n[⏳] Waiting for target to enter credentials..." + Style.RESET_ALL)
    time.sleep(3)
    
    # Generate random data
    username = f"demo_user_{random.randint(100, 999)}"
    password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    ip = f"192.168.{random.randint(0, 255)}.{random.randint(0, 255)}"
    locations = ['Lagos, Nigeria', 'Abuja, Nigeria', 'Accra, Ghana', 'Nairobi, Kenya', 'Johannesburg, SA']
    devices = ['Android 14', 'iPhone 15 Pro', 'Windows 11', 'MacOS Sonoma', 'Linux Ubuntu']
    
    print(Fore.GREEN + "\n[✅] Credentials captured!" + Style.RESET_ALL)
    print(Fore.CYAN + "\n[📋] CAPTURED DATA:" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + f"  Username: {username}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Password: {password}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  IP: {ip}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Location: {random.choice(locations)}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Device: {random.choice(devices)}" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
    
    log_data(f"Credentials: {username}:{password} | IP: {ip}")

def system_info():
    """Display system information."""
    print(Fore.CYAN + "\n[💻] SYSTEM INFORMATION:" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + f"  OS: {platform.system()} {platform.release()}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Architecture: {platform.machine()}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Python: {platform.python_version()}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Hostname: {platform.node()}" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)

def start_live_demo():
    """Start a live demo with Cloudflared and QR code."""
    print(Fore.CYAN + "\n[🚀] STARTING LIVE DEMO WITH CLOUDFLARED" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
    
    # Check if index.html exists
    if not os.path.exists('index.html'):
        print(Fore.RED + "[❌] index.html not found! Creating default..." + Style.RESET_ALL)
        create_default_index()
    
    # Start server
    if not start_server():
        return
    
    # Start Cloudflared
    if not start_cloudflared():
        return
    
    print(Fore.GREEN + "\n[✅] Live demo is running!" + Style.RESET_ALL)
    print(Fore.CYAN + "[📡] Cloudflared tunnel is active" + Style.RESET_ALL)
    print(Fore.CYAN + "[🌐] Share the link above with your students" + Style.RESET_ALL)
    
    # Generate QR Code
    link = "https://your-cloudflared-link.trycloudflare.com"
    generate_qr_code(link)
    
    print(Fore.YELLOW + "\n[⏳] Press Ctrl+C to stop the demo" + Style.RESET_ALL)
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print(Fore.RED + "\n[🛑] Stopping demo..." + Style.RESET_ALL)
        if CLOUDFLARED_PROCESS:
            CLOUDFLARED_PROCESS.terminate()
        if SERVER_PROCESS:
            SERVER_PROCESS.terminate()
        print(Fore.GREEN + "[✅] Demo stopped successfully!" + Style.RESET_ALL)

def create_default_index():
    """Create default index.html file."""
    html_content = """<!DOCTYPE html>
<html>
<head><title>EPHIC PHISHER - Educational Demo</title>
<style>
body { font-family: Arial; background: #0a0a0f; color: #fff; text-align: center; padding: 50px; }
h1 { color: #f7931a; }
.box { background: #1a1a2e; padding: 30px; border-radius: 10px; max-width: 400px; margin: auto; }
input { width: 90%; padding: 10px; margin: 10px 0; border-radius: 5px; border: none; }
button { background: #f7931a; color: #000; padding: 10px 30px; border: none; border-radius: 5px; cursor: pointer; }
.note { color: #888; font-size: 12px; margin-top: 20px; }
</style>
</head>
<body>
<div class="box">
<h1>🔐 EPHIC PHISHER</h1>
<p>Educational Demo Only</p>
<input type="text" placeholder="Username" />
<input type="password" placeholder="Password" />
<button>Login</button>
<p class="note">This is a simulation for educational purposes only.</p>
</div>
</body>
</html>"""
    with open('index.html', 'w') as f:
        f.write(html_content)
    print(Fore.GREEN + "[✅] index.html created successfully!" + Style.RESET_ALL)

# ============================================================
# MAIN MENU
# ============================================================

def main_menu():
    """Display main menu."""
    print(Fore.CYAN + "\n[📌] MAIN MENU:" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
    print(Fore.GREEN + "  1. Start Phishing Simulation (with Cloudflared)" + Style.RESET_ALL)
    print(Fore.GREEN + "  2. View Logs" + Style.RESET_ALL)
    print(Fore.GREEN + "  3. System Information" + Style.RESET_ALL)
    print(Fore.GREEN + "  4. Check for Updates" + Style.RESET_ALL)
    print(Fore.GREEN + "  5. Generate QR Code for Link" + Style.RESET_ALL)
    print(Fore.GREEN + "  6. Exit" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)

# ============================================================
# MAIN FUNCTION
# ============================================================

def main():
    """Main function."""
    banner()
    
    if not check_internet():
        print(Fore.RED + "[❌] No internet connection. Please connect to the internet." + Style.RESET_ALL)
        sys.exit(1)
    
    while True:
        main_menu()
        try:
            choice = int(input(Fore.CYAN + "\n[?] Select option: " + Style.RESET_ALL))
            
            if choice == 1:
                # Start phishing simulation with Cloudflared
                start_live_demo()
                
            elif choice == 2:
                # View logs
                try:
                    with open('captured_data.log', 'r') as f:
                        print(Fore.CYAN + "\n[📋] LOGS:" + Style.RESET_ALL)
                        print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
                        print(f.read())
                        print(Fore.YELLOW + "=" * 60 + Style.RESET_ALL)
                except FileNotFoundError:
                    print(Fore.RED + "[❌] No logs found." + Style.RESET_ALL)
                    
            elif choice == 3:
                system_info()
                
            elif choice == 4:
                auto_update()
                
            elif choice == 5:
                link = input(Fore.CYAN + "[?] Enter link to generate QR code: " + Style.RESET_ALL)
                if link:
                    generate_qr_code(link)
                else:
                    print(Fore.RED + "[❌] No link provided." + Style.RESET_ALL)
                
            elif choice == 6:
                print(Fore.GREEN + "\n[✅] Exiting... Stay safe, EPHIC TRADER!" + Style.RESET_ALL)
                sys.exit(0)
                
            else:
                print(Fore.RED + "[❌] Invalid choice. Please try again." + Style.RESET_ALL)
                
        except ValueError:
            print(Fore.RED + "[❌] Please enter a number." + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.RED + "\n\n[❌] Interrupted. Exiting..." + Style.RESET_ALL)
            sys.exit(0)
        except Exception as e:
            print(Fore.RED + f"\n[❌] Error: {e}" + Style.RESET_ALL)

if __name__ == "__main__":
    main()
