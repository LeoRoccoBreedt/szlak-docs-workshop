# GET /search

Returns trips matching the supplied filters. All parameters are optional; an
empty query returns every trip within the default budget.

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `from` | string | No | - | Departure city. Matched case-insensitively |
| `to` | string | No | - | Destination city |
| `trail_colour` | string | No | - | One of `czerwony`, `niebieski`, `zielony`, `żółty`, `czarny` |
| `max_duration_hours` | number | No | - | Upper bound on trip duration |
| `max_price` | number | No | 5000 | Maximum trip price in PLN |

## Response

```
{
  "count": 1,
  "trips": [
    {
      "id": "krk-zak-001",
      "from": "Kraków",
      "to": "Zakopane",
      "trail_colour": "czerwony",
      "duration_hours": 7.5,
      "difficulty": "moderate",
      "season": "May-October",
      "price_minor": 24900,
      "stops": ["Chochołowska valley", "oscypek stand at Kiry"],
      "summary": "The classic Tatra approach."
    }
  ]
}
```

## Example

<!-- include: samples/search_trips.py -->

## Errors

An unrecognised parameter returns `400 unknown_parameter`. See
[errors](errors.md) for the full list.
