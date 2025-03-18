import requests
import random
import time
from colorama import Fore, Style, init

init(autoreset=True)

# Daftar user-agent acak
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/100.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 Safari/537.36"
]

# Error MySQL klasik
mysql_errors = [
    "You have an error in your SQL syntax;",
    "Warning: mysql_",
    "Warning: mysqli_",
    "MySQL server version for the right syntax to use",
    "supplied argument is not a valid MySQL"
]

def check_url(url):
    try:
        test_url = url + "'"
        headers = {
            "User-Agent": random.choice(user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Connection": "close"
        }
        response = requests.get(test_url, headers=headers, timeout=5)

        for err in mysql_errors:
            if err.lower() in response.text.lower():
                return True, err
        return False, ""
    except requests.exceptions.RequestException as e:
        return False, f"[ERROR] {e}"

def main():
    print(Fore.CYAN + "==== MySQL Dork Vulnerability Scanner ====")
    print("Contoh input: http://site.com/page.php?id=1,http://test.com/view.php?id=3")
    input_urls = input(Fore.CYAN + "\nMasukkan URL target (pisahkan dengan koma):\n> ")

    urls = [u.strip() for u in input_urls.split(",") if u.strip()]
    if not urls:
        print(Fore.RED + "[!] Tidak ada URL yang dimasukkan!")
        return

    print(f"\n[*] Memulai scan pada {len(urls)} URL...\n")

    for i, url in enumerate(urls, 1):
        print(f"[{i}] Menguji: {Fore.WHITE + url}")
        vulnerable, message = check_url(url)
        if vulnerable:
            print(Fore.RED + f"    [VULNERABLE] Terindikasi error: {message}\n")
        elif message.startswith("[ERROR]"):
            print(Fore.YELLOW + f"    [GAGAL] {message}\n")
        else:
            print(Fore.GREEN + "    [AMAN] Tidak ditemukan error MySQL\n")
        time.sleep(1)

    print(Fore.CYAN + "[✓] Scan selesai.")

if __name__ == "__main__":
    main()
