# ===== lab06.py : Lab 06 - SQLite (JOIN students/enrollments/courses) =====

import requests

BASE = "http://localhost:3000"

# --- 1) ดึงผล JOIN จาก SQLite (server ทำ JOIN ให้) ---
r = requests.get(BASE + "/api/storage/sqlite/enrollments", params={"student_id": 1001})
print("Request :", r.request.url)
print("Status  :", r.status_code)
body = r.json()
print("source  :", body["source"], "| count:", body["count"])
for row in body["data"]:
    print(row["enrollment_id"], "|", row["name"], "|", row["course_id"], "|", row["course_name"], "|", row["score"])
sql_rows = body["data"]

# --- 2) ทำ JOIN เองด้วย Python จากไฟล์ JSON เพื่อเทียบ ---
students = requests.get(BASE + "/api/storage/json/students").json()["data"]
enrollments = requests.get(BASE + "/data/enrollments.json").json()
courses = requests.get(BASE + "/data/courses.json").json()
# ดึงข้อมูล 3 ชุดที่ SQLite เก็บเป็น 3 ตาราง (students, enrollments, courses)

student_by_id = {s["student_id"]: s for s in students}
course_by_id = {c["course_id"]: c for c in courses}
# lookup dict แทนการ JOIN

py_rows = []
for e in enrollments:
    if e["student_id"] == 1001:
        s = student_by_id.get(e["student_id"])
        c = course_by_id.get(e["course_id"])
        if s and c:
            # เก็บเฉพาะแถวที่มีคู่ครบทั้งสองฝั่ง = พฤติกรรมเดียวกับ INNER JOIN
            py_rows.append((e["enrollment_id"], s["name"], e["course_id"], c["course_name"], e["score"]))

sql_tuples = [(x["enrollment_id"], x["name"], x["course_id"], x["course_name"], x["score"]) for x in sql_rows]
print("\nJOIN เองด้วย Python ได้", len(py_rows), "แถว")
print("ผลตรงกับ SQLite ไหม:", sorted(py_rows) == sorted(sql_tuples))

# --- edge case 1: student_id ที่ไม่มีอยู่จริง ---
r_none = requests.get(BASE + "/api/storage/sqlite/enrollments", params={"student_id": 9999})
print("\n--- student_id=9999 ---")
print("Status:", r_none.status_code)
print("Response:", r_none.text[:200])

# --- edge case 2: student_id ไม่ใช่ตัวเลข ---
r_bad = requests.get(BASE + "/api/storage/sqlite/enrollments", params={"student_id": "abc"})
print("\n--- student_id=abc ---")
print("Status:", r_bad.status_code)
print("Response:", r_bad.text[:200])

# --- edge case 3: ไม่ส่ง student_id ---
r_all = requests.get(BASE + "/api/storage/sqlite/enrollments")
print("\n--- ไม่ส่ง student_id ---")
print("Status:", r_all.status_code)
print("count:", r_all.json().get("count"))

# --- edge case 4: path ที่ไม่มี ---
r404 = requests.get(BASE + "/api/storage/sqlite/enrollmentsxxx")
print("\n--- path ที่ไม่มี ---")
print("Status:", r404.status_code)