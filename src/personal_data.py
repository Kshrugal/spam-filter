import imaplib
import email
from email.header import decode_header
from email import message_from_bytes
import csv
import sys
from typing import Optional

IMAP_SERVER = 'imap.gmail.com'
IMAP_PORT = 993
EMAIL_ACCOUNT = 'gmail'
APP_PASSWORD = 'enter 16 char pass'
OUTPUT_CSV = "gmail_spam_messages.csv"
SPAM_FOLDER = "[Gmail]/Spam"

def decode_mime_words(s: Optional[bytes | str]) -> str:
    """Decode email headers safely."""
    if not s:
        return ""
    decoded_fragments = []
    for part, enc in decode_header(s):
        if isinstance(part, bytes):
            try:
                if not enc or enc.lower() in ("unknown-8bit", "x-unknown"):
                    enc = "utf-8"
                decoded_fragments.append(part.decode(enc, errors="replace"))
            except LookupError:
                decoded_fragments.append(part.decode("utf-8", errors="replace"))
        else:
            decoded_fragments.append(part)
    return "".join(decoded_fragments)

def safe_decode(payload: bytes, charset: Optional[str]) -> str:
    """Decode email body safely, fallback to utf-8 if charset is unknown."""
    if not payload:
        return ""
    if not charset or charset.lower() in ("unknown-8bit", "x-unknown", "binary"):
        charset = "utf-8"
    try:
        return payload.decode(charset, errors="replace")
    except LookupError:
        return payload.decode("utf-8", errors="replace")

def get_text_from_message(msg) -> str:
    """Extract plain text snippet from email message."""
    if msg.is_multipart():
        for part in msg.walk():
            ctype = part.get_content_type()
            disp = str(part.get("Content-Disposition"))
            if ctype == "text/plain" and "attachment" not in disp:
                payload = part.get_payload(decode=True)
                return safe_decode(payload, part.get_content_charset())
    else:
        payload = msg.get_payload(decode=True)
        return safe_decode(payload, msg.get_content_charset())
    return ""

def fetch_all_spam(mailbox, spam_folder):
    """Fetch all messages from the given spam folder and save to CSV."""
    rv, data = mailbox.select(spam_folder, readonly=True)
    if rv != "OK":
        print(f"Failed to select folder '{spam_folder}'")
        sys.exit(1)

    rv, data = mailbox.search(None, "ALL")
    if rv != "OK" or not data or not data[0]:
        print("No messages found in Spam folder.")
        return

    msg_ids = data[0].split()  # bytes
    print(f"Found {len(msg_ids)} messages in Spam.")

    rows = []

    for i, mid in enumerate(msg_ids, start=1):
        rv, fetched = mailbox.fetch(mid, "(RFC822)")
        if rv != "OK":
            print(f"Failed to fetch id {mid}")
            continue

        raw_msg = None
        for part in fetched:
            if isinstance(part, tuple) and part[1]:
                raw_msg = part[1]
                break
        if not raw_msg:
            continue

        msg = message_from_bytes(raw_msg)
        subject = decode_mime_words(msg.get("Subject"))
        from_ = decode_mime_words(msg.get("From"))
        date_ = decode_mime_words(msg.get("Date"))
        snippet = get_text_from_message(msg).replace("\r", " ").replace("\n", " ").strip()

        rows.append({
            "uid": mid.decode("utf-8"),
            "subject": subject,
            "from": from_,
            "date": date_,
            "snippet": snippet
        })

        if i % 50 == 0:
            print(f"Downloaded {i}/{len(msg_ids)} messages...")

    # Save to CSV
    fieldnames = ["uid", "subject", "from", "date", "snippet"]
    with open(OUTPUT_CSV, "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for r in rows:
            writer.writerow(r)

    print(f"Saved {len(rows)} messages to {OUTPUT_CSV}")

# ---------------- MAIN ----------------
if __name__ == "__main__":
    try:
        mail = imaplib.IMAP4_SSL(IMAP_SERVER, IMAP_PORT)
        mail.login(EMAIL_ACCOUNT, APP_PASSWORD)
        fetch_all_spam(mail, SPAM_FOLDER)
        mail.logout()
    except imaplib.IMAP4.error as e:
        print("IMAP login failed:", e)
        sys.exit(1)