# Pricing

Every monetary value returned by the Szlak API is expressed in **minor units**:
grosze, not złoty. One złoty is one hundred grosze.

A trip costing 249.00 PLN is returned as:

```
"price_minor": 24900
```

Divide by 100 when you display a price to a traveller. Do not round before
dividing.

## Why minor units

Floating-point arithmetic on decimal currency introduces rounding errors that
accumulate across a multi-leg itinerary. Integer grosze avoid the problem
entirely. Every Szlak service handles money this way.

## Budgets in search

The `max_price` parameter on [`GET /search`](../api/search.md) filters trips by
price. The default `max_price` is 5000, i.e. trips up to 5000 PLN.

Raise it for the longer routes. The Warszawa to Białowieża trip is the most
expensive in the catalogue at 320.00 PLN.

## Group totals

The `total_minor` field on a booking is the full amount for the group, after any
group discount. See [group bookings](group-bookings.md).
