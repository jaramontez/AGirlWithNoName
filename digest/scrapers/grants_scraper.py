"""
Scrape publicly available grant listings relevant to arts education nonprofits.
Sources: Grants.gov RSS (public), Foundation Center open data.
"""
import requests
import xml.etree.ElementTree as ET
import time

GRANTS_GOV_RSS = (
    "https://www.grants.gov/rss/GG_NewOppByAgency.aspx?&fundingCategories=AR"
)


def get_grants(limit: int = 5) -> list[dict]:
    """Pull arts grants from Grants.gov public RSS feed."""
    grants = []
    try:
        time.sleep(1)
        resp = requests.get(GRANTS_GOV_RSS, timeout=15)
        resp.raise_for_status()
        root = ET.fromstring(resp.content)
        ns = {"atom": "http://www.w3.org/2005/Atom"}

        # Try RSS format first
        channel = root.find("channel")
        if channel is not None:
            for item in channel.findall("item")[:limit]:
                title = item.findtext("title", "")
                url = item.findtext("link", "")
                desc = item.findtext("description", "")[:200]
                if title:
                    grants.append({"title": title, "url": url, "description": desc, "source": "Grants.gov"})
    except Exception as e:
        print(f"[grants_scraper] error: {e}")

    return grants
