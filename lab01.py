# ===== lab01.py : Lab 01 - JSON (อ่าน students และกรอง faculty) =====

import requests, json
# requests = ไลบรารีภายนอก (pip install requests) ใช้ยิง HTTP request ไปหา API
#            เลือกใช้เพราะอ่านง่าย โค้ดสั้น เป็นมาตรฐานที่คนใช้ดึงข้อมูลจาก API
# json     = มากับ Python อยู่แล้ว ใช้จัดรูป JSON ตอน print ให้อ่านง่าย

url = "http://localhost:3000/api/storage/json/students"
# url = ที่อยู่ endpoint ของ Lab 01
#       localhost:3000 = เครื่องตัวเอง พอร์ตที่ Nuxt รันอยู่ (npm run dev)

r = requests.get(url, params={"faculty": "Engineering"})
# requests.get = ส่ง GET request (ขอดึงข้อมูลอย่างเดียว ไม่แก้ข้อมูล)
# params       = query string จะถูกต่อเป็น ...students?faculty=Engineering ให้อัตโนมัติ
# r            = ตัวแปรเก็บคำตอบทั้งหมดที่ server ส่งกลับมา

print("Request :", r.request.url)
# r.request.url = URL เต็มที่ส่งไปจริง ใช้เป็นหลักฐาน "Request" ในรายงาน

print("Status  :", r.status_code)
# r.status_code = HTTP status ที่ server ตอบ (200 = สำเร็จ, 400 = request ผิด,
#                 404 = ไม่พบ, 409 = ข้อมูลซ้ำ, 422 = ข้อมูลไม่ผ่าน validation)

body = r.json()
# r.json() = แปลงข้อความ JSON ที่ได้รับ ให้เป็น dict ของ Python เพื่อใช้งานต่อได้

print("source  :", body["source"])
# source = บอกว่าข้อมูลมาจากแหล่งไหน (ในที่นี้คือ "json")

print("count   :", body["count"])
# count = จำนวนนักศึกษาที่ server นับให้ (ตอบโจทย์: จำนวน Engineering)

rows = body["data"]
# rows = list ของนักศึกษา แต่ละคนเป็น dict (student_id, name, faculty, ...)

print("จำนวน Engineering (นับเอง):", len(rows))
# len(rows) = นับเองด้วย Python เพื่อตรวจว่าตรงกับ count ของ server
#             (นิสัยที่ดีของ Data Engineer: ตรวจซ้ำ ไม่เชื่อตัวเลขทันที)

print("ชนิดของ skills:", type(rows[0]["skills"]).__name__)
# rows[0]["skills"] = skills ของคนแรก, type().__name__ = ชื่อชนิดข้อมูล
# ผลที่ได้คือ "list" (ตอบโจทย์: ตรวจชนิดของ skills)

print("ตัวอย่าง 1 แถว:")
print(json.dumps(rows[0], ensure_ascii=False, indent=2))
# json.dumps = แปลง dict กลับเป็นข้อความ JSON
# indent=2 = เว้นย่อหน้าให้อ่านง่าย
# ensure_ascii=False = ให้ภาษาไทยแสดงเป็นตัวอักษรจริง ไม่เป็นรหัส \u0e01

# ----- กรณี error: ทดสอบ faculty ที่ไม่มีอยู่จริง -----
r2 = requests.get(url, params={"faculty": "Magic"})
# ส่ง request ซ้ำด้วยคณะที่ไม่มี เพื่อดูว่า server ตอบอย่างไร

print("\n--- ทดสอบ faculty ที่ไม่มี ---")
print("Status:", r2.status_code, "| count:", r2.json().get("count"))
# .get("count") = ถ้าไม่มี key จะได้ None แทนที่โปรแกรมจะ crash (ต่างจาก ["count"])
# เอาผลที่ได้มาอธิบายเป็น "error/edge case" ในรายงาน