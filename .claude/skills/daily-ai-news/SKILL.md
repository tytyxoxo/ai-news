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
3. กำหนด OUTPUT_FILE = articles/{YYYY-MM-DD}-brief.md

## ขั้นตอนที่ 1 — ค้นหาข่าว

ใช้ WebSearch ค้นหาด้วย query เหล่านี้

- "AI news today"
- "artificial intelligence latest 2026"
- "LLM machine learning news today"

เลือกข่าวที่น่าสนใจ 5 ข่าว จากผลการค้นหา
จากนั้นใช้ WebFetch ดึงเนื้อหาจาก URL ที่ได้จากผลการค้นหาเท่านั้น
ห้าม WebFetch ตรงจาก domain โดยไม่ผ่าน WebSearch ก่อน

## แหล่งข้อมูลที่แนะนำ

ค้นหาจากแหล่งเหล่านี้ก่อนเป็นอันดับแรก

- techcrunch.com
- theverge.com
- huggingface.co/blog
- openai.com/news
- anthropic.com/news
- blogs.microsoft.com
- blog.google
- venturebeat.com

ถ้าหาข่าวจากแหล่งข้างต้นได้ไม่ครบ 5 ข่าว จึงค่อยค้นหาจากแหล่งอื่นเพิ่มเติม

## ขั้นตอนที่ 2 — เขียนสรุปภาษาไทย

เขียนในสไตล์นักวิเคราะห์ด้าน AI ที่อธิบายให้คนทั่วไปเข้าใจได้
แต่ละข่าวให้เขียนเป็นเรียงความ 1 ย่อหน้า ความยาวประมาณ 80-120 คำ
โดยครอบคลุม

- ที่มาและบริบทของข่าว
- ความสำคัญและผลกระทบสั้นๆ

ห้ามเขียนแบบ bullet point — ให้เป็นย่อหน้าต่อเนื่องเท่านั้น

## ขั้นตอนที่ 3 — รูปแบบไฟล์ GitHub

ใช้รูปแบบ Markdown นี้เท่านั้น

---

## date: {YYYY-MM-DD}

## 1. {หัวข้อข่าว}

{เรียงความวิเคราะห์ 80-120 คำ}

ที่มา: {ชื่อเว็บ}

---

## 2. {หัวข้อข่าว}

{เรียงความวิเคราะห์ 80-120 คำ}

ที่มา: {ชื่อเว็บ}

---

_สร้างโดย Claude Code Routine เวลา 07:00 น._

## ขั้นตอนที่ 4 — บันทึกขึ้น GitHub และส่ง LINE

ใช้ GitHub connector บันทึกไฟล์ Markdown ขึ้น articles/
ข้อความที่ส่งไป LINE ใช้รูปแบบ plain text ที่มีเนื้อหาครบถ้วน
ไม่ต้องใส่ลิงก์ "อ่านเพิ่มเติม" ท้ายข้อความ

## ข้อห้าม

- ห้ามแต่งลิงก์ขึ้นมาเอง — ใช้เฉพาะ URL จาก WebSearch เท่านั้น
- ห้าม WebFetch ตรงจาก domain ที่ไม่ได้มาจาก WebSearch
- ถ้าหาข่าวได้น้อยกว่า 3 ข่าว ให้ commit สิ่งที่มีพร้อมหมายเหตุ
- ห้ามใช้ Bash หรือ git CLI — ใช้ GitHub connector เท่านั้น
- ใช้ timezone Asia/Bangkok เสมอ

## ข้อสำคัญ

- ให้ commit ตรงลงที่ branch: main เสมอ
- ห้ามสร้าง branch ใหม่

## ข้อจำกัด LINE

ข้อความทั้งหมดที่ส่งไป LINE ต้องไม่เกิน 4,500 ตัวอักษร
ถ้าเกินให้ลดความยาวบทความแต่ละข่าวลงให้พอดี
