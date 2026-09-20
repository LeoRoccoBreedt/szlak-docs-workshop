#!/usr/bin/env python3
"""List itineraries and flag any delayed legs."""

import json
import os
import urllib.request

BASE = os.environ.get("SZLAK_BASE_URL", "http://127.0.0.1:8420")


def itineraries():
    with urllib.request.urlopen(f"{BASE}/itineraries") as response:
        return json.load(response)


def main():
    data = itineraries()
    print(f"{data['count']} itineraries\n")

    for itinerary in data["itineraries"]:
        print(f"  {itinerary['itinerary_id']}  {itinerary['traveller']}  "
              f"[{itinerary['status']}]")
        for leg in itinerary["legs"]:
            marker = "!" if leg["status"] == "delayed" else " "
            print(f"   {marker} leg {leg['leg']}: {leg['from']} -> {leg['to']} "
                  f"({leg['status']})")
            if leg["status"] == "delayed":
                print(f"      {leg['delay_hours']} h - {leg['delay_reason']}")
        print()


if __name__ == "__main__":
    main()
