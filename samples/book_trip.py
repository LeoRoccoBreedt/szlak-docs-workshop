#!/usr/bin/env python3
"""Book a trip for one or more travellers."""

import json
import os
import urllib.request

BASE = os.environ.get("SZLAK_BASE_URL", "http://127.0.0.1:8420")


def book(trip_id, travellers=1):
    payload = json.dumps({"trip_id": trip_id, "travellers": travellers}).encode("utf-8")
    request = urllib.request.Request(
        f"{BASE}/bookings",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request) as response:
        return json.load(response)


def main():
    booking = book("tor-mal-005", travellers=2)

    print(f"Booking {booking['booking_id']} confirmed")
    print(f"  Trip:       {booking['trip_id']}")
    print(f"  Travellers: {booking['travellers']}")
    print(f"  Total:      {booking['total_minor'] / 100:.2f} {booking['currency']}")


if __name__ == "__main__":
    main()
