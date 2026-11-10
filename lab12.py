# ===== lab12.py : Lab 12 - นักศึกษาคนเดียวกันจาก JSON / SQLite / MongoDB และตรวจ consistency =====
import requests

BASE = "http://localhost:3000/api/storage"
SID = 1001

# --- 1) ดึงจาก 3 แหล่ง ---
src = {}
for store in ("json", "sqlite", "mongo"):
    r = requests.get(f"{BASE}/{store}/students", timeout=10)
    body = r.json()
    src[store] = {s["student_id"]: s for s in body["data"]}   # ทำเป็น dict: student_id -> ข้อมูล
    print(f"GET /{store}/students -> {r.status_code} count {body['count']}")

# --- 2) นักศึกษาคนเดียวกันจาก 3 แหล่ง ---
print(f"\nstudent_id {SID}:")
for store in src:
    print(f"  {store}:", src[store].get(SID))
print("ตรงกันทั้ง 3 แหล่ง:", src["json"][SID] == src["sqlite"][SID] == src["mongo"][SID])

# --- 3) ตรวจ consistency: id ที่ไม่ครบ และเนื้อหาที่ต่างกัน ---
all_ids = set(src["json"]) | set(src["sqlite"]) | set(src["mongo"])
print("\nid ที่ไม่ได้อยู่ครบ 3 แหล่ง:")
for sid in sorted(all_ids):
    where = [store for store in src if sid in src[store]]
    if len(where) < 3:
        print(f"  {sid} มีเฉพาะใน {where}")
common = set(src["json"]) & set(src["sqlite"]) & set(src["mongo"])
diff = [sid for sid in common if not (src["json"][sid] == src["sqlite"][sid] == src["mongo"][sid])]
print(f"มีครบ 3 แหล่ง {len(common)} คน, เนื้อหาต่างกัน: {diff}")

# --- edge case: query ผิด ---
r = requests.get(f"{BASE}/sqlite/students", params={"min_gpa": "abc"}, timeout=10)
print(f"\nGET /sqlite/students?min_gpa=abc -> {r.status_code} {r.json().get('statusMessage')}")
