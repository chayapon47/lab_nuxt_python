# ===== lab03.py : Lab 03 - JSON (กรองโพสต์ตาม page_id และนับต่อ Page) =====

import requests
from collections import Counter
# Counter = มากับ Python (collections) ใช้นับจำนวนสมาชิกที่ซ้ำกัน ไม่ต้องติดตั้งเพิ่ม

url = "http://localhost:3000/data/social_posts.json"
r = requests.get(url)
# ดึงไฟล์ JSON (static file ใน public/data) ด้วย GET

print("Request :", r.request.url)
print("Status  :", r.status_code)
# เก็บ URL และ HTTP status เป็นหลักฐานลงรายงาน

posts = r.json()
# ไฟล์เป็น list ตรงๆ จึงใช้ได้เลย
print("จำนวนโพสต์ทั้งหมด:", len(posts))

# --- นับโพสต์ของแต่ละ Page ---
counts = Counter(p["page_id"] for p in posts)
# generator: ดึง page_id ของทุกโพสต์ แล้ว Counter นับให้ ได้ผลเป็น {page_id: จำนวน}
print("\n=== จำนวนโพสต์ต่อ Page ===")
for page_id, n in sorted(counts.items()):
    print(page_id, ":", n, "โพสต์")

# --- กรองโพสต์ตาม page_id ---
page_ids = sorted(counts)
# หา page_id ที่มีอยู่จริงจากข้อมูล (ไม่เดาชื่อเอง)

for pid in page_ids:
    filtered = [p for p in posts if p["page_id"] == pid]
    # list comprehension: เก็บเฉพาะโพสต์ที่ page_id ตรงกับ pid (สร้างลิสต์ใหม่ ไม่แก้ต้นฉบับ)
    print(f"\n--- โพสต์ของ {pid} ({len(filtered)} โพสต์) ---")
    for p in filtered[:3]:
        print(p["id"], "|", p["created_time"][:10], "|", p["message"])
    # แสดงแค่ 3 โพสต์แรกของแต่ละ Page เพื่อให้ผลลัพธ์สั้นพอแคปได้

# --- ตรวจผลรวม ---
print("\nผลรวมทุก Page =", sum(counts.values()), "| โพสต์ทั้งหมด =", len(posts))
# ต้องเท่ากัน ถ้าไม่เท่าแปลว่ามีโพสต์ที่ไม่มี page_id

# --- edge case: page_id ที่ไม่มีอยู่จริง ---
none_found = [p for p in posts if p["page_id"] == "page_999"]
print("\n--- ทดสอบ page_id = page_999 ---")
print("จำนวนโพสต์ที่พบ:", len(none_found))
# กรองแล้วได้ list ว่าง (ไม่ error) เพราะไม่มี page นี้

try:
    print(posts[0]["page"])
except KeyError as e:
    print("เรียก key ที่ไม่มี: KeyError", e)
# ใช้ key ผิด ("page" แทน "page_id") จะเกิด KeyError ตัวอย่าง error ที่อธิบายได้

# --- error 404: path ที่ไม่มีอยู่ ---
r404 = requests.get("http://localhost:3000/data/social_postsxxx.json")
print("\n--- ทดสอบ path ที่ไม่มี ---")
print("Request :", r404.request.url)
print("Status  :", r404.status_code)