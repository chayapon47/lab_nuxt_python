# ===== lab02.py : Lab 02 - JSON (จับคู่ courses กับ instructors) =====

import requests

BASE = "http://localhost:3000"
# BASE = ที่อยู่ server เก็บไว้ตัวแปรเดียว ไม่ต้องพิมพ์ซ้ำ

r_courses = requests.get(BASE + "/data/courses.json")
r_instr = requests.get(BASE + "/data/instructors.json")
# ดึงไฟล์ JSON 2 ไฟล์ (static file ใน public/data)

print("Request 1:", r_courses.request.url, "| Status:", r_courses.status_code)
print("Request 2:", r_instr.request.url, "| Status:", r_instr.status_code)
# เก็บ URL และ HTTP status ของทั้งสอง request เป็นหลักฐานลงรายงาน

courses = r_courses.json()
instructors = r_instr.json()
# ทั้งสองไฟล์เป็น list ตรงๆ จึงใช้ได้เลย

print("จำนวน courses:", len(courses))
print("จำนวน instructors:", len(instructors))

# --- สร้าง lookup dict: instructor_id -> instructor ---
instructor_by_id = {i["instructor_id"]: i for i in instructors}
# dict comprehension: ค้นผู้สอนจาก id ได้ทันที เร็วกว่าวนหาทีละคน
# สร้าง dict ใหม่แยกต่างหาก จึง "ไม่แก้ข้อมูลต้นทาง" ตามโจทย์

# --- จับคู่ (JOIN ด้วย Python) ---
print("\n=== รายวิชาพร้อมชื่อผู้สอน ===")
joined = []
for c in courses:
    inst = instructor_by_id.get(c["instructor_id"])
    # .get() = ถ้าไม่เจอ id จะได้ None ไม่ crash
    inst_name = inst["name"] if inst else "(ไม่พบผู้สอน)"
    joined.append({**c, "instructor_name": inst_name})
    # {**c, ...} = คัดลอก course เดิมแล้วเพิ่ม key ใหม่ ต้นฉบับไม่ถูกแก้
    print(f'{c["course_id"]} | {c["course_name"]:<22} | {c["instructor_id"]} | {inst_name}')

# --- ตรวจว่าไม่ได้แก้ข้อมูลต้นทาง ---
print("\ncourses[0] ต้นฉบับ มี instructor_name ไหม:", "instructor_name" in courses[0])
# ต้องได้ False เพราะเราเพิ่ม key ในสำเนา (joined) เท่านั้น

# --- edge case: instructor_id ที่ไม่มีอยู่จริง ---
print("\n--- ทดสอบ instructor_id = T999 ---")
print("ผลจับคู่ด้วย .get():", instructor_by_id.get("T999"))
# ได้ None เพราะไม่มี T999

try:
    instructor_by_id["T999"]
except KeyError as e:
    print("ผลจับคู่ด้วย [] : KeyError", e)
# ใช้ [] แล้วค้นไม่เจอ จะเกิด KeyError (ตัวอย่าง error ที่อธิบายได้)
# ----- กรณี error จริง: เรียก path ที่ไม่มีอยู่ -----
r3 = requests.get("http://localhost:3000/api/storage/json/studentsxxx")
print("\n--- ทดสอบ path ที่ไม่มี ---")
print("Status:", r3.status_code)
# path ผิด server หา endpoint ไม่เจอ จึงตอบ 404 (Not Found)