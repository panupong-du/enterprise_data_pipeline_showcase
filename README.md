# 🚀 Enterprise ELT Data Pipeline

Welcome to my Python Data Engineering & Automation Hub! This repository demonstrates a production-grade **ELT (Extract, Load, Transform)** pipeline orchestrated by **Apache Airflow** and powered by **Google BigQuery**.

## 🎯 Business Impact & Context
In a modern data-driven organization, data accuracy and timely reporting are critical. This project simulates a daily batch pipeline that:
1. **Extracts** high-volume transaction records (CSV) and user profiles (Mock API) using Python.
2. **Loads** the raw data into Google BigQuery staging tables (`stg_raw_transactions`, `dim_crm_users`).
3. **Transforms** the data natively inside BigQuery using standard SQL, allowing for massive scalability and avoiding local memory bottlenecks (ELT vs ETL).

This automated pipeline is built with **Idempotency** in mind (using Airflow's `logical_date` / `{{ ds }}`), meaning it can be rerun seamlessly for backfilling data without causing data duplication.

---

## 📂 Project Structure & Features

See [DESIGN.md](DESIGN.md) for the complete High-Level Design Document (HLDD) and Architecture Diagrams.

### Tech Stack
- **Languages:** Python 3, Standard SQL
- **Libraries:** `pandas`, `google-cloud-bigquery`
- **Data Warehouse:** Google Cloud BigQuery
- **Orchestration:** Apache Airflow (Dockerized)
- **Architecture:** Modern ELT (Extract, Load, Transform) with idempotent logic.

---

## ⚙️ How to Run Locally

### 1. Prerequisites
- Docker & Docker Compose (for Airflow)
- A Google Cloud Project with BigQuery enabled
- A Service Account JSON key (placed in the root directory)

### 2. Setup
Clone this repository and install the dependencies:
```bash
pip install -r requirements.txt
```

### 3. Run via Python CLI
You can execute the pipeline for a specific logical date to simulate how Airflow runs the job:
```bash
# Process data for a specific date (Idempotent run)
python main_etl.py --date 2026-07-09
```

### 4. Run via Airflow UI
1. Start the Airflow cluster:
   ```bash
   docker-compose up -d
   ```
2. Access the UI at `http://localhost:8080` (Username/Password: `airflow`)
3. The DAG `enterprise_data_pipeline` is scheduled to run daily at 08:00 UTC. You can trigger it manually to watch the Extract ➔ Load Raw ➔ Transform SQL process flow in action!

*(Note: If you make changes to the DAG files while developing outside the container, run `sync_dags.bat` to sync them into Airflow).*
