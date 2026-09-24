# Szlak API

Szlak plans waymarked walking routes across Poland. Search trails, book them for
a group, and track an itinerary while it is under way.

## Endpoints

| Endpoint | Purpose |
| --- | --- |
| [`GET /search`](api/search.md) | Find trips matching a trail, duration, or budget |
| [`POST /bookings`](api/bookings.md) | Book a trip for one or more travellers |
| [`GET /itineraries`](api/itineraries.md) | Retrieve itineraries and leg status |

## Getting started

New to the API? Start with the [quickstart](quickstart.md), then read
[planning a trip](guides/planning-a-trip.md).

Prices are handled in minor units. Read [pricing](guides/pricing.md) before you
write any code that deals with money.

## Trail colours

Polish trails are waymarked by colour, and Szlak uses the same values:
czerwony, niebieski, zielony, żółty, czarny.
