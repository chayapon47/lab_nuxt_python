# ===== lab08.py : Lab 08 - เปรียบเทียบ JSON กับ SQLite หลัง INSERT =====

import requests, json

BASE = "http://localhost:3000"

# --- 1) เรียก endpoint compare แล้วพิมพ์โครงสร้างดิบ ---
r = requests.get(BASE + "/api/storage/compare")
print("Request :", r.request.url)
print("Status  :", r.status_code)
print("Response:")
print(json.dumps(r.json(), ensure_ascii=False, indent=2)[:1500])
# พิมพ์ดิบก่อน เพราะยังไม่ทราบชื่อ key ของ compare

# --- 2) ดึง JSON และ SQLite มานับเองเพื่อตรวจ ---
json_rows = requests.get(BASE + "/api/storage/json/students").json()["data"]
sql_rows = requests.get(BASE + "/api/storage/sqlite/students").json()["data"]
# JSON = ไฟล์ read-only, SQLite = ฐานข้อมูลที่ POST เพิ่มได้

json_ids = {s["student_id"] for s in json_rows}
sql_ids = {s["student_id"] for s in sql_rows}
# set ของ student_id ใช้หาผลต่างได้ทันที

print("\n=== นับเอง ===")
print("JSON  :", len(json_rows), "คน")
print("SQLite:", len(sql_rows), "คน")
print("มีใน SQLite แต่ไม่มีใน JSON:", sorted(sql_ids - json_ids))
print("มีใน JSON แต่ไม่มีใน SQLite:", sorted(json_ids - sql_ids))
# ผลต่างของ set = หลักฐานว่าทำไม count ต่างกัน

# --- 3) เทียบเนื้อหาของ record ที่มีทั้งสองฝั่ง ---
j_by_id = {s["student_id"]: s for s in json_rows}
diff = [sid for sid in json_ids & sql_ids if j_by_id[sid] != next(x for x in sql_rows if x["student_id"] == sid)]
print("record ที่มีทั้งสองฝั่งแต่เนื้อหาต่างกัน:", diff)
# ว่าง = ข้อมูลชุดเดิมตรงกันทุกฟิลด์

# --- edge case 1: path ที่ไม่มี ---
r404 = requests.get(BASE + "/api/storage/comparexxx")
print("\n--- path ที่ไม่มี ---")
print("Status:", r404.status_code)

# --- edge case 2: ใช้ POST กับ endpoint ที่ GET อย่างเดียว ---
r405 = requests.post(BASE + "/api/storage/compare", json={})
print("\n--- POST ไปที่ /compare ---")
print("Status:", r405.status_code)