"""
Scrape art supply companies, corporate giving programs, and small foundations
that have donation/grant programs for art education nonprofits.
Every URL is verified live before being passed to Claude — no dead links.
"""
from .base_scraper import fetch, url_is_alive

SOURCES = [
    {
        "name": "Dick Blick Art Materials — Donation Form",
        "url": "https://www.dickblick.com/about-blick/donation-form/",
        "type": "in-kind / product donation",
        "notes": "Accepts requests from nonprofits. Submit the form on their site.",
    },
    {
        "name": "Michaels Stores Foundation",
        "url": "https://www.michaelsfoundation.org/",
        "type": "cash grant",
        "notes": "Funds arts and crafts programs for youth.",
    },
    {
        "name": "NAMTA Foundation",
        "url": "https://www.namta.org/",
        "type": "grant",
        "notes": "National Art Materials Trade Association — grants for art education.",
    },
    {
        "name": "The Pollination Project",
        "url": "https://thepollinationproject.org/apply-for-funding/",
        "type": "micro-grant ($1,000)",
        "notes": "Rolling weekly grants for grassroots projects. Very accessible for year-1 nonprofits.",
    },
    {
        "name": "Awesome Foundation",
        "url": "https://www.awesomefoundation.org/en/apply",
        "type": "micro-grant ($1,000)",
        "notes": "Monthly $1,000 grants. No restrictions on org age.",
    },
    {
        "name": "Walmart Local Community Grants",
        "url": "https://walmart.org/how-we-give/local-community-grants",
        "type": "cash grant ($250–$5,000)",
        "notes": "Rolling applications. Tied to local Walmart/Sam's Club stores.",
    },
    {
        "name": "Americans for the Arts — Funding Resources",
        "url": "https://www.americansforthearts.org/by-topic/funding",
        "type": "grant resource directory",
        "notes": "Curated list of arts funding sources.",
    },
    {
        "name": "Dollar General Literacy Foundation",
        "url": "https://www.dgliteracy.org/grant-programs/",
        "type": "cash grant",
        "notes": "Funds youth literacy and education programs.",
    },
    {
        "name": "Sargent Art — Educator Programs",
        "url": "https://www.sargentart.com/",
        "type": "in-kind / product donation",
        "notes": "Art supply company with educator and nonprofit outreach.",
    },
    {
        "name": "Target Community Giving",
        "url": "https://corporate.target.com/sustainability-governance/our-communities/target-foundation",
        "type": "grant",
        "notes": "Education and community focus. Check for local store giving too.",
    },
]


def get_grant_programs(limit: int = 10) -> list[dict]:
    """
    Check each source URL is actually live, then scrape what details we can.
    Only returns entries with confirmed working URLs.
    """
    results = []

    for source in SOURCES:
        url = source["url"]
        alive = url_is_alive(url)

        if not alive:
            print(f"[art_grants] dead link skipped: {url}")
            continue

        details = source["notes"]

        # Try to grab any extra detail from the live page
        soup = fetch(url)
        if soup:
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
            "url": url,
            "type": source["type"],
            "details": details,
            "url_verified": True,
            "source": "Art Grants Scraper",
        })

        if len(results) >= limit:
            break

    print(f"[art_grants] {len(results)} verified sources returned")
    return results
