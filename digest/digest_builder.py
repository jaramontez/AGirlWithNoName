"""
Use Claude to turn raw scraped data into one polished digest section per day.
Rotates through 4 types on a 4-day cycle keyed to the day of year.
"""
import datetime
import json
import anthropic

DOODLE_STREET_CONTEXT = """
Doodle Street is a nonprofit in its first year of operation, founded by Jara Montez.
Mission: Send art supplies to classrooms where budgets don't cover the basics.
Website: https://doodlestreet.org/
Focus area: Art education for kids, especially in under-resourced schools.
Stage: ~6 months in, founder also works a 9-5, so time is extremely limited.

PRIORITIES for the second half of year one:
1. FUNDING — finding grants, donors, and sustainable revenue. This is the #1 need.
2. SCALE — how to grow reach and impact without burning out as a solo founder.
3. ORG-BUILDING — systems, structure, and credibility that attract money and partners.

DO NOT focus on: teacher outreach, classroom connections, or supply logistics.
Those happen naturally. The founder needs help with the business side of the nonprofit.
"""

DIGEST_TYPES = [
    "how_to_scale",
    "grant_or_funder",
    "org_suggestion",
    "donor_to_reach",
]


def get_digest_type(date: datetime.date | None = None) -> str:
    if date is None:
        date = datetime.date.today()
    return DIGEST_TYPES[date.toordinal() % 4]


def build_digest(scraped_data: dict, date: datetime.date | None = None) -> dict:
    """
    scraped_data keys: articles, orgs, listings, grants
    Returns dict with keys: digest_type, subject, html_body, plain_body
    """
    if date is None:
        date = datetime.date.today()

    digest_type = get_digest_type(date)
    client = anthropic.Anthropic()

    system_prompt = f"""You are a strategic nonprofit advisor helping the founder of Doodle Street.

{DOODLE_STREET_CONTEXT}

Today is {date.strftime('%A, %B %d, %Y')}.

Your job is to produce ONE highly curated, actionable digest item for the founder.
Be warm, direct, and specific. No fluff. The founder is time-constrained so
every word should count. Format your response as JSON with these exact keys:
- subject: email subject line (engaging, specific, under 60 chars)
- headline: the main headline for this digest section (under 80 chars)
- body_markdown: the full digest content in Markdown (use headers, bullets, links)
- type_label: a friendly label for the type (e.g. "Today's Resource", "Orgs to Know", etc.)
"""

    scraped_summary = json.dumps(scraped_data, indent=2, default=str)[:8000]

    type_instructions = {
        "how_to_scale": (
            "Find or recommend ONE specific, actionable resource — article, guide, book chapter, "
            "podcast episode, or framework — on ONE of these topics for a first-year nonprofit founder: "
            "fundraising strategy, building a donor base from scratch, nonprofit revenue diversification, "
            "scaling a small nonprofit, grant writing for beginners, or board development. "
            "NOT about programs or teaching — purely about money and organizational growth. "
            "Summarize the 3-5 most actionable takeaways. Include the URL if it's a real link. "
            "Be specific enough that the founder can act on it in under 30 minutes."
        ),
        "grant_or_funder": (
            "Identify ONE specific grant opportunity OR one specific foundation/funder "
            "that is a strong match for Doodle Street right now. Use the scraped grants data "
            "if relevant, otherwise use your knowledge of real foundations that fund: "
            "arts education, school supply programs, youth arts, equity in education, or "
            "community-based nonprofits in their early years. "
            "Include: funder name, what they fund, typical grant size, deadline if known, "
            "why it's a fit for Doodle Street, and exactly where to apply or learn more. "
            "Real foundations to draw from: NEA, Walmart Foundation, Michael & Susan Dell Foundation, "
            "PNC Grow Up Great, Crayola Champion Creatively, Dollar General Literacy Foundation, "
            "local community foundations, arts council grants, corporate giving programs."
        ),
        "org_suggestion": (
            "Give ONE concrete action Doodle Street should take THIS WEEK to get closer to funding "
            "or scale — something a solo founder with a day job can realistically do in 1-2 hours. "
            "Focus on: donor cultivation, fundraising infrastructure, grant pipeline, "
            "online presence that attracts donors, earned revenue ideas, or building credibility "
            "with funders (impact data, testimonials, annual report, etc.). "
            "Be extremely specific — name the exact tool, platform, template, or person type. "
            "Include the WHY (how this directly leads to money or scale) and the HOW (step by step)."
        ),
        "donor_to_reach": (
            "Suggest ONE specific type of donor or funder for Doodle Street's founder to "
            "identify and reach out to this week. Focus on: individual major donors who give to arts "
            "or education, corporate sponsors (art supply companies, office supply retailers, "
            "local businesses), foundation program officers, or impact investors in education equity. "
            "NOT teachers, NOT school administrators — people who write checks or make grants. "
            "Include: who they are, why they'd care about Doodle Street's mission, "
            "exactly how to find them (LinkedIn search string, database, event, etc.), "
            "and a specific 3-sentence cold outreach message the founder can copy and personalize."
        ),
    }

    user_prompt = f"""Digest type for today: {digest_type}

Task: {type_instructions[digest_type]}

Scraped data from nonprofit resource sites (use what's relevant, supplement with your knowledge):
{scraped_summary}

Return ONLY valid JSON matching the schema described in the system prompt.
"""

    response = client.messages.create(
        model="claude-opus-4-7",
        max_tokens=1500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw = response.content[0].text.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    raw = raw.strip()

    result = json.loads(raw)
    result["digest_type"] = digest_type
    result["date"] = date.isoformat()
    return result
