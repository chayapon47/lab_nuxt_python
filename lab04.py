import requests
from collections import defaultdict
# defaultdict = มากับ Python (collections) dict ที่สร้างค่าเริ่มต้นให้เองเมื่อใช้ key ใหม่

BASE = "http://localhost:3000"

r_enr = requests.get(BASE + "/data/enrollments.json")
r_crs = requests.get(BASE + "/data/courses.json")
print("Request 1:", r_enr.request.url, "| Status:", r_enr.status_code)
print("Request 2:", r_crs.request.url, "| Status:", r_crs.status_code)
# เก็บ URL และ HTTP status ของทั้งสอง request เป็นหลักฐานลงรายงาน

enrollments = r_enr.json()
courses = r_crs.json()
# ทั้งสองไฟล์เป็น list ตรงๆ
print("จำนวน enrollments:", len(enrollments))

course_name = {c["course_id"]: c["course_name"] for c in courses}
# lookup dict: course_id -> ชื่อวิชา (ใช้แสดงผลคู่กับค่าเฉลี่ย)

# --- จัดกลุ่ม score ตาม course_id ---
scores_by_course = defaultdict(list)
for e in enrollments:
    scores_by_course[e["course_id"]].append(e["score"])
# ได้ {course_id: [score, score, ...]} โดยไม่แก้ข้อมูลต้นฉบับ

# --- คำนวณค่าเฉลี่ยต่อวิชา ---
print("\n=== ค่าเฉลี่ย score ของแต่ละรายวิชา ===")
total_check = 0
for cid in sorted(scores_by_course):
    s = scores_by_course[cid]
    avg = sum(s) / len(s)
    # ค่าเฉลี่ย = ผลรวม / จำนวน
    total_check += len(s)
    print(f'{cid} | {course_name.get(cid, "(ไม่พบวิชา)"):<25} | {len(s):>2} คน | เฉลี่ย {avg:.2f}')

print("\nผลรวมจำนวน enrollment ทุกวิชา =", total_check, "| ทั้งหมด =", len(enrollments))
# ต้องเท่ากัน เพื่อยืนยันว่าไม่มีรายการหลุด

# --- ตรวจ course_id ใน enrollments ที่ไม่มีใน courses.json ---
orphans = [cid for cid in scores_by_course if cid not in course_name]
print("course_id ที่ไม่มีใน courses.json:", orphans)

# --- edge case 1: วิชาที่ไม่มีใครลงทะเบียน ---
s = scores_by_course.get("CS999", [])
print("\n--- ทดสอบ course_id = CS999 ---")
print("จำนวน score:", len(s))
try:
    print("เฉลี่ย:", sum(s) / len(s))
except ZeroDivisionError as e:
    print("หารด้วยศูนย์: ZeroDivisionError:", e)
# list ว่างแล้วหารด้วย len = 0 จะเกิด ZeroDivisionError

# --- edge case 2: key ผิด ---
try:
    print(enrollments[0]["grade"])
except KeyError as e:
    print("เรียก key ที่ไม่มี: KeyError", e)

# --- edge case 3: path ที่ไม่มี ---
r404 = requests.get(BASE + "/data/enrollmentsxxx.json")
print("\n--- ทดสอบ path ที่ไม่มี ---")
print("Request :", r404.request.url)
print("Status  :", r404.status_code)