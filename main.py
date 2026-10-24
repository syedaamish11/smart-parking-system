"""
Smart Parking System - Interactive Dashboard & Simulator
"""

import sys
from database import init_db
from parking_manager import ParkingManager

def display_menu():
    print("\n" + "=" * 55)
    print("   🚗 Smart Parking Management & Automation")
    print("=" * 55)
    print(" 1. Park Vehicle (Check-in & Issue Ticket)")
    print(" 2. Checkout Vehicle (Calculate Fee & Vacate Spot)")
    print(" 3. View Real-time Lot Status & Vacancy Matrix")
    print(" 4. View Financial & Parking Analytics")
    print(" 5. Exit")
    print("-" * 55)

def main():
    init_db()

    while True:
        display_menu()
        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            plate = input("Enter License Plate (e.g. ABC-1234): ").strip()
            v_type = input("Enter Vehicle Type (CAR / SUV / EV / BIKE): ").strip()
            owner = input("Enter Driver / Owner Name (optional): ").strip()

            result = ParkingManager.park_vehicle(plate, v_type, owner)
            if result["success"]:
                print(f"\n[SUCCESS] Vehicle parked successfully!")
                print(f"  * Ticket Code  : {result['ticket_code']}")
                print(f"  * Assigned Spot: {result['spot_number']} (Floor {result['floor']})")
                print(f"  * Hourly Rate  : ${result['hourly_rate']:.2f}/hr")
            else:
                print(f"\n[ERROR] {result['message']}")

        elif choice == "2":
            ticket = input("Enter Ticket Code (e.g. TKT-1234ABCD): ").strip()
            try:
                hours = float(input("Enter Parked Duration (in hours): ").strip())
            except ValueError:
                hours = 1.0

            result = ParkingManager.exit_vehicle(ticket, hours)
            if result["success"]:
                print(f"\n[SUCCESS] Checkout completed!")
                print(f"  * Plate Number : {result['license_plate']}")
                print(f"  * Freed Spot   : {result['spot_number']}")
                print(f"  * Hours Parked : {result['hours']} hrs")
                print(f"  * Total Fee Due: ${result['total_fee']:.2f}")
            else:
                print(f"\n[ERROR] {result['message']}")

        elif choice == "3":
            overview = ParkingManager.get_live_overview()
            print("\n--- Live Spot Vacancy ---")
            for item in overview["spots"]:
                free = item["total"] - item["occupied"]
                print(f"  * {item['spot_type']:<10}: {free}/{item['total']} Available")

            print(f"\n--- Currently Parked Vehicles ({len(overview['active_tickets'])}) ---")
            for t in overview["active_tickets"]:
                print(f"  [{t['ticket_code']}] {t['license_plate']} ({t['vehicle_type']}) at Spot {t['spot_number']}")

        elif choice == "4":
            overview = ParkingManager.get_live_overview()
            print("\n--- Revenue & Statistics ---")
            print(f"  * Completed Checkouts: {overview['completed_sessions']}")
            print(f"  * Total Revenue Earned: ${overview['total_revenue']:.2f}")

        elif choice == "5":
            print("\nExiting Smart Parking System. Have a great day!")
            break
        else:
            print("Invalid selection. Please choose between 1 and 5.")

if __name__ == "__main__":
    main()
