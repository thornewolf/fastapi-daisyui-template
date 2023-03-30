import httpx
from dataclasses import dataclass
from pydantic import BaseModel, Field
from bs4 import BeautifulSoup
from cachetools import TTLCache, cached
from urllib.parse import urlparse, parse_qs


def extract_param(url, param):
    try:
        parsed_url = urlparse(url)
        query_params = parse_qs(parsed_url.query)

        u_param = query_params[param][0]

        return u_param
    except:
        return ""


class ScrapedLink(BaseModel):
    title: str = Field(..., example="Article Title")
    href: str = Field(..., example="https://example.com")

    def __hash__(self):
        return hash(self.title + self.href)


@cached(cache=TTLCache(maxsize=1, ttl=60))
def scrape_w_param(url: str, param: str) -> list[ScrapedLink]:
    response = httpx.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all("a")

    results = [
        ScrapedLink(title=link.text, href=extract_param(link["href"], param))
        for link in links
    ]
    results = [result for result in results if result.href != "" and result.title != ""]
    return results


@cached(cache=TTLCache(maxsize=1, ttl=60))
def scrape(url: str) -> list[ScrapedLink]:
    response = httpx.get(url)

    soup = BeautifulSoup(response.content, "html.parser")

    links = soup.find_all("a")

    results = [ScrapedLink(title=link.text, href=link["href"]) for link in links]
    results = [result for result in results if result.href != "" and result.title != ""]
    return results
