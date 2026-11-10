# ===== lab11.py : Lab 11 - POST MongoDB, duplicate key, เปรียบเทียบ error MongoDB/SQLite =====
import requests
from pymongo import MongoClient

BASE = "http://localhost:3000/api/storage"
students = MongoClient("mongodb://127.0.0.1:27017")["nuxt_intern"]["students"]
students.delete_one({"student_id": 3001})   # ลบของรอบก่อน ให้รันซ้ำได้ผลเดิม

new = {"student_id": 3001, "name": "Mongo Demo", "faculty": "IT", "year": 2, "gpa": 3.2, "active": True, "skills": ["Nuxt"]}
dup = {**new, "student_id": 1001}   # id ที่มีอยู่แล้ว
bad = {**dup, "gpa": 5}             # gpa เกิน 4

def post(store, label, body):
    r = requests.post(f"{BASE}/{store}/students", json=body, timeout=10)
    res = r.json()
    print(f"[{store}] {label} -> {r.status_code} {res.get('statusMessage', 'Created')}")
    if "data" in res:
        print("    data:", res["data"])   # 201 = ข้อมูลที่เพิ่ม, 422 ของ SQLite = field ที่ผิด

# 1) เพิ่ม document และทดสอบ duplicate key
post("mongo", "เพิ่ม 3001", new)
post("mongo", "3001 ซ้ำ", new)

# 2) เปรียบเทียบ error MongoDB / SQLite
for store in ("mongo", "sqlite"):
    post(store, "1001 ซ้ำ", dup)
    post(store, "gpa = 5", bad)

print("students ใน MongoDB:", students.count_documents({}))
