# POST /bookings

Books a trip for one or more travellers.

## Parameters

| Name | Type | Required | Default | Description |
| --- | --- | --- | --- | --- |
| `trip_id` | string | Yes | - | Identifier returned by [`GET /search`](search.md) |
| `travellers` | integer | No | 1 | Number of travellers. Must be at least 1 |

## Group discount

Bookings of six or more travellers receive a 10% discount. The discount is
applied by the API; do not apply it yourself before sending the request.

See [group bookings](../guides/group-bookings.md) for a worked example.

## Response

```
{
  "booking_id": "bkg_tormal00",
  "trip_id": "tor-mal-005",
  "travellers": 2,
  "total_minor": 31800,
  "currency": "PLN",
  "status": "confirmed"
}
```

`total_minor` is expressed in grosze. See [pricing](../guides/pricing.md).

## Example

<!-- include: samples/book_trip.py -->
