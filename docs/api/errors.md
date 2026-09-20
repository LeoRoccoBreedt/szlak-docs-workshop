# Errors

Every error response carries an `error` field and, where relevant, the parameter
that caused it.

| Status | Code | Meaning |
| --- | --- | --- |
| 400 | `unknown_parameter` | A parameter not recognised by this API version |
| 400 | `invalid_parameter` | Recognised parameter, unusable value |
| 400 | `missing_parameter` | A required parameter was absent |
| 400 | `invalid_json` | Request body could not be parsed |
| 404 | `trip_not_found` | No trip matches the supplied `trip_id` |
| 404 | `not_found` | No such endpoint |

## Unknown parameters

The API rejects parameters it does not recognise rather than ignoring them. A
parameter removed in a major version returns `unknown_parameter` from the
release onwards, with no deprecation window.

```
{
  "error": "unknown_parameter",
  "parameter": "max_price"
}
```

Check the [changelog](../reference/changelog.md) when you see this.
