import imaplib
import email
from email.header import decode_header
import csv
import random

IMAP_SERVER = "imap.gmail.com"
IMAP_PORT = 993
EMAIL_ACCOUNT = "insert email"
APP_PASSWORD = "16 char pwd"

OUTPUT_FILE = "emails_subset_spam"
SAMPLE_SIZE = 200  # how many emails to export (adjust as needed)


def clean_text(text):
    """Cleans up strings for CSV export."""
    if not text:
        return ""
    return " ".join(text.replace("\n", " ").split())

def decode_mime_words(s):
    """Handles encoded subject lines like =?UTF-8?..."""
    decoded = decode_header(s)
    subject = ""
    for part, enc in decoded:
        if isinstance(part, bytes):
            subject += part.decode(enc or "utf-8", errors="ignore")
        else:
            subject += part
    return subject

def fetch_emails(mailbox, label):
    """Fetches emails from a mailbox (INBOX or SPAM)."""
    emails = []
    status, _ = mail.select(mailbox)
    if status != "OK":
        print(f"Could not open {mailbox}")
        return emails

    status, data = mail.search(None, "ALL")
    if status != "OK":
        return emails

    ids = data[0].split()
    ids = [id_.decode() for id_ in ids]
    ids = ids[-50:]
    for num in ids:
        res, msg_data = mail.fetch(num, "(RFC822)")
        if res != "OK":
            continue
        msg = email.message_from_bytes(msg_data[0][1])

        # From
        from_ = msg.get("From", "")
        # Subject
        subject = decode_mime_words(msg.get("Subject", ""))
        # Body (only first text/plain part)
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                if part.get_content_type() == "text/plain":
                    try:
                        body = part.get_payload(decode=True).decode(errors="ignore")
                        break
                    except:
                        continue
        else:
            try:
                body = msg.get_payload(decode=True).decode(errors="ignore")
            except:
                body = msg.get_payload()

        emails.append({
            "gmail_label": label,
            "from": clean_text(from_),
            "subject": clean_text(subject),
            "body_preview": clean_text(body[:200])  # only first 200 chars
        })

    return emails


mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
mail.login(EMAIL_ACCOUNT, APP_PASSWORD)

all_emails = []
all_emails.extend(fetch_emails("INBOX", "INBOX"))
all_emails.extend(fetch_emails("[Gmail]/Spam", "SPAM"))

mail.logout()

print(f"Fetched {len(all_emails)} total emails")

# Take random subset
if len(all_emails) > SAMPLE_SIZE:
    subset = random.sample(all_emails, SAMPLE_SIZE)
else:
    subset = all_emails

# Save to CSV
with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["gmail_label", "from", "subject", "body_preview"])
    writer.writeheader()
    writer.writerows(subset)

print(f"Saved {len(subset)} emails to {OUTPUT_FILE}")