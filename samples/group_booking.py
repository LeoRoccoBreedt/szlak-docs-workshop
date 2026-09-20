#!/usr/bin/env python3
"""Find a trip within budget for a group, then book it.

Groups of six or more receive a 10% discount, applied at booking.
"""

import json
import os
import urllib.parse
import urllib.request

BASE = os.environ.get("SZLAK_BASE_URL", "http://127.0.0.1:8420")

GROUP_SIZE = 8
BUDGET_PER_PERSON = 250


def search(**params):
    query = urllib.parse.urlencode(params)
    with urllib.request.urlopen(f"{BASE}/search?{query}") as response:
        return json.load(response)


def book(trip_id, travellers):
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
    result = search(max_price=BUDGET_PER_PERSON, max_duration_hours=6)

    if result["count"] == 0:
        print("No trips within budget.")
        return

    trip = result["trips"][0]
    print(f"Selected: {trip['from']} -> {trip['to']}")

    booking = book(trip["id"], GROUP_SIZE)
    print(f"Booked {booking['travellers']} travellers")
    print(f"  Total: {booking['total_minor'] / 100:.2f} {booking['currency']}")


if __name__ == "__main__":
    main()
