import requests, random, time, threading
from concurrent.futures import ThreadPoolExecutor
from proxy_scraper import scrape_proxies
import logging

LOG_FILE = "track.log"
user_agents = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Mozilla/5.0 (Linux; Android 10; SM-G970F)",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X)",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
]

logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format='%(asctime)s | %(message)s')

def visit(target, proxy, delay):
    while True:
        try:
            ua = random.choice(user_agents)
            headers = {"User-Agent": ua}
            proxies = {"http": f"http://{proxy}", "https": f"http://{proxy}"}
            r = requests.get(target, headers=headers, proxies=proxies, timeout=10)
            status = r.status_code
            log = f"{proxy} | {status} | {ua}"
            logging.info(log)
            print(f"[✓] {log}")
        except Exception as e:
            print(f"[✗] {proxy} - Error: {e}")
        time.sleep(delay)

def run_boost(target, proxies, threads, delay):
    with ThreadPoolExecutor(max_workers=threads) as executor:
        for _ in range(threads):
            p = random.choice(proxies)
            executor.submit(visit, target, p, delay)

def main_loop():
    try:
        with open("target.txt") as f:
            lines = f.read().splitlines()
        target = lines[0]
        threads = int(lines[1])
        delay = float(lines[2])
        interval = 6  # hours
    except:
        print("Gagal membaca target.txt")
        return

    while True:
        print("[*] Scraping proxy...")
        proxies = scrape_proxies()
        print(f"[*] Total proxy: {len(proxies)}")
        run_thread = threading.Thread(target=run_boost, args=(target, proxies, threads, delay))
        run_thread.start()
        time.sleep(interval * 3600)

if __name__ == "__main__":
    main_loop()
