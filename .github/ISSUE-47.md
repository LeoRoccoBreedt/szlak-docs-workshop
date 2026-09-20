# #47 — Breaking: `max_price` renamed and switched to minor units

**Labels:** `docs`, `breaking-change`, `v2.1`
**Milestone:** v2.1
**Assignee:** @docs

---

Billing is standardising on minor units across every service. The `max_price`
parameter on `GET /search` becomes `max_price_minor` and now takes **grosze**
rather than **złoty**.

| | v2.0 | v2.1 |
| --- | --- | --- |
| Name | `max_price` | `max_price_minor` |
| Type | number | integer |
| Unit | złoty | grosze |
| Default | `5000` | `500000` |

The default is unchanged in real terms: 5000 złoty is 500000 grosze.

The old parameter returns `400 unknown_parameter` from v2.1 onwards. There is no
deprecation window — this was flagged in the v2.0 release notes.

## What needs doing

- [ ] Update every page that mentions `max_price`
- [ ] Update the code samples and confirm they still run
- [ ] Check `redirects.yaml` for stale anchors
- [ ] Confirm `./build.sh` and `./samples/run_samples.sh` both pass

## Testing against v2.1

The mock API serves v2.0 by default. To reproduce the new behaviour:

```
SZLAK_API_VERSION=2.1 ./samples/run_samples.sh
```

/cc @docs
