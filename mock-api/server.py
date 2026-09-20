#!/usr/bin/env python3
"""
Szlak API - local mock server.

Serves fixture data so the code samples in samples/ can actually run.
No network access required, no dependencies beyond the standard library.

The API version is controlled by the SZLAK_API_VERSION environment variable:

    2.0  (default)  max_price      - accepts zloty
    2.1             max_price_minor - accepts grosze, rejects max_price

See ISSUE-47.md for the change that introduced 2.1.
"""

import json
import os
import re
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

FIXTURES = Path(__file__).parent / "fixtures"
VERSION = os.environ.get("SZLAK_API_VERSION", "2.0")
PORT = int(os.environ.get("SZLAK_PORT", "8420"))


def load(name):
    with open(FIXTURES / name, encoding="utf-8") as f:
        return json.load(f)


class SzlakHandler(BaseHTTPRequestHandler):
    def log_message(self, *args):
        pass  # keep sample output clean

    def _send(self, status, payload):
        body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("X-Szlak-Version", VERSION)
        self.end_headers()
        self.wfile.write(body)

    def _error(self, status, code, **extra):
        payload = {"error": code}
        payload.update(extra)
        self._send(status, payload)

    # ------------------------------------------------------------------ GET
    def do_GET(self):
        url = urlparse(self.path)
        params = {k: v[0] for k, v in parse_qs(url.query).items()}

        if url.path == "/health":
            return self._send(200, {"status": "ok", "version": VERSION})

        if url.path == "/search":
            return self.search(params)

        if url.path == "/itineraries":
            return self._send(200, load("itineraries.json"))

        return self._error(404, "not_found", path=url.path)

    def search(self, params):
        price_field = "max_price_minor" if VERSION >= "2.1" else "max_price"
        retired = "max_price" if VERSION >= "2.1" else None

        # v2.1 removed max_price with no deprecation window.
        if retired and retired in params:
            return self._error(400, "unknown_parameter", parameter=retired)

        allowed = {"from", "to", "trail_colour", "max_duration_hours", price_field}
        for key in params:
            if key not in allowed:
                return self._error(400, "unknown_parameter", parameter=key)

        # Default budget. 5000 zloty in 2.0; the same amount as 500000 grosze in 2.1.
        default_budget = 500000 if VERSION >= "2.1" else 5000
        raw = params.get(price_field, default_budget)
        try:
            budget = int(raw) if VERSION >= "2.1" else float(raw)
        except ValueError:
            return self._error(400, "invalid_parameter", parameter=price_field)

        budget_minor = budget if VERSION >= "2.1" else budget * 100

        trips = load("trips.json")["trips"]
        results = [t for t in trips if t["price_minor"] <= budget_minor]

        if "from" in params:
            results = [t for t in results if t["from"].lower() == params["from"].lower()]
        if "to" in params:
            results = [t for t in results if t["to"].lower() == params["to"].lower()]
        if "trail_colour" in params:
            results = [t for t in results if t["trail_colour"] == params["trail_colour"]]
        if "max_duration_hours" in params:
            limit = float(params["max_duration_hours"])
            results = [t for t in results if t["duration_hours"] <= limit]

        return self._send(200, {"count": len(results), "trips": results})

    # ----------------------------------------------------------------- POST
    def do_POST(self):
        url = urlparse(self.path)
        length = int(self.headers.get("Content-Length", 0))
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
        except json.JSONDecodeError:
            return self._error(400, "invalid_json")

        if url.path != "/bookings":
            return self._error(404, "not_found", path=url.path)

        if "trip_id" not in body:
            return self._error(400, "missing_parameter", parameter="trip_id")

        travellers = body.get("travellers", 1)
        if not isinstance(travellers, int) or travellers < 1:
            return self._error(400, "invalid_parameter", parameter="travellers")

        trips = {t["id"]: t for t in load("trips.json")["trips"]}
        trip = trips.get(body["trip_id"])
        if trip is None:
            return self._error(404, "trip_not_found", trip_id=body["trip_id"])

        # Group discount: 10% for six or more travellers.
        total = trip["price_minor"] * travellers
        if travellers >= 6:
            total = int(total * 0.9)

        return self._send(201, {
            "booking_id": "bkg_" + re.sub(r"\W", "", trip["id"])[:8],
            "trip_id": trip["id"],
            "travellers": travellers,
            "total_minor": total,
            "currency": "PLN",
            "status": "confirmed",
        })


if __name__ == "__main__":
    print(f"Szlak mock API v{VERSION} listening on http://127.0.0.1:{PORT}")
    HTTPServer(("127.0.0.1", PORT), SzlakHandler).serve_forever()
