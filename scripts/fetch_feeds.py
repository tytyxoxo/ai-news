"""Fetch trusted RSS/Atom feeds into feeds/candidates.json for the daily-ai-news routine.

Runs in GitHub Actions (open internet) because the routine's cloud session
can't reach news sites. Stdlib only.
"""
import gzip
import html
import json
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from pathlib import Path

# (name, url, ai_only) — ai_only=False means a general feed, keep only items matching AI_RE.
# No feed exists for Anthropic, Meta AI; VentureBeat (429) and Reuters (401) block bots.
FEEDS = [
    ("OpenAI", "https://openai.com/news/rss.xml", True),
    ("Google DeepMind", "https://deepmind.google/blog/rss.xml", True),
    ("Google AI", "https://blog.google/technology/ai/rss/", True),
    ("Microsoft Research", "https://www.microsoft.com/en-us/research/feed/", False),
    ("NVIDIA Blog", "https://blogs.nvidia.com/feed/", False),
    ("arXiv cs.AI", "https://rss.arxiv.org/rss/cs.AI", True),
    ("TechCrunch", "https://techcrunch.com/category/artificial-intelligence/feed/", True),
    ("The Verge", "https://www.theverge.com/rss/ai-artificial-intelligence/index.xml", True),
    ("Ars Technica", "https://arstechnica.com/ai/feed/", True),
    ("MIT Technology Review", "https://www.technologyreview.com/topic/artificial-intelligence/feed", True),
    ("Wired", "https://www.wired.com/feed/tag/ai/latest/rss", True),
    ("Bloomberg", "https://feeds.bloomberg.com/technology/news.rss", False),
    ("Hugging Face", "https://huggingface.co/blog/feed.xml", True),
    ("Blognone", "https://www.blognone.com/atom.xml", False),
    ("The Standard", "https://thestandard.co/category/news/tech/feed/", False),
    ("Techsauce", "https://techsauce.co/feed", False),
    ("Brand Inside", "https://brandinside.asia/feed/", False),
    ("TechHub", "https://www.techhub.in.th/feed/", False),
    ("Prachachat", "https://www.prachachat.net/feed", False),
    ("NECTEC", "https://www.nectec.or.th/feed", False),
]

# ponytail: keyword filter for general feeds, misses AI stories that never say these words
AI_RE = re.compile(
    r"\bA\.?I\b|artificial intelligence|machine learning|\bLLMs?\b|\bGPT|ChatGPT|Gemini|Claude|"
    r"OpenAI|Anthropic|DeepMind|Copilot|chatbot|neural|generative|"
    r"ปัญญาประดิษฐ์|เอไอ|แชตบอต|แชทบอท",
    re.IGNORECASE,
)
WINDOW_HOURS = 36  # routine applies the exact 24h cut; slack covers late cron runs
PER_FEED_CAP = 20
SUMMARY_CHARS = 1200
SHORT_SUMMARY = 400  # below this, fetch the article page for real text
UA = "Mozilla/5.0 (compatible; ai-news-bot/1.0)"  # a URL in the UA gets 418 from TechHub


def local(tag):
    return tag.rsplit("}", 1)[-1]


def child_text(el, *names):
    for c in el:
        if local(c.tag) in names and (c.text or "").strip():
            return c.text.strip()
    return ""


def parse_date(s):
    if not s:
        return None
    try:
        d = parsedate_to_datetime(s)  # RSS pubDate
    except (TypeError, ValueError):
        try:
            d = datetime.fromisoformat(s.replace("Z", "+00:00"))  # Atom / dc:date
        except ValueError:
            return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def clean(s):
    s = re.sub(r"<[^>]+>", " ", s or "")
    return re.sub(r"\s+", " ", html.unescape(s)).strip()


