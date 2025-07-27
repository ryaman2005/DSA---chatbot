import requests
from bs4 import BeautifulSoup
import os
import re

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def clean_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    paragraphs = soup.find_all('p')
    return "\n".join(p.get_text().strip() for p in paragraphs if p.get_text().strip())

def scrape_gfg_article(url):
    try:
        res = requests.get(url, headers=HEADERS)
        res.raise_for_status()
        return clean_text(res.text)
    except Exception as e:
        print(f"[ERROR] Could not scrape {url}: {e}")
        return ""

def url_to_filename(url):
    slug = url.rstrip("/").split("/")[-1]
    return re.sub(r'[^a-zA-Z0-9_-]', '', slug)

def save_gfg_article(url, path="data/processed_gfg"):
    os.makedirs(path, exist_ok=True)
    content = scrape_gfg_article(url)
    if not content:
        return
    name = url_to_filename(url)
    with open(os.path.join(path, f"{name}.txt"), "w", encoding="utf-8") as f:
        f.write(content)
    print(f"[✔] Saved {name}.txt")

def batch_scrape(urls, path="data/processed_gfg"):
    for url in urls:
        save_gfg_article(url, path)

# Example use:
if __name__ == "__main__":
    gfg_urls = [
        "https://www.geeksforgeeks.org/binary-search/",
        "https://www.geeksforgeeks.org/queue-data-structure/",
        "https://www.geeksforgeeks.org/dynamic-programming/"
    ]
    batch_scrape(gfg_urls)
