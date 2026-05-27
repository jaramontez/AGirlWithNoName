"""Scrape Candid.org blog / learning hub for nonprofit how-to articles."""
from .base_scraper import fetch

CANDID_BLOG_URL = "https://candid.org/learn"


def get_articles(limit: int = 5) -> list[dict]:
    soup = fetch(CANDID_BLOG_URL)
    if not soup:
        return []

    articles = []
    # Candid's learn hub uses article cards
    for card in soup.select("article, .card, [class*='article'], [class*='post']")[:limit * 2]:
        title_el = card.select_one("h2, h3, h4, a")
        link_el = card.select_one("a[href]")
        desc_el = card.select_one("p")

        title = title_el.get_text(strip=True) if title_el else ""
        url = link_el["href"] if link_el else ""
        desc = desc_el.get_text(strip=True) if desc_el else ""

        if not url.startswith("http"):
            url = "https://candid.org" + url

        if title and url:
            articles.append({"title": title, "url": url, "description": desc, "source": "Candid.org"})
        if len(articles) >= limit:
            break

    return articles
