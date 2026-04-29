---
name: daily-ai-news
description: ค้นหาและสรุปข่าว AI ประจำวัน 5 ข่าว เป็นภาษาไทย แล้วบันทึกขึ้น GitHub
---

# skill: daily-ai-news

## เครื่องมือที่ใช้ได้

WebSearch, WebFetch, GitHub connector (create_or_update_file)

## ขั้นตอนที่ 0 — เตรียมการ

1. ตรวจสอบว่า GitHub connector เชื่อมต่ออยู่ — ถ้าไม่มีให้หยุดและแจ้งเหตุผล
2. กำหนดวันที่ปัจจุบันตาม timezone Asia/Bangkok
3. ใช้ GitHub connector อ่านไฟล์ล่าสุดใน articles/ เพื่อดึง URL และหัวข้อที่เคยรายงานไปแล้ว (YESTERDAYS_URLS)
4. กำหนด OUTPUT_FILE = articles/{YYYY-MM-DD}-brief.md

## ขั้นตอนที่ 1 — ค้นหาข่าว

ใช้ WebSearch ค้นหาด้วย query เหล่านี้
- "AI news today"
- "artificial intelligence latest 2026"
- "LLM machine learning news today"

## แหล่งข้อมูล

**Tier 1A** — สื่อกลาง เชื่อถือสูงสุด เลือกก่อนเสมอ
- techcrunch.com
- theverge.com
- venturebeat.com
- huggingface.co/blog

**Tier 1B** — Official blog ข้อมูลตรงจากบริษัท แต่เป็น PR
- openai.com/news
- anthropic.com/news
- blogs.microsoft.com
- blog.google

**Tier 2** — ใช้เมื่อ Tier 1A และ 1B ไม่พอ
- blognone.com
- beartai.com
- thaipbs.or.th
- medium.com

### ลำดับการเลือก
1. Tier 1A ก่อนเสมอ
2. ถ้า Tier 1A ไม่พอ → เพิ่ม Tier 1B
3. ถ้ายังไม่พอ → เพิ่ม Tier 2
4. Prefer primary announcements over commentary ทุก Tier

## เกณฑ์คัดเลือกข่าว

กรองข่าวด้วย 2 เงื่อนไขนี้เท่านั้น
1. **24h filter** — ต้องเผยแพร่ภายใน 24 ชั่วโมงที่ผ่านมาเท่านั้น
2. **Dedup filter** — URL และหัวข้อต้องไม่ซ้ำกับ YESTERDAYS_URLS

เลือกข่าวที่ผ่านทั้ง 2 เงื่อนไข สูงสุด 5 ข่าว โดย
- มีแหล่งข่าวภาษาไทยอย่างน้อย 1 ข่าว (ถ้ามี)
- มีแหล่งข่าวต่างประเทศอย่างน้อย 3 ข่าว

**ห้ามผ่อนเกณฑ์เพื่อให้ครบ 5 ข่าว** — ถ้าผ่านแค่ 3 ก็ส่ง 3

## กรณีไม่มีข่าวผ่านเกณฑ์

ถ้าไม่มีข่าวผ่านเลย ให้ commit ไฟล์ stub แทน

---
date: {YYYY-MM-DD}
---

ไม่มีข่าว AI ใหม่ในวันนี้
สาเหตุ: {ระบุว่ามาจาก 24h filter / dedup filter / หรือทั้งคู่}

_สร้างโดย Claude Code Routine เวลา 09:00 น._

## ขั้นตอนที่ 2 — เรียงลำดับและเขียนสรุปภาษาไทย

ก่อนเขียนให้เรียงลำดับข่าวจากสำคัญมากไปน้อย โดยพิจารณาจาก
- ผลกระทบต่อวงการ AI ในภาพรวม
- ความใหม่และความน่าสนใจของเทคโนโลยี
- ผลกระทบต่อ developer และผู้ใช้ทั่วไป

เขียนในสไตล์นักวิเคราะห์ด้าน AI ที่อธิบายให้คนทั่วไปเข้าใจได้
แต่ละข่าวให้เขียนเป็นเรียงความ 1 ย่อหน้า ความยาวประมาณ 80-120 คำ
โดยครอบคลุม
- ที่มาและบริบทของข่าว
- ความสำคัญและสิ่งที่น่าสนใจ
- ผลกระทบหรือแนวโน้มที่อาจเกิดขึ้นในอนาคต

ห้ามเขียนแบบ bullet point — ให้เป็นย่อหน้าต่อเนื่องเท่านั้น

## ขั้นตอนที่ 3 — รูปแบบไฟล์ GitHub

ใช้รูปแบบ Markdown นี้เท่านั้น

---
date: {YYYY-MM-DD}
---

## 1. {หัวข้อข่าว}

{เรียงความวิเคราะห์ 80-120 คำ}

ที่มา: {ชื่อเว็บ}

---

## 2. {หัวข้อข่าว}

{เรียงความวิเคราะห์ 80-120 คำ}

ที่มา: {ชื่อเว็บ}

---

_สร้างโดย Claude Code Routine เวลา 09:00 น._

## ขั้นตอนที่ 4 — บันทึกขึ้น GitHub

ใช้ GitHub connector บันทึกไฟล์ Markdown ขึ้น articles/
ไม่ต้องใส่ลิงก์ "อ่านเพิ่มเติม" ท้ายข้อความ

## ข้อห้าม

- ห้ามแต่งลิงก์ขึ้นมาเอง — ใช้เฉพาะ URL จาก WebSearch เท่านั้น
- ห้าม WebFetch ตรงจาก domain ที่ไม่ได้มาจาก WebSearch
- ห้ามใช้ Bash หรือ git CLI — ใช้ GitHub connector เท่านั้น
- ใช้ timezone Asia/Bangkok เสมอ

## ข้อสำคัญ

- ให้ commit ตรงลงที่ branch: main เสมอ
- ห้ามสร้าง branch ใหม่

## ข้อจำกัด LINE

ข้อความทั้งหมดที่ส่งไป LINE ต้องไม่เกิน 4,500 ตัวอักษร
ถ้าเกินให้ลดความยาวบทความแต่ละข่าวลงให้พอดี