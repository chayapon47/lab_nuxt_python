# ===== lab05.py : Lab 05 - SQLite (SELECT + min_gpa และเทียบกับ JSON) =====

import requests

BASE = "http://localhost:3000"

# --- 1) ดึงจาก SQLite (server กรองด้วย SQL WHERE gpa >= ?) ---
r_sql = requests.get(BASE + "/api/storage/sqlite/students", params={"min_gpa": 3.5})
print("Request :", r_sql.request.url)
print("Status  :", r_sql.status_code)
body_sql = r_sql.json()
print("source  :", body_sql["source"], "| count:", body_sql["count"])
sql_rows = body_sql["data"]

# --- 2) ดึงจาก JSON ทั้งหมด แล้วกรองเองด้วย Python ---
r_json = requests.get(BASE + "/api/storage/json/students")
print("\nRequest :", r_json.request.url)
print("Status  :", r_json.status_code)
json_all = r_json.json()["data"]
json_rows = [s for s in json_all if s["gpa"] >= 3.5]
# list comprehension: กรอง gpa >= 3.5 ด้วยโค้ดเอง (JSON ไม่มี SQL engine)
print("JSON ทั้งหมด:", len(json_all), "คน | gpa >= 3.5:", len(json_rows), "คน")

# --- 3) เทียบผล ---
sql_ids = sorted(s["student_id"] for s in sql_rows)
json_ids = sorted(s["student_id"] for s in json_rows)
print("\nจำนวนเท่ากันไหม :", len(sql_ids) == len(json_ids))
print("student_id ตรงกันไหม:", sql_ids == json_ids)
print("student_id (SQLite):", sql_ids)

# --- 4) เช็กว่าทุกคนที่ได้จาก SQLite มี gpa >= 3.5 จริง ---
print("gpa ต่ำสุดที่ SQLite ส่งมา:", min(s["gpa"] for s in sql_rows))

# --- edge case 1: min_gpa สูงเกินไป ---
r_hi = requests.get(BASE + "/api/storage/sqlite/students", params={"min_gpa": 4.5})
print("\n--- min_gpa=4.5 ---")
print("Status:", r_hi.status_code, "| count:", r_hi.json().get("count"))

# --- edge case 2: min_gpa ไม่ใช่ตัวเลข ---
r_bad = requests.get(BASE + "/api/storage/sqlite/students", params={"min_gpa": "abc"})
print("\n--- min_gpa=abc ---")
print("Status:", r_bad.status_code)
print("Response:", r_bad.text[:200])

# --- edge case 3: SQL injection (พิสูจน์ว่า parameterized query ปลอดภัย) ---
r_inj = requests.get(BASE + "/api/storage/sqlite/students",
                     params={"min_gpa": "0 OR 1=1"})
print("\n--- min_gpa='0 OR 1=1' ---")
print("Status:", r_inj.status_code)
print("Response:", r_inj.text[:200])

# --- edge case 4: path ที่ไม่มี ---
r404 = requests.get(BASE + "/api/storage/sqlite/studentsxxx")
print("\n--- path ที่ไม่มี ---")
print("Status:", r404.status_code)