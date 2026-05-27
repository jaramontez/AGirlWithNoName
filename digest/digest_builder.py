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
Stage: ~6 months in, founder is also working a 9-5, so capacity is limited.
Goals for the second half of the year: grow impact, build key relationships,
find grants, connect with aligned organizations and donors.
"""

DIGEST_TYPES = [
    "how_to_resource",
    "similar_orgs",
    "org_suggestion",
    "person_to_reach_out",
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
        "how_to_resource": (
            "Pick the SINGLE most useful how-to article, blog post, or resource "
            "from the scraped data for a first-year nonprofit founder running an art-supply "
            "program for kids. Summarize the key takeaways in 3-5 bullets. Include the URL. "
            "If nothing scraped is great, recommend a specific real resource you know of."
        ),
        "similar_orgs": (
            "Identify 3-5 nonprofits in the art education / arts-supplies-for-kids space "
            "from the scraped orgs data. For each: name, what they do, why Doodle Street "
            "should know them, and a URL. If scraped data is thin, use your knowledge to "
            "suggest real orgs in this space."
        ),
        "org_suggestion": (
            "Give ONE concrete, specific action Doodle Street should take in the next 7 days "
            "to grow as an organization — something realistic for a founder with limited time. "
            "Could be a partnership to pursue, a program tweak, a social media move, "
            "a grant to apply for, or an operational improvement. Be very specific."
        ),
        "person_to_reach_out": (
            "Suggest ONE specific type of person (or a real example if you know one) "
            "for Doodle Street's founder to connect with this week — could be a grant writer, "
            "a donor profile type, a peer founder, a school administrator, a community leader, "
            "or an arts advocate. Explain exactly who, why, and how to approach them "
            "(what to say in the first message). Include a LinkedIn search tip or a real org "
            "where this type of person can be found."
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
