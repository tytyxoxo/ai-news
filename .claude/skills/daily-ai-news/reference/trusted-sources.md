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
- Beartai — https://www.beartai.com/
- The Standard Tech — https://thestandard.co/category/news/tech/
- Thairath Tech — https://www.thairath.co.th/news/tech
- Prachachat ICT — https://www.prachachat.net/ict
- NECTEC — https://www.nectec.or.th/news/

## หมายเหตุ

- Official blog มีอคติเชิง PR — สรุปสิ่งที่เขารายงาน ไม่ใช่สิ่งที่เป็นจริงในโลก
- Prefer primary announcement เหนือบทวิเคราะห์ทุกกรณี

## โดเมนที่ WebFetch เข้าไม่ได้ (บล็อก bot)

โดเมนต่อไปนี้ปฏิเสธการเข้าถึงของ WebFetch (403 หรือ block) — ห้ามเสีย call พยายามยืนยัน published date ด้วย WebFetch กับโดเมนเหล่านี้ ให้ใช้วันที่ที่ WebSearch ระบุไว้ชัดเจนแทนได้ (ต้องเป็นวันที่ตัวเลขจริง ไม่ใช่คำกว้างๆ เช่น "today"/"recently") ถ้า WebSearch ก็ไม่ระบุวันที่ชัดเจน ให้ตัดข่าวนั้นทิ้ง:

- OpenAI (openai.com)
- Reuters (reuters.com)
- Bloomberg (bloomberg.com)
- The Verge (theverge.com)
- Blognone (blognone.com)
- Ars Technica (arstechnica.com)
- Wired (wired.com)
- VentureBeat (venturebeat.com)

MIT Technology Review (technologyreview.com) โหลดได้แต่เป็นหน้า JS ว่างเปล่า ไม่มีบทความให้อ่าน — ถือว่าใช้ไม่ได้เช่นกันจนกว่าจะเจอวิธีอื่น
