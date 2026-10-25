"""
Unit tests for Smart Parking Management System
Validates database schema, vehicle check-in, dynamic billing, checkout, and receipt generation.
"""

import os
import sys
import unittest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from database import init_db, get_connection
from parking_manager import ParkingManager

class TestSmartParkingSystem(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        init_db()

    def test_01_park_ev_vehicle(self):
        result = ParkingManager.park_vehicle("TESLA-EV1", "EV", "Syed Aamish")
        self.assertTrue(result["success"])
        self.assertIn("TKT-", result["ticket_code"])
        self.assertEqual(result["vehicle_type"], "EV")
        # Spot should be EV spot (e.g. F1-01)
        self.assertTrue(result["spot_number"].startswith("F1"))

    def test_02_occupancy_matrix(self):
        matrix = ParkingManager.get_occupancy_matrix()
        self.assertIn("floors", matrix)
        self.assertGreater(len(matrix["floors"]), 0)
        floor1 = next(f for f in matrix["floors"] if f["floor"] == 1)
        self.assertGreaterEqual(floor1["occupied"], 1)

    def test_03_exit_vehicle_and_billing(self):
        park_res = ParkingManager.park_vehicle("CAR-TEST9", "CAR", "John Doe")
        self.assertTrue(park_res["success"])
        ticket = park_res["ticket_code"]

        exit_res = ParkingManager.exit_vehicle(ticket, hours_parked=2.5)
        self.assertTrue(exit_res["success"])
        # Rate for CAR is $5.00/hr * 2.5 = $12.50
        self.assertEqual(exit_res["total_fee"], 12.50)

    def test_04_receipt_generation(self):
        park_res = ParkingManager.park_vehicle("BIKE-B1", "BIKE", "Alice")
        ticket = park_res["ticket_code"]
        ParkingManager.exit_vehicle(ticket, hours_parked=2.0)

        receipt = ParkingManager.generate_receipt(ticket)
        self.assertIn("SMART PARKING AUTOMATION RECEIPT", receipt)
        self.assertIn("BIKE-B1", receipt)
        self.assertIn("PAID", receipt)

    def test_05_unsupported_vehicle(self):
        res = ParkingManager.park_vehicle("PLANE-001", "AIRPLANE")
        self.assertFalse(res["success"])
        self.assertIn("Unsupported", res["message"])

if __name__ == "__main__":
    unittest.main()