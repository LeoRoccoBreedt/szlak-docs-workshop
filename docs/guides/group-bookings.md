# Group bookings

Groups of six or more travellers receive a 10% discount, applied by the API at
booking time.

## Finding a trip within budget

Search with a per-person budget, then book the whole group in one request:

```python
import json
import urllib.parse
import urllib.request

BASE = "http://127.0.0.1:8420"

GROUP_SIZE = 8
BUDGET_PER_PERSON = 250


def search(**params):
    query = urllib.parse.urlencode(params)
    with urllib.request.urlopen(f"{BASE}/search?{query}") as response:
        return json.load(response)


result = search(max_price=BUDGET_PER_PERSON, max_duration_hours=6)
trip = result["trips"][0]
print(f"Selected: {trip['from']} -> {trip['to']}")
```

Pass the selected `trip_id` to [`POST /bookings`](../api/bookings.md) with
`travellers` set to the group size.

## What the discount applies to

The discount applies to the trip price multiplied by the number of travellers.
It does not apply to seasonal surcharges.

| Travellers | Discount |
| --- | --- |
| 1-5 | None |
| 6 or more | 10% |
