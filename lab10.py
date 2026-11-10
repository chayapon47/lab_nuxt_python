# ===== lab10.py : Lab 10 - อ่าน MongoDB ผ่าน API, filter faculty, _id vs student_id, projection =====

import json
import requests
from pymongo import MongoClient

BASE = "http://localhost:3000"
URL = BASE + "/api/storage/mongo/students"
# ต้องเปิด npm run dev และ docker compose up -d ไว้ก่อน


def show(label, r):
    body = r.json()
    print(f"\n--- {label} ---")
    print("Request :", r.request.method, r.request.url)
    print("Status  :", r.status_code)
    print("count   :", body.get("count"))
    return body
# ฟังก์ชันช่วยพิมพ์ request / status / count ให้ทุกกรณีหน้าตาเหมือนกัน


# --- 1) อ่าน document ทั้งหมด และ filter faculty ---
all_body = show("ทั้งหมด", requests.get(URL, timeout=10))
it_body = show("faculty=IT", requests.get(URL, params={"faculty": "IT"}, timeout=10))
print("ชื่อ:", [s["name"] for s in it_body["data"]])
print("ทุกคนเป็น IT:", all(s["faculty"] == "IT" for s in it_body["data"]))
# params= ให้ requests ต่อ ?faculty=IT ท้าย URL ให้เอง

print("\nResponse ตัวอย่าง (เอกสารแรกของ IT):")
print(json.dumps(it_body["data"][0], ensure_ascii=False, indent=2))
print("มี _id ใน response API ไหม:", "_id" in it_body["data"][0])
# False เพราะ endpoint ใช้ projection {_id: 0}


# --- 2) _id กับ student_id: ดูเอกสารจริงใน MongoDB ---
client = MongoClient("mongodb://127.0.0.1:27017", serverSelectionTimeoutMS=3000)
students = client["nuxt_intern"]["students"]

raw = students.find_one({"student_id": 1008})
print("\n=== เอกสารจริงใน MongoDB (ไม่มี projection) ===")
print("_id        :", raw["_id"], "| ชนิด:", type(raw["_id"]).__name__)
print("student_id :", raw["student_id"], "| ชนิด:", type(raw["student_id"]).__name__)
print("_id สร้างเมื่อ:", raw["_id"].generation_time)
# _id = ObjectId ที่ MongoDB สร้างให้ตอน seed (ฝังเวลาที่สร้างไว้ข้างใน)
# student_id = ตัวเลขจากไฟล์ JSON ของเรา


# --- 3) projection 2 แบบ ---
print("\n=== Projection ===")
print("ตัด _id ออก {_id: 0}             :", students.find_one({"student_id": 1008}, {"_id": 0}))
print("เลือกเอา {_id: 0, student_id, name}:", students.find_one({"student_id": 1008}, {"_id": 0, "student_id": 1, "name": 1}))
print("ไม่สั่ง _id {student_id, name}     :", students.find_one({"student_id": 1008}, {"student_id": 1, "name": 1}))
# แบบที่ 3: ถ้าไม่สั่ง _id: 0 MongoDB จะแถม _id มาเสมอ

client.close()


# --- edge case 1: คณะที่ไม่มี และตัวพิมพ์ผิด ---
show("faculty=Art (ไม่มีคณะนี้)", requests.get(URL, params={"faculty": "Art"}, timeout=10))
show("faculty=it (ตัวเล็ก)", requests.get(URL, params={"faculty": "it"}, timeout=10))
# 200 + count 0: resource มีอยู่ แค่ผลกรองว่าง และ MongoDB แยกตัวพิมพ์เล็กใหญ่

# --- edge case 2: ส่ง faculty ซ้ำ 2 ค่า ---
dup = show("faculty=IT&faculty=Science", requests.get(URL, params=[("faculty", "IT"), ("faculty", "Science")], timeout=10))
print("filter ถูกข้าม:", dup["count"] == all_body["count"])
# q.faculty กลายเป็น list -> typeof ไม่ใช่ string -> ไม่กรอง ได้ทั้ง 30 (ควรเป็น 400 ตามเกณฑ์ตรวจรับ)

# --- edge case 3: path ผิด ---
r404 = requests.get(BASE + "/api/storage/mongo/studentsxxx", timeout=10)
print("\n--- path ที่ไม่มี ---")
print("Status:", r404.status_code)
