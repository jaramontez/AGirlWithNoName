"""
Scrape art supply companies, corporate giving programs, and small foundations
that have actual donation/grant programs relevant to art education nonprofits.
Focuses on sources accessible to first-year orgs with no geographic restrictions.
"""
from .base_scraper import fetch

SOURCES = [
    {
        "name": "Dick Blick Art Materials Donations",
        "url": "https://www.dickblick.com/about-blick/donation-form/",
        "type": "in-kind/product donation",
    },
    {
        "name": "Michaels Stores Foundation",
        "url": "https://www.michaelsfoundation.org/grant-guidelines/",
        "type": "grant",
    },
    {
        "name": "NAMTA Foundation Grants",
        "url": "https://www.namta.org/page/FoundationGrants",
        "type": "grant",
    },
    {
        "name": "The Pollination Project",
        "url": "https://thepollinationproject.org/apply-for-funding/",
        "type": "micro-grant",
    },
    {
        "name": "Awesome Foundation",
        "url": "https://www.awesomefoundation.org/en/apply",
        "type": "micro-grant",
    },
    {
        "name": "Americans for the Arts Grants",
        "url": "https://www.americansforthearts.org/by-topic/funding",
        "type": "grant resource",
    },
    {
        "name": "Faber-Castell USA Education",
        "url": "https://www.fabercastell.com/pages/art-education",
        "type": "partnership/in-kind",
    },
    {
        "name": "Dollar General Literacy Foundation",
        "url": "https://www.dgliteracy.org/grant-programs/",
        "type": "grant",
    },
    {
        "name": "Target Arts & Culture Grants",
        "url": "https://corporate.target.com/sustainability-governance/our-communities/target-foundation",
        "type": "grant",
    },
    {
        "name": "Walmart Community Grants",
        "url": "https://walmart.org/how-we-give/community-grants",
        "type": "grant",
    },
]


def get_grant_programs(limit: int = 8) -> list[dict]:
    """
    Scrape each source page and extract key eligibility/deadline info.
    Falls back to returning the source metadata if scraping fails.
    """
    results = []

    for source in SOURCES[:limit]:
        soup = fetch(source["url"])
        details = ""

        if soup:
            # Pull the first substantive paragraph or list from the page
            for tag in soup.select("p, li"):
                text = tag.get_text(strip=True)
                if len(text) > 80 and any(kw in text.lower() for kw in [
                    "grant", "donat", "apply", "eligib", "fund", "award",
                    "nonprofit", "501", "art", "educat", "deadline", "amount"
                ]):
                    details = text[:400]
                    break

        results.append({
            "name": source["name"],
            "url": source["url"],
            "type": source["type"],
            "details": details,
            "source": "Art Grants Scraper",
        })

    return results
