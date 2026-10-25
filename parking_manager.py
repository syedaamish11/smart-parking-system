"""
Parking Automation & Business Logic Manager
Orchestrates vehicle entry, ticket generation, rate calculation, exit checkout,
and automated receipt formatting.
"""

import uuid
import datetime
from database import get_connection, find_available_spot

HOURLY_RATES = {
    "BIKE": 2.50,
    "CAR": 5.00,
    "SUV": 7.00,
    "EV": 6.00
}

class ParkingManager:
    @staticmethod
    def park_vehicle(license_plate: str, vehicle_type: str, owner_name: str = "") -> dict:
        plate = license_plate.strip().upper()
        v_type = vehicle_type.strip().upper()

        if v_type not in HOURLY_RATES:
            return {"success": False, "message": f"Unsupported vehicle type: {vehicle_type}"}

        spot = find_available_spot(v_type)
        if not spot:
            return {"success": False, "message": "Sorry, no vacant parking spots available!"}

        conn = get_connection()
        cursor = conn.cursor()

        # 1. Upsert vehicle record
        cursor.execute("SELECT vehicle_id FROM vehicles WHERE license_plate = ?", (plate,))
        v_row = cursor.fetchone()
        if not v_row:
            cursor.execute(
                "INSERT INTO vehicles (license_plate, vehicle_type, owner_name) VALUES (?, ?, ?)",
                (plate, v_type, owner_name)
            )
            vehicle_id = cursor.lastrowid
        else:
            vehicle_id = v_row["vehicle_id"]

        # 2. Mark spot as occupied
        cursor.execute("UPDATE parking_spots SET is_occupied = 1 WHERE spot_id = ?", (spot["spot_id"],))

        # 3. Create active session ticket
        ticket_code = f"TKT-{str(uuid.uuid4())[:8].upper()}"
        rate = HOURLY_RATES[v_type]
        cursor.execute("""
            INSERT INTO parking_sessions (ticket_code, vehicle_id, spot_id, hourly_rate, payment_status)
            VALUES (?, ?, ?, ?, 'PENDING')
        """, (ticket_code, vehicle_id, spot["spot_id"], rate))

        conn.commit()
        conn.close()

        return {
            "success": True,
            "ticket_code": ticket_code,
            "spot_number": spot["spot_number"],
            "floor": spot["floor_number"],
            "vehicle_type": v_type,
            "hourly_rate": rate
        }

    @staticmethod
    def exit_vehicle(ticket_code: str, hours_parked: float = 1.0) -> dict:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT s.*, v.license_plate, v.vehicle_type, p.spot_number 
            FROM parking_sessions s
            JOIN vehicles v ON s.vehicle_id = v.vehicle_id
            JOIN parking_spots p ON s.spot_id = p.spot_id
            WHERE s.ticket_code = ? AND s.payment_status = 'PENDING'
        """, (ticket_code.strip().upper(),))
        session = cursor.fetchone()

        if not session:
            conn.close()
            return {"success": False, "message": "Ticket not found or already paid."}

        # Calculate fee
        total_fee = max(hours_parked, 0.5) * session["hourly_rate"]
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Update session
        cursor.execute("""
            UPDATE parking_sessions 
            SET exit_time = ?, duration_hours = ?, total_fee = ?, payment_status = 'PAID'
            WHERE session_id = ?
        """, (now, hours_parked, total_fee, session["session_id"]))

        # Free spot
        cursor.execute("UPDATE parking_spots SET is_occupied = 0 WHERE spot_id = ?", (session["spot_id"],))

        conn.commit()
        conn.close()

        return {
            "success": True,
            "ticket_code": ticket_code,
            "license_plate": session["license_plate"],
            "spot_number": session["spot_number"],
            "hours": hours_parked,
            "total_fee": round(total_fee, 2)
        }

    @staticmethod
    def generate_receipt(ticket_code: str) -> str:
        """Generates a clean formatted ASCII transaction receipt."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT s.*, v.license_plate, v.vehicle_type, v.owner_name, p.spot_number, p.floor_number
            FROM parking_sessions s
            JOIN vehicles v ON s.vehicle_id = v.vehicle_id
            JOIN parking_spots p ON s.spot_id = p.spot_id
            WHERE s.ticket_code = ?
        """, (ticket_code.strip().upper(),))
        row = cursor.fetchone()
        conn.close()

        if not row:
            return f"Receipt Error: Ticket {ticket_code} not found."

        owner = row["owner_name"] or "Valued Guest"
        exit_time = row["exit_time"] or "In Progress"
        duration = f"{row['duration_hours']:.1f} hrs" if row["duration_hours"] else "Active"
        fee = f"${row['total_fee']:.2f}" if row["total_fee"] is not None else "$0.00"

        receipt = f"""
+--------------------------------------------------+
|           SMART PARKING AUTOMATION RECEIPT       |
+--------------------------------------------------+
  Ticket ID      : {row['ticket_code']}
  Status         : {row['payment_status']}
  Guest Name     : {owner}
  Vehicle Plate  : {row['license_plate']} ({row['vehicle_type']})
  Assigned Spot  : {row['spot_number']} (Floor {row['floor_number']})
  Entry Time     : {row['entry_time']}
  Exit Time      : {exit_time}
  Duration       : {duration}
  Hourly Rate    : ${row['hourly_rate']:.2f}/hr
----------------------------------------------------
  TOTAL BILLED   : {fee}
+--------------------------------------------------+
|         Thank you for choosing Smart Parking!    |
+--------------------------------------------------+
""".strip()
        return receipt

    @staticmethod
    def get_occupancy_matrix() -> dict:
        """Returns floor-by-floor capacity and vacancy metrics."""
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                floor_number,
                COUNT(*) as total_spots,
                SUM(is_occupied) as occupied_spots,
                COUNT(*) - SUM(is_occupied) as available_spots
            FROM parking_spots
            GROUP BY floor_number
            ORDER BY floor_number ASC
        """)
        floors = []
        for r in cursor.fetchall():
            tot = r["total_spots"]
            occ = r["occupied_spots"]
            utilization = round((occ / tot * 100.0), 1) if tot > 0 else 0.0
            floors.append({
                "floor": r["floor_number"],
                "total": tot,
                "occupied": occ,
                "available": r["available_spots"],
                "utilization_pct": utilization
            })

        conn.close()
        return {"floors": floors}

    @staticmethod
    def get_live_overview() -> dict:
        conn = get_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT spot_type, COUNT(*) as total, SUM(is_occupied) as occupied FROM parking_spots GROUP BY spot_type")
        spot_summary = [dict(row) for row in cursor.fetchall()]

        cursor.execute("SELECT * FROM v_active_sessions")
        active_tickets = [dict(row) for row in cursor.fetchall()]

        cursor.execute("SELECT COUNT(*) as completed_sessions, SUM(total_fee) as revenue FROM parking_sessions WHERE payment_status = 'PAID'")
        stats = dict(cursor.fetchone())

        conn.close()
        return {
            "spots": spot_summary,
            "active_tickets": active_tickets,
            "total_revenue": stats.get("revenue") or 0.0,
            "completed_sessions": stats.get("completed_sessions") or 0
        }