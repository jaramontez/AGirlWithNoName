"""
Send the daily digest email via Gmail SMTP using an App Password,
or via SendGrid if SENDGRID_API_KEY is set.
"""
import os
import smtplib
import textwrap
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import markdown


def _build_html(digest: dict) -> str:
    date_str = digest.get("date", "")
    type_label = digest.get("type_label", "Daily Digest")
    headline = digest.get("headline", "")
    body_md = digest.get("body_markdown", "")
    body_html = markdown.markdown(body_md, extensions=["extra", "nl2br"])

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Doodle Street Digest</title>
<style>
  body {{ font-family: Georgia, serif; background: #fdf8f3; color: #2c2c2c; margin: 0; padding: 0; }}
  .wrapper {{ max-width: 620px; margin: 0 auto; padding: 32px 20px; }}
  .header {{ border-bottom: 3px solid #e8603c; padding-bottom: 16px; margin-bottom: 24px; }}
  .badge {{ display: inline-block; background: #e8603c; color: #fff; font-size: 11px;
            font-family: sans-serif; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;
            padding: 4px 10px; border-radius: 3px; margin-bottom: 8px; }}
  .org-name {{ font-family: sans-serif; font-size: 13px; color: #888; margin: 0; }}
  .date {{ font-family: sans-serif; font-size: 12px; color: #bbb; margin: 0; }}
  h1 {{ font-size: 24px; color: #1a1a1a; margin: 0 0 4px 0; line-height: 1.3; }}
  .body {{ line-height: 1.7; font-size: 16px; }}
  .body h2, .body h3 {{ font-family: sans-serif; color: #e8603c; }}
  .body a {{ color: #e8603c; }}
  .body ul {{ padding-left: 20px; }}
  .body li {{ margin-bottom: 6px; }}
  .footer {{ margin-top: 40px; padding-top: 16px; border-top: 1px solid #eee;
             font-family: sans-serif; font-size: 12px; color: #bbb; }}
</style>
</head>
<body>
<div class="wrapper">
  <div class="header">
    <span class="badge">{type_label}</span>
    <p class="org-name">Doodle Street &mdash; Founder Digest</p>
    <p class="date">{date_str}</p>
    <h1>{headline}</h1>
  </div>
  <div class="body">
    {body_html}
  </div>
  <div class="footer">
    You're receiving this because you set up the Doodle Street daily digest.
    &bull; <a href="https://doodlestreet.org" style="color:#bbb;">doodlestreet.org</a>
  </div>
</div>
</body>
</html>"""


def _build_plain(digest: dict) -> str:
    date_str = digest.get("date", "")
    type_label = digest.get("type_label", "Daily Digest")
    headline = digest.get("headline", "")
    body_md = digest.get("body_markdown", "")

    return textwrap.dedent(f"""
    DOODLE STREET FOUNDER DIGEST
    {type_label} | {date_str}
    {'=' * 50}

    {headline}

    {body_md}

    ---
    doodlestreet.org
    """).strip()


def send_digest(digest: dict) -> None:
    recipient = os.environ["RECIPIENT_EMAIL"]
    subject = digest.get("subject", "Your Doodle Street Digest")

    html_body = _build_html(digest)
    plain_body = _build_plain(digest)

    sendgrid_key = os.environ.get("SENDGRID_API_KEY")
    if sendgrid_key:
        _send_via_sendgrid(sendgrid_key, recipient, subject, html_body, plain_body)
    else:
        _send_via_gmail(recipient, subject, html_body, plain_body)


def _send_via_gmail(recipient: str, subject: str, html_body: str, plain_body: str) -> None:
    sender = os.environ["GMAIL_SENDER"]
    app_password = os.environ["GMAIL_APP_PASSWORD"]

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"Doodle Street Digest <{sender}>"
    msg["To"] = recipient

    msg.attach(MIMEText(plain_body, "plain"))
    msg.attach(MIMEText(html_body, "html"))

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, app_password)
        server.sendmail(sender, recipient, msg.as_string())

    print(f"[emailer] sent via Gmail to {recipient}")


def _send_via_sendgrid(api_key: str, recipient: str, subject: str, html_body: str, plain_body: str) -> None:
    import urllib.request
    import json

    sender = os.environ.get("GMAIL_SENDER", "digest@doodlestreet.org")
    payload = {
        "personalizations": [{"to": [{"email": recipient}]}],
        "from": {"email": sender, "name": "Doodle Street Digest"},
        "subject": subject,
        "content": [
            {"type": "text/plain", "value": plain_body},
            {"type": "text/html", "value": html_body},
        ],
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        "https://api.sendgrid.com/v3/mail/send",
        data=data,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        print(f"[emailer] sent via SendGrid — status {resp.status}")
