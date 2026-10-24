"""
Database Manager for Smart Parking System
Handles SQLite connection, schema migrations, and queries.
"""

import sqlite3
import os
from typing import List, Dict, Optional, Tuple

DB_PATH = os.path.join(os.path.dirname(__file__), "parking_system.db")
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "schema.sql")

def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    """Initializes tables and seed data using schema.sql."""
    conn = get_connection()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()

def find_available_spot(vehicle_type: str) -> Optional[sqlite3.Row]:
    """Selects the optimal free spot based on vehicle requirements."""
    type_map = {
        "BIKE": "COMPACT",
        "EV": "EV",
        "CAR": "STANDARD",
        "SUV": "LARGE"
    }
    preferred_spot = type_map.get(vehicle_type.upper(), "STANDARD")
    conn = get_connection()
    cursor = conn.cursor()

    # Try preferred spot type first, otherwise standard
    cursor.execute("""
        SELECT * FROM parking_spots 
        WHERE is_occupied = 0 AND spot_type = ? 
        ORDER BY floor_number ASC, spot_number ASC LIMIT 1
    """, (preferred_spot,))
    spot = cursor.fetchone()

    if not spot and preferred_spot != "STANDARD":
        cursor.execute("""
            SELECT * FROM parking_spots 
            WHERE is_occupied = 0 AND spot_type = 'STANDARD' 
            ORDER BY floor_number ASC, spot_number ASC LIMIT 1
        """)
        spot = cursor.fetchone()

    conn.close()
    return spot
