# ai-news

สรุปข่าว AI ประจำวันเป็นภาษาไทย ส่งตรงถึง LINE อัตโนมัติทุกวัน

## การทำงาน

1. **GitHub Actions** (`fetch-feeds.yml`, ทุกชั่วโมง) ดึง RSS จากแหล่งที่เชื่อถือได้ เช่น TechCrunch, The Verge, Ars Technica ด้วย `scripts/fetch_feeds.py` แล้ว force-push เป็น `feeds/candidates.json` บน branch `feeds` (commit เดียวเสมอ ไม่สะสมใน history; cloud session ของ routine เข้าเว็บข่าวไม่ได้ จึงต้องดึงฝั่ง Actions)
2. **Claude Code Skill** (`daily-ai-news`, 09:00 น.) อ่าน `candidates.json` คัด 5 ข่าวใน 36 ชม. ที่ยังไม่เคยลง สรุปเป็นภาษาไทย แล้วบันทึกเป็น `articles/YYYY-MM-DD-brief.md` ผ่าน GitHub connector
3. **GitHub Actions** (`line-notify.yml`) ตรวจจับเมื่อมีไฟล์ใหม่ใน `articles/` แล้วส่งเข้า LINE ด้วย `scripts/line_notify.py` — 1 ข่าวต่อ 1 บับเบิล (สูงสุด 5 บับเบิล นับโควตาเป็น 1 ข้อความ)
4. **Watchdog** (`line-watchdog.yml`, 10:13 น.) ถ้ายังไม่มีไฟล์ข่าววันนี้ ส่ง LINE เตือนว่า routine ไม่ทำงาน
5. **เก็บย้อนหลัง 30 วัน** — `fetch-feeds.yml` ลบ `articles/` ที่เก่ากว่า 30 วันทุกวัน (ไฟล์ที่ลบยังอยู่ใน git history แต่ main โตแค่ราว 5KB/วัน)

## โครงสร้างไฟล์

```
articles/          # ไฟล์สรุปข่าวรายวัน
scripts/           # fetch_feeds.py, line_notify.py + test_*.py (python3 scripts/test_*.py)
.claude/skills/    # Claude Code skill สำหรับสร้างข่าว
.github/workflows/ # GitHub Actions สำหรับส่ง LINE
```

## ตั้งค่า Secrets

ใน GitHub repository ให้เพิ่ม secrets ดังนี้:

| Secret | คำอธิบาย |
|--------|----------|
| `LINE_CHANNEL_ACCESS_TOKEN` | Channel Access Token จาก LINE Developers |
| `LINE_TO` | User ID หรือ Group ID ปลายทาง |

## เครดิต

ได้รับแรงบันดาลใจและคอนเซ็ปมาจาก [thannob/dailyainews](https://github.com/thannob/dailyainews)
