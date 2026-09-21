# Szlak API Documentation

Documentation and runnable code samples for the Szlak trip-planning API.

## Layout

```
docs/        Markdown pages, built and published
samples/     Runnable code samples, included by reference into docs/
mock-api/    Local mock server so the samples can run offline
```

## Working on the docs

Install nothing. Everything here runs on the Python standard library.

### Check the docs

```
./build.sh
```

Validates internal links, checks every `<!-- include: -->` target exists, and
enforces the house writing conventions.

### Run the code samples

```
./samples/run_samples.sh
```

All four samples should pass.

## Contributing

Work on a branch, then open a pull request. Both `./build.sh` and
`./samples/run_samples.sh` must pass before review.

Code samples are the source of truth. If a sample and a page disagree, the
sample is right and the page needs fixing.
