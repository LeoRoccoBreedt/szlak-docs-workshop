#!/usr/bin/env python3
"""Search for trips on a given waymarked trail."""

import json
import os
import urllib.parse
import urllib.request

BASE = os.environ.get("SZLAK_BASE_URL", "http://127.0.0.1:8420")

TRAIL = "czerwony"
MAX_HOURS = 8


def search(**params):
    query = urllib.parse.urlencode(params)
    with urllib.request.urlopen(f"{BASE}/search?{query}") as response:
        return json.load(response)


def main():
    result = search(trail_colour=TRAIL, max_duration_hours=MAX_HOURS)

    print(f"Found {result['count']} trips on the {TRAIL} trail\n")
    for trip in result["trips"]:
        # note: max_price and price_minor are both in zloty - see #31
        print(f"  {trip['from']} -> {trip['to']}")
        print(f"    {trip['duration_hours']} h, {trip['difficulty']}, "
              f"{trip['price_minor'] / 100:.2f} PLN")
        print(f"    {trip['summary']}\n")


if __name__ == "__main__":
    main()
