# Doodle Street Daily Digest — Setup Guide

A daily 4am email that gives you one curated nonprofit insight each morning.

## What it sends (rotates daily)

| Day cycle | Content |
|-----------|---------|
| Day 1 | How-to article or resource from Candid, Instrumentl, Blue Avocado, etc. |
| Day 2 | 3–5 nonprofits in the art-education-for-kids space to know |
| Day 3 | One concrete action Doodle Street should take this week |
| Day 4 | One specific person to reach out to (with a template opener) |

---

## One-time setup (takes ~15 minutes)

### 1. Fork / clone this repo to your GitHub account

### 2. Get an Anthropic API key
- Go to https://console.anthropic.com/
- Create an API key (free tier gives you enough for daily emails)

### 3. Set up Gmail to send the email
You need a **Gmail App Password** (different from your regular password).

1. Make sure 2-Step Verification is ON for your Google account
2. Go to: https://myaccount.google.com/apppasswords
3. Create a new App Password → name it "Doodle Street Digest"
4. Copy the 16-character password

> **Tip:** You can send FROM your main Gmail and TO your main Gmail.
> Or create a free `doodlestreet.org` Google Workspace account and send from that.

### 4. Add GitHub Secrets

Go to your repo → **Settings → Secrets and variables → Actions → New repository secret**

| Secret name | Value |
|-------------|-------|
| `ANTHROPIC_API_KEY` | Your Anthropic key (`sk-ant-...`) |
| `GMAIL_SENDER` | The Gmail address you send FROM |
| `GMAIL_APP_PASSWORD` | The 16-char App Password from step 3 |
| `RECIPIENT_EMAIL` | `jaramontez@gmail.com` |

### 5. Enable GitHub Actions
- Go to your repo → **Actions** tab
- Click "I understand my workflows, go ahead and enable them"
- The digest will run every day at 9 AM UTC (4 AM EST / 5 AM EDT)

---

## Test it right now

Go to **Actions → Doodle Street Daily Digest → Run workflow**

Set "Dry run" to `true` to see the output without sending an email.
Set "Dry run" to `false` to actually send it to your inbox.

---

## Run locally

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
export GMAIL_SENDER=you@gmail.com
export GMAIL_APP_PASSWORD=xxxx-xxxx-xxxx-xxxx
export RECIPIENT_EMAIL=jaramontez@gmail.com

# Dry run (prints digest, no email)
python -m digest.main --dry-run

# Send it
python -m digest.main

# Test a specific day type
python -m digest.main --date 2026-05-28 --dry-run
python -m digest.main --date 2026-05-29 --dry-run
python -m digest.main --date 2026-05-30 --dry-run
python -m digest.main --date 2026-05-31 --dry-run
```

---

## Adjusting the timing

Edit `.github/workflows/daily_digest.yml` — the cron line:
```
- cron: "0 9 * * *"   ← 9 AM UTC = 4 AM EST
- cron: "0 8 * * *"   ← 8 AM UTC = 4 AM EDT (daylight saving)
```

---

## Sources it scrapes

- **Candid.org** — nonprofit learning hub
- **Instrumentl** — grant writing blog
- **Blue Avocado** — practical nonprofit management
- **NonprofitAF** — candid nonprofit leadership
- **Idealist.org** — nonprofits & listings in art education
- **Grants.gov** — federal arts grant opportunities
