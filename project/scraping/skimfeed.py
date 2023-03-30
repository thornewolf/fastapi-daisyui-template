from .common import ScrapedLink, scrape_w_param


def scrape_skimfeed() -> list[ScrapedLink]:
    url = "https://skimfeed.com/"
    return scrape_w_param(url, "u")
