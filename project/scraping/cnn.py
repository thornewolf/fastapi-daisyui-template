from .common import ScrapedLink, scrape
from bs4 import BeautifulSoup
from cachetools import TTLCache, cached
from urllib.parse import urlparse, parse_qs


def bad_title_filter(title: str) -> bool:
    stubs = ["Go to", "Terms of Use", "Privacy Policy", "Ad Choices", "Cookie Settings"]
    return any([stub in title for stub in stubs])


def scrape_cnn() -> list[ScrapedLink]:
    url = "https://lite.cnn.com/"
    results = scrape(url)
    results = [result for result in results if result.title != "CNN"]
    for r in results:
        r.title = r.title.strip()
        r.href = f"https://lite.cnn.com{r.href}"
    results = [result for result in results if not bad_title_filter(result.title)]
    return results
