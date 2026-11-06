# Decisions

## 2026-11-06 — fetch-feeds รันทุกชั่วโมง, routine กรอง 36 ชม. + dedup

- **ตัดสินใจ:** cron `17 * * * *` แทน `17 0 * * *`; routine ยอม candidates เก่าได้ถึง 12 ชม. และกรองข่าว 36 ชม. โดยกันซ้ำด้วย URL ใน articles 2 ไฟล์ล่าสุด
- **เหตุผล:** วันแรก (6 พ.ย.) cron 07:17 ไม่รันเลย ไม่มี branch `feeds` → routine ส่ง "ไม่มีข่าว"; watchdog ของ 5 พ.ย. ก็รันช้า 7 ชม. 45 นาที — GitHub cron เป็น best-effort จะผูกกับรอบเดียวก่อน 09:00 ไม่ได้
- **Trade-off:** รัน Actions ~24 ครั้ง/วัน (repo public ไม่เสียเงิน); branch `feeds` ยังเป็น commit เดียว
- **ทางเลือกที่ไม่เอา:** ให้ routine สั่ง workflow_dispatch เอง (ไม่แน่ใจว่า connector ทำได้), ตั้งหลาย cron ช่วงเช้า (ยังโดนข้ามทั้งชุดได้)

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
