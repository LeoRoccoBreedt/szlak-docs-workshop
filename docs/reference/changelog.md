# Changelog

## v2.0

- Itinerary legs now report `delayed` with `delay_hours` and `delay_reason`
- `POST /bookings` applies the group discount server-side
- Unrecognised query parameters return `400 unknown_parameter` rather than being
  ignored

## v1.4

- Added `trail_colour` filtering on `GET /search`
- Added the Poznań to Biskupin and Łódź to Spała routes

## v1.3

- All monetary values moved to minor units. `price` became `price_minor`
