# 🅿️ Smart Parking Management & Automation System

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![SQL](https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-003B57?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Tests](https://img.shields.io/badge/Tests-Passing-success?style=flat&logo=githubactions&logoColor=white)](#)
[![Focus](https://img.shields.io/badge/Focus-Database%20Design%20%7C%20Automation-orange)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An automated backend and relational database management system for smart multi-level parking facilities. It provides automated spot assignment, dynamic hourly billing based on vehicle class (Car, SUV, EV, Bike), real-time occupancy tracking, audit logging, and automated receipt generation.

---

## 🏛️ Relational Database Schema

```
+------------------+          +-------------------+
|  PARKING_SPOTS   |          |     VEHICLES      |
+------------------+          +-------------------+
| PK spot_id       |          | PK vehicle_id     |
|    spot_number   |          |    license_plate  |
|    floor_number  |          |    vehicle_type   |
|    spot_type     |          |    owner_name     |
|    is_occupied   |          +---------+---------+
+--------+---------+                    |
         |                              |
         |    +--------------------+    |
         +--->|  PARKING_SESSIONS  |<---+
              +--------------------+
              | PK session_id      |
              |    ticket_code     |
              | FK vehicle_id      |
              | FK spot_id         |
              |    entry_time      |
              |    exit_time       |
              |    duration_hours  |
              |    hourly_rate     |
              |    total_fee       |
              |    payment_status  |
              +--------------------+
```

---

## ✨ Features

- **Automated Spot Allocation**: Intelligent algorithm assigns matching spots (EV charging spots for EVs, Compact spots for bikes, Standard/Large for cars & SUVs).
- **Dynamic Tiered Hourly Rates**:
  - `Bike`: $2.50 / hour
  - `Car`: $5.00 / hour
  - `EV`: $6.00 / hour
  - `SUV`: $7.00 / hour
- **Real-Time Occupancy Matrix**: Detailed floor-by-floor breakdown of capacity utilization and vacant spots.
- **Automated Receipt Generation**: Formatted ASCII transaction receipts generated upon checkout.
- **Relational Integrity**: Foreign key cascades, check constraints, and normalized views (`v_active_sessions`).
- **Comprehensive Unit Tests**: Built-in `unittest` test suite covering parking, billing, and edge cases.

---

## 🚀 Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/syedaamish11/smart-parking-system.git
cd smart-parking-system
```

### 2. Run the interactive management console
```bash
python main.py
```

### 3. Run automated unit tests
```bash
python -m unittest discover -s tests
```

---

## 🧾 Sample Formatted Receipt

```
+--------------------------------------------------+
|           SMART PARKING AUTOMATION RECEIPT       |
+--------------------------------------------------+
  Ticket ID      : TKT-A1B2C3D4
  Status         : PAID
  Guest Name     : Syed Aamish
  Vehicle Plate  : TESLA-EV1 (EV)
  Assigned Spot  : F1-01 (Floor 1)
  Entry Time     : 2026-10-25 10:00:00
  Exit Time      : 2026-10-25 12:30:00
  Duration       : 2.5 hrs
  Hourly Rate    : $6.00/hr
----------------------------------------------------
  TOTAL BILLED   : $15.00
+--------------------------------------------------+
|         Thank you for choosing Smart Parking!    |
+--------------------------------------------------+
```

---

## 📁 Project Structure

```
smart-parking-system/
├── tests/
│   └── test_parking.py      # Automated test suite (allocation, checkout, receipts)
├── database.py              # SQLite connection, migrations, and spot query engine
├── parking_manager.py       # Core orchestration, billing logic, and receipt generator
├── schema.sql               # Relational DDL, constraints, views, and seed spots
├── main.py                  # CLI operator interface
└── README.md
```

---

## 👤 Author
- **Syed Aamish** — [GitHub Profile](https://github.com/syedaamish11)