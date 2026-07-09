# Roadmap: Data Engineering & dbt Portfolio Project

แผนงานนี้ถูกออกแบบมาเพื่อสร้างโปรเจกต์ Data Engineering แบบ Full-stack บน GitHub เพื่อดึงดูด Recruiter และโชว์ทักษะ Modern Data Stack (dbt, Airflow, Cloud Data Warehouse)

---

## 🚀 Step 1: Data Ingestion (ดึงข้อมูลดิบ)
**เป้าหมาย:** เขียน Python Script ดึงข้อมูลจาก Public API มาเก็บเป็น Raw Data (Bronze Layer)

**สิ่งที่จะทำ:**
- [ ] เลือก Public API ที่น่าสนใจ (เช่น OpenWeather, CoinGecko สำหรับคริปโต, หรือ OMDb สำหรับหนัง)
- [ ] เขียน Python script ใช้ไลบรารี `requests` ดึงข้อมูลมาเป็น JSON
- [ ] แปลง JSON เป็น Pandas DataFrame และบันทึกเป็นไฟล์ `.csv` หรือ `.parquet`
- [ ] อัปโหลดไฟล์ดิบนี้ขึ้น Cloud Storage (เช่น AWS S3 หรือ Google Cloud Storage) หรือโหลดตรงเข้า BigQuery

---

## 🚀 Step 2: Cloud Data Warehouse Setup (ตั้งค่า BigQuery/Databricks)
**เป้าหมาย:** นำข้อมูลดิบเข้าสู่ Data Warehouse

**สิ่งที่จะทำ:**
- [ ] สร้าง Project และ Dataset บน Google Cloud BigQuery (ฟรี Tier เพียงพอ)
- [ ] โหลดไฟล์จาก Step 1 เข้าเป็นตาราง Raw Table (Landing Zone)

---

## 🚀 Step 3: Data Transformation (แปลงข้อมูลด้วย dbt)
**เป้าหมาย:** โชว์สกิลที่ตลาดตามหาที่สุดตอนนี้ คือการใช้ dbt ทำ Transformation (Silver & Gold Layer)

**สิ่งที่จะทำ:**
- [ ] ติดตั้ง `dbt-core` และ `dbt-bigquery`
- [ ] สร้างโปรเจกต์ dbt (`dbt init`) และเชื่อมต่อกับ BigQuery
- [ ] **Silver Layer:** เขียน SQL models (`.sql`) เพื่อคลีนข้อมูล (เช่น เปลี่ยนชื่อคอลัมน์, จัดการ Null)
- [ ] **Gold Layer:** เขียน SQL models เพื่อ Aggregate ข้อมูลให้อยู่ในรูป Star Schema พร้อมใช้งาน
- [ ] ใส่ dbt Tests (Unique, Not Null) ลงในไฟล์ `schema.yml` เพื่อโชว์ทักษะ QA
- [ ] สร้าง Document อัตโนมัติด้วยคำสั่ง `dbt docs generate`

---

## 🚀 Step 4: Orchestration (ตั้งเวลาด้วย Apache Airflow)
**เป้าหมาย:** ทำให้ทุกอย่างทำงานแบบอัตโนมัติ

**สิ่งที่จะทำ:**
- [ ] เขียน Airflow DAG (`.py`)
- [ ] สร้าง Task 1: สั่งรัน Python Ingestion (จาก Step 1)
- [ ] สร้าง Task 2: สั่งรันคำสั่ง `dbt run` และ `dbt test` (จาก Step 3)
- [ ] (ทางเลือก) หากไม่อยากเซ็ตอัป Airflow เครื่องตัวเอง สามารถใช้ GitHub Actions เป็นตัวตั้งเวลา (Cron job) แทนได้ ซึ่งทำได้ง่ายและโชว์ทักษะ CI/CD

---

## 🚀 Step 5: GitHub Presentation
**เป้าหมาย:** สรุปผลงานให้น่าสนใจ

**สิ่งที่จะทำ:**
- [ ] อัปโหลดโค้ดทั้งหมดขึ้น GitHub Repo
- [ ] เขียนไฟล์ `README.md` อธิบาย Architecture Diagram (สามารถวาดด้วย draw.io)
- [ ] อธิบาย Business Value ว่า Pipeline นี้เอาไปต่อยอดทำ Dashboard อะไรได้บ้าง
