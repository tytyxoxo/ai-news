# Decisions

## 2026-11-05 — LINE แยกบับเบิลต่อข่าว, candidates อยู่ branch แยก, เก็บข่าว 30 วัน

- **ตัดสินใจ:** (1) `line_notify.py` ส่ง 1 ข่าว = 1 text bubble (สูงสุด 5) แทนข้อความเดียว 4,500 ตัวอักษร — ลบระบบงบตัวอักษรใน skill และ auto-trim ใน workflow (2) `candidates.json` force-push เป็น orphan commit เดียวบน branch `feeds` (3) ลบ `articles/` เก่ากว่า 30 วันทุกวัน (4) watchdog 10:13 น. เตือนทาง LINE ถ้าไม่มีไฟล์วันนี้ (5) feed ไทย: เพิ่ม Techsauce / Brand Inside / TechHub, ตัด Beartai (feed ค้าง 6 ต.ค.) / Thairath (ไม่มีข่าว AI ผ่าน)
- **เหตุผล:** LINE นับโควตาตามผู้รับ ไม่ใช่จำนวน message object ([pricing](https://developers.line.biz/en/docs/messaging-api/pricing/)) จึงแยกบับเบิลได้ฟรี และ LLM นับความยาวเองพลาดจน LINE fail หลายวัน; candidates ~140KB/วันถ้า commit ลง main จะสะสม ~50MB/ปี
- **Trade-off:** ไฟล์ที่ prune แล้วยังอยู่ใน git history ของ main (เล็ก ~5KB/วัน); ไม่ rewrite history เพราะต้อง force-push main ซึ่งชนกับ routine
- **ทางเลือกที่ไม่เอา:** Flex Message (JSON เยอะ ดูแลยาก), rewrite history main เป็นระยะ (เสี่ยงทับ commit ของ routine)

## 2026-11-05 — ดึงข่าวผ่าน RSS ใน GitHub Actions แทน WebSearch/WebFetch ใน routine

- **ตัดสินใจ:** `fetch-feeds.yml` (07:17 น.) รัน `scripts/fetch_feeds.py` ดึง RSS → `feeds/candidates.json`; routine อ่านไฟล์นี้ผ่าน GitHub connector อย่างเดียว
- **เหตุผล:** cloud session ของ routine โดน network allowlist บล็อก WebFetch ไปเว็บข่าว — 6 ใน 8 วัน (29 ต.ค.–5 พ.ย.) ออกมาว่า "ไม่มีข่าวผ่านเกณฑ์" ทั้งที่มีข่าว; Actions ออกเน็ตได้ปกติ และวันที่จาก feed แม่นกว่าให้ LLM อ่านจากหน้าเว็บ
- **Trade-off:** แหล่งที่ไม่มี RSS (Anthropic, Meta AI) หรือบล็อก bot (VentureBeat, Reuters) หายไป; feed ทั่วไปกรองด้วยคีย์เวิร์ด AI แบบหยาบ; ถ้า Actions cron ไม่รัน routine จะได้ไฟล์เก่า (กันด้วยเช็ก `generated_at` > 6 ชม.)
- **ทางเลือกที่ไม่เอา:** เพิ่มโดเมนใน allowlist ของ cloud environment (คุมเองไม่ได้ พังซ้ำแล้วหลายรอบ), ใช้วันที่จาก WebSearch snippet (ไม่มีวันที่ชัด + เนื้อหาไม่พอเขียนโดยไม่เดา)
