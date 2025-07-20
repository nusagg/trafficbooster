import requests, re

def scrape_proxies():
    urls = [
        "https://api.proxyscrape.com/?request=getproxies&proxytype=http",
        "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt"
    ]
    proxies = set()
    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            found = re.findall(r'\d+\.\d+\.\d+\.\d+:\d+', r.text)
            proxies.update(found)
        except:
            pass
    with open("proxies.txt", "w") as f:
        for proxy in proxies:
            f.write(proxy + "\n")
    return list(proxies)
