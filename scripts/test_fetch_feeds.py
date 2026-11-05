"""Run: python3 scripts/test_fetch_feeds.py"""
import gzip
from datetime import datetime, timezone

from fetch_feeds import collect, decode

NOW = datetime(2026, 11, 5, 0, 0, tzinfo=timezone.utc)

RSS = b"""<?xml version="1.0"?><rss xmlns:content="http://purl.org/rss/1.0/modules/content/"><channel>
<item><title>New AI model</title><link>https://a.com/new</link><pubDate>Wed, 04 Nov 2026 20:00:00 +0000</pubDate>
<description>&lt;p&gt;Short &amp;amp; sweet&lt;/p&gt;</description></item>
<item><title>Old AI model</title><link>https://a.com/old</link><pubDate>Mon, 02 Nov 2026 00:00:00 +0000</pubDate></item>
<item><title>Seen AI model</title><link>https://a.com/seen</link><pubDate>Wed, 04 Nov 2026 21:00:00 +0000</pubDate></item>
<item><title>Football results</title><link>https://a.com/sport</link><pubDate>Wed, 04 Nov 2026 22:00:00 +0000</pubDate></item>
</channel></rss>"""

ATOM = b"""<?xml version="1.0"?><feed xmlns="http://www.w3.org/2005/Atom">
<entry><title>Verge piece</title><link rel="alternate" href="https://v.com/x"/>
<published>2026-11-04T17:42:15-05:00</published><content type="html">&lt;b&gt;Body&lt;/b&gt;</content></entry>
</feed>"""

PAGE = ("<html><script>var p='<p>no</p>'</script><p>Caption</p><p class=x>" + "Real article text. " * 5 + "</p></html>").encode()
feeds = {"rss": RSS, "atom": gzip.compress(ATOM), "broken": b"<html>nope", "https://a.com/new": PAGE}
out = collect(
    [("General", "rss", False), ("Verge", "atom", True), ("Broken", "broken", True)],
    NOW,
    {"https://a.com/seen"},
    fetcher=lambda u: decode(feeds[u]),
)
urls = [i["url"] for i in out["items"]]
assert urls == ["https://v.com/x", "https://a.com/new"], urls  # newest first; old/seen/non-AI dropped
assert out["items"][1]["summary"] == ("Real article text. " * 5).strip(), out["items"][1]  # short summary -> page text
assert out["items"][0]["summary"] == "Body"  # article fetch failed (KeyError) -> feed summary kept
assert out["items"][0]["published"] == "2026-11-04T22:42:15+00:00"
assert [f["source"] for f in out["failed_feeds"]] == ["Broken"]
print("ok")
