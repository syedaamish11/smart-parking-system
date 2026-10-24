-- ========================================================
-- Smart Parking Management System - Relational Schema
-- Engine: SQLite / PostgreSQL compatible
-- ========================================================

PRAGMA foreign_keys = ON;

-- 1. Parking Spots Definition
CREATE TABLE IF NOT EXISTS parking_spots (
    spot_id INTEGER PRIMARY KEY AUTOINCREMENT,
    spot_number TEXT NOT NULL UNIQUE,
    floor_number INTEGER NOT NULL DEFAULT 1,
    spot_type TEXT CHECK(spot_type IN ('COMPACT', 'STANDARD', 'EV', 'LARGE')) NOT NULL DEFAULT 'STANDARD',
    is_occupied INTEGER NOT NULL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Vehicle Registry
CREATE TABLE IF NOT EXISTS vehicles (
    vehicle_id INTEGER PRIMARY KEY AUTOINCREMENT,
    license_plate TEXT NOT NULL UNIQUE,
    vehicle_type TEXT CHECK(vehicle_type IN ('BIKE', 'CAR', 'SUV', 'EV')) NOT NULL DEFAULT 'CAR',
    owner_name TEXT,
    registered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Parking Sessions & Automated Billing
CREATE TABLE IF NOT EXISTS parking_sessions (
    session_id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_code TEXT NOT NULL UNIQUE,
    vehicle_id INTEGER NOT NULL,
    spot_id INTEGER NOT NULL,
    entry_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    exit_time TIMESTAMP,
    duration_hours REAL,
    hourly_rate REAL NOT NULL DEFAULT 5.0,
    total_fee REAL DEFAULT 0.0,
    payment_status TEXT CHECK(payment_status IN ('PENDING', 'PAID', 'CANCELLED')) DEFAULT 'PENDING',
    FOREIGN KEY (vehicle_id) REFERENCES vehicles(vehicle_id) ON DELETE CASCADE,
    FOREIGN KEY (spot_id) REFERENCES parking_spots(spot_id) ON DELETE RESTRICT
);

-- 4. Audit & Analytics View
CREATE VIEW IF NOT EXISTS v_active_sessions AS
SELECT 
    s.ticket_code,
    v.license_plate,
    v.vehicle_type,
    p.spot_number,
    p.floor_number,
    p.spot_type,
    s.entry_time
FROM parking_sessions s
JOIN vehicles v ON s.vehicle_id = v.vehicle_id
JOIN parking_spots p ON s.spot_id = p.spot_id
WHERE s.payment_status = 'PENDING';

-- 5. Seed Data: Default Spots
INSERT OR IGNORE INTO parking_spots (spot_number, floor_number, spot_type) VALUES
('F1-01', 1, 'EV'),
('F1-02', 1, 'EV'),
('F1-03', 1, 'COMPACT'),
('F1-04', 1, 'STANDARD'),
('F1-05', 1, 'STANDARD'),
('F1-06', 1, 'LARGE'),
('F2-01', 2, 'STANDARD'),
('F2-02', 2, 'STANDARD'),
('F2-03', 2, 'STANDARD'),
('F2-04', 2, 'LARGE');
