# GET /itineraries

Returns every itinerary for the authenticated account, including the status of
each leg.

## Parameters

This endpoint takes no parameters.

## Leg status values

| Value | Meaning |
| --- | --- |
| scheduled | Not yet started |
| complete | Finished |
| delayed | Held up. Includes delay_hours and delay_reason |

A delayed leg carries a human-readable delay_reason. Weather closures on the
Tatra and Karkonosze routes are the most common cause.

## Example

<!-- include: samples/list_itineraries.py -->
