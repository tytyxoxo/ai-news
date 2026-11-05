"""Run: python3 scripts/test_line_notify.py"""
from line_notify import build_messages

ITEM = "## {n}. หัวข้อ {n}\n\nเนื้อ **หนา** ข่าว {n}\n\nที่มา: [Site](https://x.com/{n})"
FOOTER = "_สร้างโดย Claude Code Routine เวลา 09:00 น._"


def article(n):
    return "---\ndate: 2026-11-05\n---\n\n" + "\n\n---\n\n".join([ITEM.format(n=i) for i in range(1, n + 1)] + [FOOTER])


m = build_messages(article(3))
assert len(m) == 3, m
assert m[0].startswith("🗞 สรุปข่าว AI ประจำวัน 05/11/2026\n\n1. หัวข้อ 1"), m[0]
assert "เนื้อ หนา ข่าว 1" in m[0] and "ที่มา: Site" in m[0] and "https://" not in m[0]
assert m[2].endswith("ที่มา: Site\n\nสร้างโดย Claude Code Routine เวลา 09:00 น."), m[2]
assert "---" not in "".join(m)

m = build_messages(article(7))  # over the 5-bubble cap: tail merged, nothing dropped
assert len(m) == 5 and "หัวข้อ 7" in m[4] and "หัวข้อ 5" in m[4]

empty = "---\ndate: 2026-11-05\n---\n\nไม่มีข่าว AI ใหม่ที่ผ่านเกณฑ์ในวันนี้\nสาเหตุ: x\n\n" + FOOTER + "\n"
m = build_messages(empty)
assert len(m) == 1 and "ไม่มีข่าว" in m[0] and m[0].endswith("09:00 น."), m

long = article(1).replace("ข่าว 1", "ก" * 6000)
assert len(build_messages(long)[0]) == 5000
print("ok")
