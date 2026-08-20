#!/usr/bin/env python3
# ============================================================
# EPHIC PHISHER PRO - VERSION 1.0.0
# ADVANCED PHISHING SIMULATION TOOL FOR EDUCATIONAL PURPOSES
# AUTHOR: EPHIC TRADER | KOC @ LBank Exchange
# ============================================================

import os
import sys
import time
import json
import subprocess
import platform
import requests
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# ============================================================
# BANNER
# ============================================================

def banner():
    os.system('clear')
    print(Fore.YELLOW + """
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║    ███████╗██████╗ ██╗  ██╗██╗ ██████╗                   ║
    ║    ██╔════╝██╔══██╗██║  ██║██║██╔════╝                   ║
    ║    █████╗  ██████╔╝███████║██║██║                         ║
    ║    ██╔══╝  ██╔═══╝ ██╔══██║██║██║                         ║
    ║    ███████╗██║     ██║  ██║██║╚██████╗                   ║
    ║    ╚══════╝╚═╝     ╚═╝  ╚═╝╚═╝ ╚═════╝                   ║
    ║                                                           ║
    ║           ██████╗ ██████╗  ██████╗                        ║
    ║           ██╔══██╗██╔══██╗██╔═══██╗                       ║
    ║           ██████╔╝██████╔╝██║   ██║                       ║
    ║           ██╔═══╝ ██╔══██╗██║   ██║                       ║
    ║           ██║     ██║  ██║╚██████╔╝                       ║
    ║           ╚═╝     ╚═╝  ╚═╝ ╚═════╝                        ║
    ║                                                           ║
    ║    ╔═══════════════════════════════════════════════════╗   ║
    ║    ║  ADVANCED PHISHING SIMULATION TOOL               ║   ║
    ║    ║  FOR EDUCATIONAL & TESTING PURPOSES ONLY         ║   ║
    ║    ║  AUTHOR: EPHIC TRADER                            ║   ║
    ║    ║  VERSION: 1.0.0                                  ║   ║
    ║    ╚═══════════════════════════════════════════════════╝   ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """ + Style.RESET_ALL)

# ============================================================
# TEMPLATES DATA
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
# FUNCTIONS
# ============================================================

def show_templates():
    """Display available templates."""
    print(Fore.CYAN + "\n📋 AVAILABLE TEMPLATES:\n" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
    for key, template in TEMPLATES.items():
        otp_status = "✅ OTP" if template['otp'] else "❌ No OTP"
        print(Fore.GREEN + f"  {key}. {template['name']:12} → {template['url']:15} ({otp_status})" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)

def show_tunneling():
    """Display available tunneling options."""
    print(Fore.CYAN + "\n🔗 AVAILABLE TUNNELING OPTIONS:\n" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)
    for key, tunnel in TUNNELING_OPTIONS.items():
        print(Fore.GREEN + f"  {key}. {tunnel['name']:15} → {tunnel['command'][:30]}..." + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 50 + Style.RESET_ALL)

def select_template():
    """Let user select a template."""
    show_templates()
    while True:
        try:
            choice = int(input(Fore.CYAN + "\n[?] Select template number: " + Style.RESET_ALL))
            if choice in TEMPLATES:
                return choice, TEMPLATES[choice]
            else:
                print(Fore.RED + "❌ Invalid choice. Please try again." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "❌ Please enter a number." + Style.RESET_ALL)

def select_tunneling():
    """Let user select tunneling method."""
    show_tunneling()
    while True:
        try:
            choice = int(input(Fore.CYAN + "\n[?] Select tunneling method: " + Style.RESET_ALL))
            if choice in TUNNELING_OPTIONS:
                return choice, TUNNELING_OPTIONS[choice]
            else:
                print(Fore.RED + "❌ Invalid choice. Please try again." + Style.RESET_ALL)
        except ValueError:
            print(Fore.RED + "❌ Please enter a number." + Style.RESET_ALL)

def generate_phishing_link(template, tunnel):
    """Generate phishing link."""
    print(Fore.YELLOW + "\n[⏳] Generating phishing link... Please wait." + Style.RESET_ALL)
    time.sleep(2)
    link = f"https://{template['url']}.com/simulate/ephic"
    print(Fore.GREEN + f"\n✅ Phishing link generated: {link}" + Style.RESET_ALL)
    print(Fore.CYAN + f"🔗 Share this link with your target (for educational purposes only)" + Style.RESET_ALL)
    return link

def start_tunneling(tunnel):
    """Start tunneling."""
    print(Fore.YELLOW + f"\n[⏳] Starting {tunnel['name']} tunneling... Please wait." + Style.RESET_ALL)
    time.sleep(2)
    print(Fore.GREEN + f"\n✅ {tunnel['name']} started successfully!" + Style.RESET_ALL)
    print(Fore.CYAN + f"📡 Command: {tunnel['command']}" + Style.RESET_ALL)

def capture_credentials():
    """Simulate credential capture."""
    print(Fore.YELLOW + "\n[⏳] Waiting for target to enter credentials..." + Style.RESET_ALL)
    time.sleep(3)
    print(Fore.GREEN + "\n✅ Credentials captured!" + Style.RESET_ALL)
    print(Fore.CYAN + "\n📋 CAPTURED DATA:" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 40 + Style.RESET_ALL)
    print(Fore.GREEN + f"  Username: demo_user_{int(time.time())%1000}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Password: **********" + Style.RESET_ALL)
    print(Fore.GREEN + f"  IP: 192.168.1.{int(time.time())%255}" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Location: Lagos, Nigeria" + Style.RESET_ALL)
    print(Fore.GREEN + f"  Device: Android 14" + Style.RESET_ALL)
    print(Fore.YELLOW + "=" * 40 + Style.RESET_ALL)

def log_data(data):
    """Log captured data."""
    with open('captured_data.log', 'a') as f:
        f.write(f"{time.ctime()} | {data}\n")
    print(Fore.GREEN + f"\n✅ Data logged to captured_data.log" + Style.RESET_ALL)

def main():
    """Main function."""
    banner()
    print(Fore.CYAN + "\n⚠️  WARNING: This tool is for EDUCATIONAL PURPOSES only." + Style.RESET_ALL)
    print(Fore.CYAN + "⚠️  Do NOT use for illegal activities. Unauthorized use is prohibited." + Style.RESET_ALL)
    print(Fore.CYAN + "⚠️  By using this tool, you agree to use it responsibly.\n" + Style.RESET_ALL)

    # Select template
    template_id, template = select_template()

    # Select tunneling
    tunnel_id, tunnel = select_tunneling()

    # Generate link
    link = generate_phishing_link(template, tunnel)

    # Start tunneling
    start_tunneling(tunnel)

    # Simulate credential capture
    capture_credentials()

    # Log data
    log_data(f"Template: {template['name']} | Link: {link}")

    print(Fore.GREEN + "\n✅ Simulation completed!" + Style.RESET_ALL)
    print(Fore.CYAN + "\n📌 REMEMBER: Use this knowledge responsibly." + Style.RESET_ALL)
    print(Fore.CYAN + "📌 Protect yourself and others from real phishing attacks.\n" + Style.RESET_ALL)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(Fore.RED + "\n\n❌ Interrupted. Exiting..." + Style.RESET_ALL)
        sys.exit(0)
    except Exception as e:
        print(Fore.RED + f"\n❌ Error: {e}" + Style.RESET_ALL)
        sys.exit(1)
