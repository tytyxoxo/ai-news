# trusted-sources.md

แหล่งข่าวที่อนุญาตให้อ้างอิงใน daily-ai-news skill เท่านั้น
ห้ามใช้แหล่งที่ไม่อยู่ในรายการนี้ แม้จะดูน่าเชื่อถือ

## ลำดับการเลือก

1. Official blog / primary announcement ก่อนเสมอ
2. ถ้ามีข่าวเดียวกันใน official blog และสื่อ — เลือก official blog
3. ถ้าไม่มี official blog — เลือก Tier 1 ก่อน Tier 2

## ต่างประเทศ — Official / Primary

- OpenAI — https://openai.com/news
- Anthropic — https://www.anthropic.com/news
- Google DeepMind — https://deepmind.google/discover/blog/
- Meta AI — https://ai.meta.com/blog/
- Microsoft Research — https://www.microsoft.com/en-us/research/blog/
- NVIDIA Blog — https://blogs.nvidia.com/
- arXiv (cs.AI / cs.LG / cs.CL) — https://arxiv.org/list/cs.AI/recent

หมายเหตุ: arXiv เป็น preprint ยังไม่ผ่าน peer-review — ถ้าใช้ ให้ระบุชัดเจนในบทความ

## ต่างประเทศ — Tier 1

- TechCrunch — https://techcrunch.com/category/artificial-intelligence/
- The Verge — https://www.theverge.com/ai-artificial-intelligence
- Ars Technica — https://arstechnica.com/ai/
- MIT Technology Review — https://www.technologyreview.com/topic/artificial-intelligence/
- Wired — https://www.wired.com/tag/artificial-intelligence/
- VentureBeat — https://venturebeat.com/ai/

## ต่างประเทศ — Tier 2 (ใช้เมื่อ Tier 1 ไม่พอ)

- Reuters Technology — https://www.reuters.com/technology/
- Bloomberg Technology — https://www.bloomberg.com/technology
- Hugging Face Blog — https://huggingface.co/blog

## ไทย

- Blognone — https://www.blognone.com/
- The Standard Tech — https://thestandard.co/category/news/tech/
- Techsauce — https://techsauce.co/
- Brand Inside — https://brandinside.asia/
- TechHub — https://www.techhub.in.th/
- Prachachat ICT — https://www.prachachat.net/ict
- NECTEC — https://www.nectec.or.th/news/

## หมายเหตุ

- Official blog มีอคติเชิง PR — สรุปสิ่งที่เขารายงาน ไม่ใช่สิ่งที่เป็นจริงในโลก
- Prefer primary announcement เหนือบทวิเคราะห์ทุกกรณี

## Feed ที่ดึงจริง

รายการ RSS ที่ GitHub Actions ดึงจริงอยู่ใน `FEEDS` ของ `scripts/fetch_feeds.py` — ถ้าเพิ่ม/ลบแหล่งในไฟล์นี้ ต้องแก้ที่นั่นด้วย

แหล่งที่ยังไม่มีข่าวเข้า candidates (ไม่มี RSS หรือบล็อก bot): Anthropic, Meta AI, VentureBeat (429), Reuters (401) — ข่าวจากค่ายเหล่านี้มักมาทาง TechCrunch / The Verge / Bloomberg อยู่แล้ว
