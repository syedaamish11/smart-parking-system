# 🚗 Smart Parking Management & Automation System

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=flat&logo=python&logoColor=white)](https://python.org)
[![SQL](https://img.shields.io/badge/Database-SQLite%20%7C%20PostgreSQL-003B57?style=flat&logo=sqlite&logoColor=white)](https://sqlite.org)
[![Focus](https://img.shields.io/badge/Focus-Database%20Design%20%7C%20Automation-orange)](#)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

An automated backend and relational database management system for smart multi-level parking facilities. It provides automated spot assignment, dynamic hourly billing based on vehicle class (Car, SUV, EV, Bike), real-time occupancy tracking, and transaction auditing.

---

## 🏗️ Relational Database Schema

```
┌─────────────────────┐          ┌─────────────────────┐
│    PARKING_SPOTS    │          │      VEHICLES       │
├─────────────────────┤          ├─────────────────────┤
│ PK  spot_id         │          │ PK  vehicle_id      │
│     spot_number     │          │     license_plate   │
│     floor_number    │          │     vehicle_type    │
│     spot_type       │          │     owner_name      │
│     is_occupied     │          └──────────┬──────────┘
└──────────┬──────────┘                     │
           │                                │
           │     ┌────────────────────┐     │
           └────►│  PARKING_SESSIONS  │◄────┘
                 ├────────────────────┤
                 │ PK  session_id     │
                 │     ticket_code    │
                 │ FK  vehicle_id     │
                 │ FK  spot_id        │
                 │     entry_time     │
                 │     exit_time      │
                 │     duration_hours │
                 │     hourly_rate    │
                 │     total_fee      │
                 │     payment_status │
                 └────────────────────┘
```

---

## ✨ Features

- **Automated Spot Allocation**: Intelligent algorithm assigns matching spots (EV charging spots for EVs, Compact spots for bikes, Standard/Large for cars & SUVs).
- **Relational Integrity**: Foreign keys, check constraints, indexed lookup by license plate and ticket code.
- **SQL Analytical Views**: Pre-configured views (`v_active_sessions`) for instant occupancy reporting.
- **Dynamic Fee Calculation**: Computes duration-based rates upon exit and frees up the spot in a single atomic transaction.
- **Interactive Terminal Simulator**: Test check-ins, ticket validation, fee calculations, and audit logs.

---

## 🚀 Quickstart

### 1. Clone the repository
```bash
git clone https://github.com/syedaamish11/smart-parking-system.git
cd smart-parking-system
```

### 2. Run the application (Zero external dependencies needed!)
```bash
python main.py
```
*The database and seed parking spots are automatically initialized on the first run.*

---

## 📂 Project Structure

```
smart-parking-system/
├── schema.sql              # Database schema DDL, views, and seed spots
├── database.py             # SQLite connection wrapper and queries
├── parking_manager.py      # Business logic and automated billing calculations
├── main.py                 # Interactive terminal dashboard & simulator
└── README.md
```

---

## 🛠️ Tech Stack
- **Database**: SQLite / SQL (Relations, Foreign Keys, Views, Check Constraints)
- **Language**: Python 3
- **Concepts**: Database Normalization, Automated Resource Allocation, Transaction Handling

---

## 👤 Author
- **Syed Aamish** — [GitHub Profile](https://github.com/syedaamish11)