def parse_feed(xml_bytes):
    """Yield (title, url, published_dt, summary) from RSS or Atom bytes."""
    root = ET.fromstring(xml_bytes)
    for el in root.iter():
        kind = local(el.tag)
        if kind not in ("item", "entry"):
            continue
        url = child_text(el, "link") if kind == "item" else ""
        if not url:  # Atom: <link href=... rel="alternate"/>
            for c in el:
                if local(c.tag) == "link" and c.get("rel", "alternate") == "alternate":
                    url = c.get("href", "")
                    break
        published = parse_date(child_text(el, "pubDate", "published", "date", "updated"))
        # longest wins: TechCrunch's description is one line, content:encoded is the article
        summary = max((clean(c.text) for c in el if local(c.tag) in ("encoded", "description", "summary", "content")), key=len, default="")
        yield clean(child_text(el, "title")), url.strip(), published, summary


def decode(body):
    return gzip.decompress(body) if body[:2] == b"\x1f\x8b" else body  # DeepMind always gzips


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=20) as r:
        return decode(r.read())


def article_text(url, fetcher=fetch):
    """Paragraph text from an article page, for feeds that only ship a one-line description."""
    page = fetcher(url).decode("utf-8", "replace")
    page = re.sub(r"(?is)<(script|style|nav|footer|aside)\b.*?</\1>", " ", page)
    tags = re.findall(r"(?is)<p\b([^>]*)>(.*?)</p>", page)
    # WordPress (TechCrunch…) marks body text; centered ones are promo banners
    body = [t for t in tags if "wp-block-paragraph" in t[0] and "align-center" not in t[0]]
    paras = [clean(text) for _, text in body or tags]
    return " ".join(p for p in paras if len(p) > 60)  # ponytail: drops captions/bylines, regex not a DOM


def seen_urls(articles_dir):
    urls = set()
    for f in Path(articles_dir).glob("*.md"):
        urls.update(re.findall(r"\]\((https?://[^)\s]+)\)", f.read_text(encoding="utf-8")))
    return urls


def collect(feeds, now, seen, fetcher=fetch):
    cutoff = now - timedelta(hours=WINDOW_HOURS)
    items, failed = [], []
    for name, url, ai_only in feeds:
        try:
            entries = list(parse_feed(fetcher(url)))
        except Exception as e:  # one broken feed must not kill the run
            failed.append({"source": name, "error": f"{type(e).__name__}: {e}"[:200]})
            print(f"FAIL {name}: {e}", file=sys.stderr)
            continue
        kept = []
        for title, link, published, summary in entries:
            if not link or not published or published < cutoff or published > now + timedelta(hours=1):
                continue
            if link in seen or (not ai_only and not AI_RE.search(f"{title} {summary}")):
                continue
            kept.append({
                "source": name,
                "title": title,
                "url": link,
                "published": published.astimezone(timezone.utc).isoformat(),
                "summary": summary[:SUMMARY_CHARS],
            })
        kept.sort(key=lambda i: i["published"], reverse=True)
        kept = kept[:PER_FEED_CAP]
        for item in kept:
            if len(item["summary"]) < SHORT_SUMMARY:
                try:
                    body = article_text(item["url"], fetcher)
                    if len(body) > len(item["summary"]):
                        item["summary"] = body[:SUMMARY_CHARS]
                except Exception as e:  # keep the feed summary, flag it for the routine
                    print(f"     article fetch failed {item['url']}: {e}", file=sys.stderr)
        items += kept
        print(f"OK   {name}: {len(entries)} entries -> {len(kept)} kept", file=sys.stderr)
    items.sort(key=lambda i: i["published"], reverse=True)
    return {
        "generated_at": now.isoformat(),
        "window_hours": WINDOW_HOURS,
        "failed_feeds": failed,
        "items": items,
    }


if __name__ == "__main__":
    root = Path(__file__).resolve().parent.parent
    out = collect(FEEDS, datetime.now(timezone.utc), seen_urls(root / "articles"))
    path = root / "feeds" / "candidates.json"
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"Wrote {len(out['items'])} items, {len(out['failed_feeds'])} failed feeds -> {path}", file=sys.stderr)
    if len(out["failed_feeds"]) == len(FEEDS):
        sys.exit("All feeds failed")
