# ===== lab07.py : Lab 07 - SQLite (POST เพิ่มนักศึกษา: 201 / 409 / 422) =====

import requests

BASE = "http://localhost:3000"
URL = BASE + "/api/storage/sqlite/students"
# POST = ส่งข้อมูลไปสร้าง record ใหม่ (ต่างจาก GET ที่อ่านอย่างเดียว)

new_student = {
    "student_id": 2001,
    "name": "Intern Demo",
    "faculty": "IT",
    "year": 2,
    "gpa": 3.2,
    "active": True,
    "skills": ["Nuxt", "SQL"],
}
# ข้อมูลนักศึกษาที่จะ INSERT (True ใน Python จะถูกแปลงเป็น true ใน JSON ให้เอง)

def show(title, resp):
    print(f"\n--- {title} ---")
    print("Request :", resp.request.method, resp.request.url)
    body = resp.request.body
    print("Body    :", body.decode() if isinstance(body, bytes) else body)
    print("Status  :", resp.status_code)
    print("Response:", resp.text[:300])
# ฟังก์ชันช่วยพิมพ์ request / status / response ให้ครบ ใช้ซ้ำทุกกรณีทดสอบ

# --- 1) ก่อน INSERT: ดูว่า 2001 มีอยู่แล้วหรือไม่ ---
before = requests.get(URL).json()
ids_before = [s["student_id"] for s in before["data"]]
print("จำนวนนักศึกษาใน SQLite ก่อน INSERT:", before["count"])
print("มี 2001 อยู่แล้วไหม:", 2001 in ids_before)

# --- 2) INSERT ปกติ (คาดว่า 201 ถ้าเป็นครั้งแรก, 409 ถ้ารันซ้ำ) ---
r1 = requests.post(URL, json=new_student)
# json=... = requests แปลง dict เป็น JSON และใส่ Content-Type ให้อัตโนมัติ
show("INSERT 2001 ครั้งที่ 1", r1)

# --- 3) INSERT ซ้ำ (คาดว่า 409 Conflict เพราะ student_id ซ้ำ) ---
r2 = requests.post(URL, json=new_student)
show("INSERT 2001 ซ้ำ (duplicate)", r2)

# --- 4) GPA = 5 (คาดว่า 422 เพราะ GPA เกินช่วง) ---
bad_gpa = {**new_student, "student_id": 2002, "gpa": 5}
r3 = requests.post(URL, json=bad_gpa)
show("GPA = 5 (เกินช่วง)", r3)
# {**new_student, ...} = คัดลอก dict แล้วเปลี่ยนบาง key ต้นฉบับไม่ถูกแก้

# --- 5) ข้อมูลไม่ครบ (ไม่มี name) ---
missing = {"student_id": 2003, "faculty": "IT", "year": 2, "gpa": 3.0}
r4 = requests.post(URL, json=missing)
show("ไม่ส่ง name", r4)

# --- 6) ตรวจหลัง INSERT ว่า 2001 อยู่ในฐานข้อมูลจริง ---
after = requests.get(URL).json()
ids_after = [s["student_id"] for s in after["data"]]
print("\n=== ตรวจหลัง INSERT ===")
print("จำนวนนักศึกษาใน SQLite หลัง INSERT:", after["count"])
print("มี 2001 ไหม:", 2001 in ids_after)
print("มี 2002 ไหม (ต้องไม่มี เพราะ GPA=5 ถูกปฏิเสธ):", 2002 in ids_after)
print("มี 2003 ไหม (ต้องไม่มี เพราะข้อมูลไม่ครบ):", 2003 in ids_after)

# --- 7) เทียบกับ JSON: JSON เป็น read-only จึงต้องไม่มี 2001 ---
json_ids = [s["student_id"] for s in requests.get(BASE + "/api/storage/json/students").json()["data"]]
print("\nJSON มี 2001 ไหม (ต้องไม่มี เพราะ JSON read-only):", 2001 in json_ids)