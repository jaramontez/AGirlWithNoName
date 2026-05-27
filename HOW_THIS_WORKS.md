# How Your Daily Digest Works — Plain English

---

## What we built

Every morning at 4am, you get an email with one of these four things:

1. **A how-to** — a specific article or guide on fundraising or growing a nonprofit
2. **A grant or funding opportunity** — one real program you can apply to right now
3. **One action to take this week** — something concrete that moves Doodle Street forward
4. **A donor to reach out to** — who they are, why they'd care, and what to say

It rotates through all four types so you're not getting the same thing every day.

The email pulls from real websites like Candid, Instrumentl, Dick Blick's donation page, Michaels Foundation, the Pollination Project, and others — then uses AI to turn that raw information into something actually useful for you.

---

## The pieces

### GitHub — your free server in the cloud

Think of GitHub like Google Drive, but for code. It stores your project files online.

The important part for you: GitHub has a feature called **Actions**. Actions lets you say *"run this program every day at 4am"* — and GitHub just does it, for free, on its own computers. You don't need to leave your laptop on. You don't need to pay for a server. GitHub wakes up, runs your digest, sends the email, and goes back to sleep.

That's all GitHub is doing here — it's your alarm clock and runner.

### The scraper — the part that goes out and reads websites

Every morning before your email goes out, the program visits a list of websites:
- Candid.org (nonprofit how-to articles)
- Instrumentl (grant writing resources)
- Blue Avocado and NonprofitAF (nonprofit management blogs)
- Dick Blick, Michaels Foundation, NAMTA, Pollination Project, Awesome Foundation, and others (grant and donation programs)
- Idealist.org (nonprofits in the arts education space)
- Grants.gov (federal arts grants)

It reads those pages the same way you would — just much faster — and collects whatever looks useful. Think of it like having an assistant who spent 20 minutes every morning skimming 10 websites before you woke up.

### Claude (the AI) — the part that makes it readable

After the scraper collects raw information, it hands everything to Claude (Anthropic's AI — the same AI you're talking to right now). Claude reads through all of it and writes you one clean, specific, useful summary — not a wall of links, but an actual recommendation with context.

Claude also knows a lot about Doodle Street specifically (mission, stage, what you need right now) so it filters everything through that lens. It's been told: *don't talk about teacher outreach, focus on money and scale.*

The Anthropic API Key in your GitHub settings is what lets the program use Claude. It's like a password that says "yes, this program is allowed to use the AI."

### SendGrid — the part that sends the email

SendGrid is an email delivery service. The reason we use it instead of just sending directly from Gmail is reliability — email systems are suspicious of automated emails, and SendGrid has a good reputation with Gmail so your digest actually arrives instead of getting blocked.

Your SendGrid API Key (also stored in GitHub) is what lets the program say "SendGrid, please send this email on my behalf."

The whole flow is:
> GitHub wakes up → scraper reads websites → Claude writes the digest → SendGrid delivers it to your inbox

### Secrets — your passwords, stored safely

In GitHub, there's a special place called **Secrets** where you stored four private keys:

| Secret | What it does |
|--------|-------------|
| `ANTHROPIC_API_KEY` | Lets the program use Claude AI |
| `SENDGRID_API_KEY` | Lets the program send email through SendGrid |
| `GMAIL_SENDER` | The email address the digest comes from |
| `RECIPIENT_EMAIL` | Where the digest gets delivered (your Gmail) |

These are encrypted — even if someone looked at your GitHub, they couldn't read these values.

---

## What you never have to touch again

Once this is running, you don't touch any of it. No logging in, no clicking buttons. The digest just shows up in your inbox every morning.

The only reason you'd come back to GitHub is if you wanted to change something — like adjusting what topics the digest covers, adding a new website to scrape, or changing the delivery time.

---

## Cost

| Service | Cost |
|---------|------|
| GitHub | Free |
| SendGrid | Free (up to 100 emails/day, you're sending 1) |
| Anthropic (Claude AI) | Pay-as-you-go — roughly **$0.10–$0.30 per email** |

The AI is the only ongoing cost. At one email a day, that's about **$3–$9/month**.

---

## If something breaks

The most likely things that could go wrong:

- **Email goes to spam** — open it and click "Not spam." That teaches Gmail to trust it.
- **Workflow fails** — go to GitHub → Actions tab → click the failed run → read the red error message. Usually it's a temporary website being down.
- **SendGrid stops working** — log into sendgrid.com and make sure your sender email is still verified.

---

*Built for Doodle Street — doodlestreet.org*
