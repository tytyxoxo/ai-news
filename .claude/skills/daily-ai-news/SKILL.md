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

## ขั้นตอนที่ 2 — เขียนสรุปภาษาไทย

เขียนทุกอย่างเป็นภาษาไทย สำหรับแต่ละข่าวให้มี

- หัวข้อข่าวภาษาไทย
- สรุปเนื้อหา 3-5 ประโยค เข้าใจง่าย ไม่ใช้ศัพท์เทคนิคเกินไป
- แหล่งอ้างอิงพร้อมลิงก์จริงจาก WebSearch เท่านั้น

## ขั้นตอนที่ 3 — รูปแบบไฟล์

ใช้รูปแบบนี้เท่านั้น

---

## date: {YYYY-MM-DD}

# สรุปข่าว AI ประจำวัน {DD/MM/YYYY}

## 1. {หัวข้อข่าว}

{สรุปเนื้อหา}
**แหล่งอ้างอิง:** [{ชื่อเว็บ}]({url})

## 2. ...

---

_สร้างโดย Claude Code Routine เวลา 07:00 น._

## ขั้นตอนที่ 4 — บันทึกขึ้น GitHub

ใช้ GitHub connector สร้างหรืออัปเดตไฟล์

- path: articles/{YYYY-MM-DD}-brief.md
- commit message: brief: {หัวข้อหลัก} {YYYY-MM-DD}
- branch: main

## ข้อห้าม

- ห้ามแต่งลิงก์ขึ้นมาเอง — ใช้เฉพาะ URL จาก WebSearch เท่านั้น
- ห้าม WebFetch ตรงจาก domain ที่ไม่ได้มาจาก WebSearch
- ถ้าหาข่าวได้น้อยกว่า 3 ข่าว ให้ commit สิ่งที่มีพร้อมหมายเหตุ
- ห้ามใช้ Bash หรือ git CLI — ใช้ GitHub connector เท่านั้น
- ใช้ timezone Asia/Bangkok เสมอ

## ข้อสำคัญ

- ให้ commit ตรงลงที่ branch: main เสมอ
- ห้ามสร้าง branch ใหม่
