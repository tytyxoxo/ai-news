# ai-news

สรุปข่าว AI ประจำวันเป็นภาษาไทย ส่งตรงถึง LINE อัตโนมัติทุกวัน

## การทำงาน

1. **Claude Code Skill** (`daily-ai-news`) ค้นหาข่าว AI 5 ข่าวจากแหล่งที่เชื่อถือได้ เช่น TechCrunch, The Verge, Ars Technica และสรุปเป็นภาษาไทย
2. **บันทึกลง GitHub** เป็นไฟล์ `articles/YYYY-MM-DD-brief.md` ผ่าน GitHub connector
3. **GitHub Actions** (`line-notify.yml`) ตรวจจับเมื่อมีไฟล์ใหม่ใน `articles/` แล้วส่งข้อความแจ้งเตือนไปยัง LINE อัตโนมัติ

## โครงสร้างไฟล์

```
articles/          # ไฟล์สรุปข่าวรายวัน
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
