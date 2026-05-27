"""
Entry point for the Doodle Street daily digest.
Run locally:  python -m digest.main
Run with date: python -m digest.main --date 2026-06-01
Run dry-run:  python -m digest.main --dry-run
"""
import argparse
import datetime
import json
import sys

from .scrapers import (
    blue_avocado_scraper,
    candid_scraper,
    grants_scraper,
    idealist_scraper,
    instrumentl_scraper,
    nonprofit_af_scraper,
)
from .digest_builder import build_digest
from .emailer import send_digest


def gather_data() -> dict:
    print("[main] scraping resource sites...")
    articles = []
    articles += candid_scraper.get_articles()
    articles += instrumentl_scraper.get_articles()
    articles += blue_avocado_scraper.get_articles()
    articles += nonprofit_af_scraper.get_articles()

    print("[main] scraping Idealist...")
    orgs = idealist_scraper.get_orgs()
    listings = idealist_scraper.get_listings()

    print("[main] fetching grants...")
    grants = grants_scraper.get_grants()

    return {
        "articles": articles,
        "orgs": orgs,
        "listings": listings,
        "grants": grants,
    }


def main():
    parser = argparse.ArgumentParser(description="Doodle Street daily digest")
    parser.add_argument("--date", help="Override date (YYYY-MM-DD)")
    parser.add_argument("--dry-run", action="store_true", help="Print digest, don't send email")
    parser.add_argument("--skip-scrape", action="store_true", help="Skip scraping (use empty data)")
    args = parser.parse_args()

    date = datetime.date.fromisoformat(args.date) if args.date else datetime.date.today()

    if args.skip_scrape:
        scraped = {"articles": [], "orgs": [], "listings": [], "grants": []}
    else:
        scraped = gather_data()

    print(f"[main] building digest for {date} ...")
    digest = build_digest(scraped, date=date)

    print(f"\n{'=' * 60}")
    print(f"Subject: {digest['subject']}")
    print(f"Type:    {digest['digest_type']}")
    print(f"Label:   {digest['type_label']}")
    print(f"{'=' * 60}")
    print(digest.get("body_markdown", ""))
    print(f"{'=' * 60}\n")

    if args.dry_run:
        print("[main] dry-run mode — email NOT sent.")
        return

    print("[main] sending email...")
    send_digest(digest)
    print("[main] done.")


if __name__ == "__main__":
    main()
