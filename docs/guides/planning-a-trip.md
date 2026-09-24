# Planning a trip

A complete trip goes through three stages: search, book, then track.

## 1. Search

Narrow by trail colour and duration before you filter on price. Most travellers
know which trail they want before they know what they want to spend.

<!-- include: samples/search_trips.py -->

![Trail waymarking on the Chochołowska approach](../img/waymark.png)
*The red waymark above Kiry. Trips on this route are filtered with
trail_colour=czerwony and priced with `max_price` in złoty.*

## 2. Book

Pass the `id` from the search response to [`POST /bookings`](../api/bookings.md).
Groups of six or more are discounted automatically.

<!-- include: samples/book_trip.py -->

## 3. Track

Poll [`GET /itineraries`](../api/itineraries.md) while the trip is under way.
Legs above the treeline on the Tatra and Karkonosze routes are the ones most
likely to report `delayed`.

<!-- include: samples/list_itineraries.py -->

## Seasonal closures

The Kraków to Zakopane and Wrocław to Karpacz routes close in winter. The
`season` field on each trip gives the months it operates.
