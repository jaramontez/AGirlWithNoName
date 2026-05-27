"""
Scrape Idealist.org for nonprofits and volunteer/job listings in art education.
Idealist renders via client-side JS, so we use their public search API endpoints
that back the site's search page.
"""
import requests
import time

BASE_API = "https://www.idealist.org/api/v1"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Referer": "https://www.idealist.org/",
}
SEARCH_TERMS = ["art education children", "arts education youth", "visual arts kids nonprofit"]


def get_orgs(limit: int = 6) -> list[dict]:
    orgs = []
    seen = set()

    for term in SEARCH_TERMS:
        if len(orgs) >= limit:
            break
        try:
            time.sleep(1.5)
            params = {
                "q": term,
                "type": "ORGANIZATION",
                "page": 1,
                "perPage": 10,
            }
            resp = requests.get(f"{BASE_API}/search", headers=HEADERS, params=params, timeout=15)
            if resp.status_code != 200:
                continue
            data = resp.json()
            items = data.get("results", data.get("hits", []))
            for item in items:
                name = item.get("name") or item.get("title", "")
                url = item.get("url") or item.get("actionUrl") or f"https://www.idealist.org/en/nonprofit/{item.get('slug', '')}"
                mission = item.get("mission") or item.get("description", "")[:200]
                location = item.get("location") or item.get("city", "")

                if name and name not in seen:
                    seen.add(name)
                    orgs.append({
                        "name": name,
                        "url": url,
                        "mission": mission,
                        "location": location,
                        "source": "Idealist.org",
                    })
                if len(orgs) >= limit:
                    break
        except Exception as e:
            print(f"[idealist] error: {e}")

    return orgs


def get_listings(limit: int = 5) -> list[dict]:
    """Volunteer ops and jobs in art education."""
    listings = []
    seen = set()

    for term in ["art education", "arts youth nonprofit"]:
        if len(listings) >= limit:
            break
        try:
            time.sleep(1.5)
            for list_type in ["VOLUNTEER", "JOB"]:
                params = {
                    "q": term,
                    "type": list_type,
                    "page": 1,
                    "perPage": 5,
                }
                resp = requests.get(f"{BASE_API}/search", headers=HEADERS, params=params, timeout=15)
                if resp.status_code != 200:
                    continue
                data = resp.json()
                items = data.get("results", data.get("hits", []))
                for item in items:
                    title = item.get("name") or item.get("title", "")
                    org = item.get("parentOrganization", {}).get("name", "") if isinstance(item.get("parentOrganization"), dict) else item.get("organization", "")
                    url = item.get("url") or item.get("actionUrl", "")
                    location = item.get("location") or item.get("city", "")

                    key = f"{title}-{org}"
                    if title and key not in seen:
                        seen.add(key)
                        listings.append({
                            "title": title,
                            "organization": org,
                            "url": url,
                            "location": location,
                            "type": list_type,
                            "source": "Idealist.org",
                        })
                    if len(listings) >= limit:
                        break
        except Exception as e:
            print(f"[idealist listings] error: {e}")

    return listings
