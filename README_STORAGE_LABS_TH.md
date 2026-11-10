# Nuxt.js + JSON + SQLite + MongoDB — Internship Training Pack

ชุดนี้ต่อยอดจาก Nuxt API 12 Labs เดิม ไม่แทนที่ Labs เดิม และใช้ข้อมูลสมมติชุดเดียวกัน (149 records)

## เริ่มต้น
- Node.js ที่รองรับ Nuxt 4; npm; Docker สำหรับ MongoDB (ไม่จำเป็นสำหรับ JSON/SQLite)
- แตก ZIP แล้วเข้าโฟลเดอร์ `Nuxt_API_Intern_12_Labs`

```bash
npm install
cp .env.example .env
npm run dev
```

เปิด `http://localhost:3000` เพื่อใช้หน้า Nuxt เดิม และทดลอง endpoints ใหม่ด้วย Browser, curl หรือ Postman

### MongoDB
```bash
docker compose up -d
npm run seed:mongo
```
**ระวัง:** `seed:mongo` ลบเอกสารใน 6 collections ของฐานข้อมูล `nuxt_intern` ก่อน seed ใหม่ ห้ามตั้ง `MONGODB_DB` เป็นฐานข้อมูลจริง

### API ตัวอย่าง
```bash
curl 'http://localhost:3000/api/storage/json/students?faculty=Engineering'
curl 'http://localhost:3000/api/storage/sqlite/students?min_gpa=3.5'
curl 'http://localhost:3000/api/storage/sqlite/enrollments?student_id=1001'
curl 'http://localhost:3000/api/storage/mongo/students?faculty=IT'
curl 'http://localhost:3000/api/storage/compare'
```

### เพิ่มนักศึกษา (SQLite)
```bash
curl -i -X POST http://localhost:3000/api/storage/sqlite/students \
  -H 'Content-Type: application/json' \
  -d '{"student_id":2001,"name":"Intern Demo","faculty":"IT","year":2,"gpa":3.2,"active":true,"skills":["Nuxt","SQL"]}'
```
MongoDB: เปลี่ยน endpoint เป็น `/api/storage/mongo/students` และใช้ student_id=3001

## ความแตกต่างของ Data Stores
| JSON | SQLite | MongoDB |
|---|---|---|
| ไฟล์ document | relational tables | document collections |
| เหมาะ seed/mock | SQL, JOIN, ACID transactions | flexible nested document, query/index |
| ตัวอย่างนี้ read-only | POST persists in .db | POST persists in Mongo volume |
| ไม่มี SQL query engine | foreign keys + parameterized SQL | unique indexes |

## แบบฝึกหัด 12 ชุด

### Lab 01 — JSON 01
- **Endpoint/command:** `GET /api/storage/json/students`
- **ลงมือทำ:** อ่าน students 30 รายการ; กรอง ?faculty=Engineering
- **โจทย์:** บอกจำนวน Engineering และตรวจชนิดของ skills
- **ส่งงาน:** โค้ด, request, response, HTTP status, ภาพทดสอบ, และคำอธิบาย error อย่างน้อยหนึ่งกรณี

### Lab 02 — JSON 02
- **Endpoint/command:** `GET /data/courses.json`
- **ลงมือทำ:** แสดง 10 วิชา; จับคู่ instructor_id กับ instructors.json
- **โจทย์:** แสดงชื่อผู้สอนโดยไม่แก้ข้อมูลต้นทาง
- **ส่งงาน:** โค้ด, request, response, HTTP status, ภาพทดสอบ, และคำอธิบาย error อย่างน้อยหนึ่งกรณี

### Lab 03 — JSON 03
- **Endpoint/command:** `GET /data/social_posts.json`
- **ลงมือทำ:** กรองโพสต์ตาม page_id และคำค้น
- **โจทย์:** ทำตัวนับ posts ของแต่ละ Page
- **ส่งงาน:** โค้ด, request, response, HTTP status, ภาพทดสอบ, และคำอธิบาย error อย่างน้อยหนึ่งกรณี

### Lab 04 — JSON 04
- **Endpoint/command:** `GET /data/enrollments.json`
- **ลงมือทำ:** จับคู่ student_id/course_id ใน JavaScript
- **โจทย์:** หาค่าเฉลี่ย score ของแต่ละรายวิชา
- **ส่งงาน:** โค้ด, request, response, HTTP status, ภาพทดสอบ, และคำอธิบาย error อย่างน้อยหนึ่งกรณี

### Lab 05 — SQLite 05
- **Endpoint/command:** `GET /api/storage/sqlite/students`
- **ลงมือทำ:** ดึงตาราง students ผ่าน SQL SELECT และ ?min_gpa=3.5
- **โจทย์:** เปรียบเทียบผลกับ JSON; อธิบาย SQL parameter
- **ส่งงาน:** โค้ด, request, response, HTTP status, ภาพทดสอบ, และคำอธิบาย error อย่างน้อยหนึ่งกรณี

