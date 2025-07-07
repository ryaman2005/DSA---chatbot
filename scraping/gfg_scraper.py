import requests
from bs4 import BeautifulSoup
import urllib.parse

HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_gfg_article(query):
    try:
        search_url = f"https://duckduckgo.com/html/?q={urllib.parse.quote(query)}+site:geeksforgeeks.org"
        res = requests.get(search_url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")

        links = soup.find_all("a", class_="result__a", href=True)
        if not links:
            return "\u26a0\ufe0f No results found."

        article_url = links[0]["href"]
        if article_url.startswith("/l/?uddg="):
            article_url = urllib.parse.unquote(article_url.split("/l/?uddg=")[1])

        article_res = requests.get(article_url, headers=HEADERS)
        article_soup = BeautifulSoup(article_res.text, "html.parser")
        content_div = article_soup.find("div", class_="text")

        if not content_div:
            return "\u26a0\ufe0f Couldn't extract article content."

        paragraphs = content_div.find_all("p")
        full_text = "\n\n".join(p.get_text() for p in paragraphs)
        return full_text.strip()[:3000]

    except Exception as e:
        return f"\u26a0\ufe0f Error fetching article: {e}"
