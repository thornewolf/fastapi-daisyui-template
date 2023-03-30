from .common import ScrapedLink, scrape
from bs4 import BeautifulSoup
from cachetools import TTLCache, cached
from urllib.parse import urlparse, parse_qs


def bad_title_filter(title: str) -> bool:
    stubs = [
        "Skip To First Content",
        "CBC Lite",
        "Sections",
        "News",
        "Editors'",
        "Latest",
        "Trending",
        "Topics",
        "Privacy",
        "Accessibility",
        "Submit Feedback",
        "Lite Help Centre",
        "Jobs",
        "RSS",
        "release notes",
        "visit the full site.",
        "enhance our services",
        "advertising purposes",
        "review your settings",
        "Learn more about CBC and your data",
        "Terms of Use",
        "Reuse & Permission",
    ]
    return any([stub in title for stub in stubs])


@cached(cache=TTLCache(maxsize=1, ttl=60))
def scrape_cbc() -> list[ScrapedLink]:
    url = "https://www.cbc.ca/lite/news?sort=latest"
    results = scrape(url)
    results = [result for result in results if result.title != ""]
    for r in results:
        r.title = r.title.strip()
        r.href = f"https://www.cbc.ca{r.href}"
    results = [result for result in results if not bad_title_filter(result.title)]
    print(results)
    return results
