# ===== lab09.py : Lab 09 - ตรวจข้อมูลหลัง seed MongoDB (npm run seed:mongo) =====

import json
from pathlib import Path
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError, ServerSelectionTimeoutError

URI = "mongodb://127.0.0.1:27017"
DB_NAME = "nuxt_intern"
DATA_DIR = Path(__file__).parent / "server" / "data"
# ใช้ค่าเดียวกับ .env.example และ scripts/seed-mongo.mjs

# collection -> field ที่ seed สร้าง unique index ไว้ (ตาม seed-mongo.mjs บรรทัด 14)
COLLECTIONS = {
    "students": "student_id",
    "courses": "course_id",
    "instructors": "instructor_id",
    "enrollments": "enrollment_id",
    "social_pages": "id",
    "social_posts": "id",
}

# --- 1) เชื่อมต่อ ---
client = MongoClient(URI, serverSelectionTimeoutMS=3000)
try:
    client.admin.command("ping")
except ServerSelectionTimeoutError as e:
    print("เชื่อมต่อ MongoDB ไม่ได้ (เปิด Docker แล้วหรือยัง? docker compose up -d)")
    print("Error:", type(e).__name__)
    raise SystemExit(1)
db = client[DB_NAME]
print("Connected:", URI, "/", DB_NAME)
# ping ก่อน เพื่อให้รู้ทันทีว่า MongoDB เปิดอยู่ไหม (รอไม่เกิน 3 วินาที)

# --- 2) ตรวจจำนวนเอกสาร: JSON ต้นทาง เทียบกับ MongoDB ---
print("\n=== จำนวนเอกสาร ===")
print(f"{'collection':<14}{'JSON':>6}{'Mongo':>7}  ตรงกัน")
total_json = total_mongo = 0
for name in COLLECTIONS:
    json_count = len(json.loads((DATA_DIR / f"{name}.json").read_text(encoding="utf-8")))
    mongo_count = db[name].count_documents({})
    total_json += json_count
    total_mongo += mongo_count
    print(f"{name:<14}{json_count:>6}{mongo_count:>7}  {'✅' if json_count == mongo_count else '❌'}")
print(f"{'รวม':<14}{total_json:>6}{total_mongo:>7}  {'✅' if total_json == total_mongo else '❌'}")
# นับจากไฟล์จริง ไม่ใช่ตัวเลขที่จำมา จึงพิสูจน์ได้ว่า seed ครบ

# --- 3) ตรวจ unique index ---
print("\n=== Unique index ===")
for name, field in COLLECTIONS.items():
    info = db[name].index_information()
    unique = [idx for idx, spec in info.items() if spec.get("unique")]
    expected = f"{field}_1"
    print(f"{name:<14} unique index: {unique}  {'✅' if expected in unique else '❌ ไม่พบ ' + expected}")
# index ชื่อ <field>_1 สร้างโดย createIndex({field: 1}, {unique: true})
# _id_ ไม่แสดง เพราะ MongoDB สร้างให้เองทุก collection และไม่มี key "unique" ใน spec

# --- edge case: ใส่ student_id ที่มีอยู่แล้ว ---
print("\n=== Edge case: insert student_id 1001 ซ้ำ ===")
before = db["students"].count_documents({})
try:
    db["students"].insert_one({"student_id": 1001, "name": "Duplicate Test"})
    print("❌ insert สำเร็จ (ไม่ควรเกิด แปลว่าไม่มี unique index)")
except DuplicateKeyError as e:
    print("DuplicateKeyError code:", e.code)
    print("Message:", e.details.get("errmsg"))
after = db["students"].count_documents({})
print("จำนวน students ก่อน/หลัง:", before, "/", after)
# code 11000 = duplicate key; API POST /api/storage/mongo/students แปลงเป็น HTTP 409
# ก่อน/หลังเท่ากัน = index กันข้อมูลซ้ำได้จริง ไม่มีอะไรถูกเพิ่ม

client.close()
