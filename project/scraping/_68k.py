from .common import ScrapedLink, scrape_w_param


def scrape_68k() -> list[ScrapedLink]:
    url = "http://68k.news/"
    return scrape_w_param(url, "a")
