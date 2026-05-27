import requests
from bs4 import BeautifulSoup
import time
import random

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


def fetch(url: str, timeout: int = 15) -> BeautifulSoup | None:
    try:
        time.sleep(random.uniform(1.0, 2.5))
        resp = requests.get(url, headers=HEADERS, timeout=timeout)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, "html.parser")
    except Exception as e:
        print(f"[scraper] failed to fetch {url}: {e}")
        return None


def url_is_alive(url: str, timeout: int = 10) -> bool:
    """Return True only if the URL actually responds with a non-error status."""
    try:
        time.sleep(random.uniform(0.5, 1.0))
        resp = requests.head(url, headers=HEADERS, timeout=timeout, allow_redirects=True)
        if resp.status_code == 405:
            # Some servers don't allow HEAD — fall back to GET
            resp = requests.get(url, headers=HEADERS, timeout=timeout, stream=True)
        return resp.status_code < 400
    except Exception:
        return False