### Lab 06 — SQLite 06
- **Endpoint/command:** `GET /api/storage/sqlite/enrollments?student_id=1001`
- **ลงมือทำ:** ทดลอง JOIN students/enrollments/courses
- **โจทย์:** อธิบาย INNER JOIN และผลเมื่อ student_id ไม่พบ
- **ส่งงาน:** โค้ด, request, response, HTTP status, ภาพทดสอบ, และคำอธิบาย error อย่างน้อยหนึ่งกรณี

### Lab 07 — SQLite 07
- **Endpoint/command:** `POST /api/storage/sqlite/students`
- **ลงมือทำ:** INSERT นักศึกษา 2001 และทดสอบ 201/409/422
- **โจทย์:** ลอง GPA 5 และ student_id ซ้ำ; ยืนยันข้อมูลคงอยู่หลัง restart
- **ส่งงาน:** โค้ด, request, response, HTTP status, ภาพทดสอบ, และคำอธิบาย error อย่างน้อยหนึ่งกรณี

### Lab 08 — SQLite 08
- **Endpoint/command:** `GET /api/storage/compare`
- **ลงมือทำ:** เปรียบเทียบ JSON กับ SQLite หลัง INSERT
- **โจทย์:** อธิบายเหตุใด count ต่างกัน; เสนอ sync policy
- **ส่งงาน:** โค้ด, request, response, HTTP status, ภาพทดสอบ, และคำอธิบาย error อย่างน้อยหนึ่งกรณี

### Lab 09 — MongoDB 09
- **Endpoint/command:** `npm run seed:mongo`
- **ลงมือทำ:** นำข้อมูล JSON 6 collections เข้า MongoDB
- **โจทย์:** ตรวจจำนวนเอกสารและ unique index
- **ส่งงาน:** โค้ด, request, response, HTTP status, ภาพทดสอบ, และคำอธิบาย error อย่างน้อยหนึ่งกรณี

### Lab 10 — MongoDB 10
- **Endpoint/command:** `GET /api/storage/mongo/students`
- **ลงมือทำ:** อ่าน document และ filter faculty
- **โจทย์:** เปรียบเทียบ _id กับ student_id; แสดง projection
- **ส่งงาน:** โค้ด, request, response, HTTP status, ภาพทดสอบ, และคำอธิบาย error อย่างน้อยหนึ่งกรณี

### Lab 11 — MongoDB 11
- **Endpoint/command:** `POST /api/storage/mongo/students`
- **ลงมือทำ:** เพิ่ม document และทดสอบ duplicate key
- **โจทย์:** เปรียบเทียบข้อผิดพลาด MongoDB/SQLite
- **ส่งงาน:** โค้ด, request, response, HTTP status, ภาพทดสอบ, และคำอธิบาย error อย่างน้อยหนึ่งกรณี

### Lab 12 — Integration 12
- **Endpoint/command:** `GET JSON, SQLite, MongoDB`
- **ลงมือทำ:** แสดงนักศึกษารายเดียวกันจาก 3 แหล่ง; เปรียบเทียบ
- **โจทย์:** ออกแบบ Data Source of Truth และวิธีตรวจ consistency
- **ส่งงาน:** โค้ด, request, response, HTTP status, ภาพทดสอบ, และคำอธิบาย error อย่างน้อยหนึ่งกรณี

## ข้อมูลต้นทาง
- students 30, courses 10, instructors 5, enrollments 60
- social_pages 2, social_posts 20, ai_tasks 12, api_error_cases 10
- รวม 149 รายการ; SQLite เก็บ 4 ตารางหลัก (105 records); Mongo seed 6 collections (127 records)
- JSON files ใน public/data เปิดให้ browser เห็น: เป็นข้อมูลสมมติเท่านั้น
- SQLite ใช้ `skills_json` (TEXT) และ `active` (INTEGER) แต่ API แปลงกลับเป็น array/boolean
- MongoDB driver ใช้ `MongoClient` ฝั่ง server เท่านั้น ไม่ส่ง connection string ให้ browser

## การตรวจรับ
1. ผล JSON/SQLite/MongoDB ตรงกันก่อนมีการเพิ่มข้อมูล
2. แสดงว่า SQLite JOIN ถูกต้อง และ Mongo filter ใช้งานได้
3. Validation 422, duplicate 409, invalid query 400
4. อธิบาย persistence: JSON file, SQLite file, Mongo volume
5. เสนอ schema migration, backup, auth, rate limit และ secret management ก่อน production

## ข้อจำกัด
- โค้ดเป็น local training demo; ไม่มี authentication/authorization และไม่ควร deploy สาธารณะ
- MongoDB container เปิดพอร์ตเฉพาะ loopback; ยังไม่มี auth เพราะใช้ฝึกในเครื่องเท่านั้น
- Nuxt 4 + native SQLite dependency `better-sqlite3` ต้องมี binary compatible กับ Node.js ของเครื่อง
- ไม่ต้องมี OpenAI API Key สำหรับ 12 labs ใหม่; ชุดเดิม Labs 10–12 ยังต้องใช้ key
