"""Scrape Instrumentl blog for grant-writing and nonprofit resources."""
from .base_scraper import fetch

INSTRUMENTL_BLOG_URL = "https://www.instrumentl.com/blog"


def get_articles(limit: int = 5) -> list[dict]:
    soup = fetch(INSTRUMENTL_BLOG_URL)
    if not soup:
        return []

    articles = []
    for card in soup.select("article, .blog-card, [class*='post'], [class*='blog']")[:limit * 3]:
        title_el = card.select_one("h2, h3, h4")
        link_el = card.select_one("a[href]")
        desc_el = card.select_one("p")

        title = title_el.get_text(strip=True) if title_el else ""
        url = link_el["href"] if link_el else ""
        desc = desc_el.get_text(strip=True) if desc_el else ""

        if not url.startswith("http"):
            url = "https://www.instrumentl.com" + url

        if title and url and len(title) > 10:
            articles.append({"title": title, "url": url, "description": desc, "source": "Instrumentl"})
        if len(articles) >= limit:
            break

    return articles
