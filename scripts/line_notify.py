"""Push an article (one bubble per news item) or a plain alert to LINE.

Usage: line_notify.py articles/2026-11-05-brief.md
       line_notify.py --text "message"
Env:   LINE_CHANNEL_ACCESS_TOKEN, LINE_TO
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request

MAX_BUBBLES = 5  # LINE push limit per request; quota counts recipients, not bubbles
MAX_CHARS = 5000  # LINE text message limit
SEP = "\n\n──────────────\n\n"


def clean(md):
    c = re.sub(r"^#{1,6}\s*", "", md, flags=re.MULTILINE)
    c = re.sub(r"\*\*([^*]+)\*\*", r"\1", c)
    c = re.sub(r"\[([^\]]+)\]\(https?://[^\)]*\)", r"\1", c)
    c = re.sub(r"_([^_]+)_", r"\1", c)
    c = re.sub(r"\n{3,}", "\n\n", c)
    return c.strip()


def build_messages(content):
    m = re.search(r"^date:\s*(\d{4})-(\d{2})-(\d{2})", content, re.MULTILINE)
    date_fmt = f"{m[3]}/{m[2]}/{m[1]}" if m else ""
    body = re.sub(r"^---[\s\S]*?---\s*", "", content, count=1)  # frontmatter
    parts = [p for p in re.split(r"\n+---\n+", body.strip()) if p.strip()]
    footer = parts.pop() if len(parts) > 1 and parts[-1].lstrip().startswith("_") else None
    texts = [clean(p) for p in parts] or [""]
    if len(texts) > MAX_BUBBLES:  # skill caps at 5 items; never drop news if it slips
        texts = texts[: MAX_BUBBLES - 1] + [SEP.join(texts[MAX_BUBBLES - 1 :])]
    texts[0] = f"🗞 สรุปข่าว AI ประจำวัน {date_fmt}\n\n{texts[0]}".rstrip()
    if footer:
        texts[-1] += "\n\n" + clean(footer)
    return [t if len(t) <= MAX_CHARS else t[: MAX_CHARS - 1] + "…" for t in texts]


def push(texts):
    payload = {"to": os.environ["LINE_TO"], "messages": [{"type": "text", "text": t} for t in texts]}
    req = urllib.request.Request(
        "https://api.line.me/v2/bot/message/push",
        data=json.dumps(payload).encode(),
        headers={
            "Authorization": f"Bearer {os.environ['LINE_CHANNEL_ACCESS_TOKEN']}",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"LINE {r.status}: {r.read().decode()}")
    except urllib.error.HTTPError as e:
        sys.exit(f"LINE push failed {e.code}: {e.read().decode()}")


if __name__ == "__main__":
    if sys.argv[1:2] == ["--text"]:
        texts = [sys.argv[2]]
    else:
        with open(sys.argv[1], encoding="utf-8") as f:
            texts = build_messages(f.read())
    print(f"{len(texts)} bubble(s): {[len(t) for t in texts]} chars")
    push(texts)
