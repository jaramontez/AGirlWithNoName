"""Scrape Blue Avocado — practical nonprofit management articles."""
from .base_scraper import fetch

BLUE_AVOCADO_URL = "https://blueavocado.org"


def get_articles(limit: int = 5) -> list[dict]:
    soup = fetch(BLUE_AVOCADO_URL)
    if not soup:
        return []

    articles = []
    for card in soup.select("article, .post, [class*='entry']")[:limit * 3]:
        title_el = card.select_one("h2, h3, .entry-title")
        link_el = card.select_one("a[href]")
        desc_el = card.select_one("p, .entry-summary")

        title = title_el.get_text(strip=True) if title_el else ""
        url = link_el["href"] if link_el else ""
        desc = desc_el.get_text(strip=True)[:200] if desc_el else ""

        if not url.startswith("http"):
            url = BLUE_AVOCADO_URL + url

        if title and url and len(title) > 10:
            articles.append({"title": title, "url": url, "description": desc, "source": "Blue Avocado"})
        if len(articles) >= limit:
            break

    return articles
