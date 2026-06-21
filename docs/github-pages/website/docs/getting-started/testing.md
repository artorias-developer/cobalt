# Testing

This guide explains how to run Cobalt's end-to-end (E2E) test suite locally.

::: warning
Make sure the dashboard and all required containers are running before executing tests.
:::

1. Navigate to the tests directory:

```bash
cd tests
```

2. Install dependencies:

```bash
npm install
```

3. Create your `.env` file from the example:

```bash
cp .env.example .env
```

4. Run all E2E tests:

```bash
npm run test:e2e
```
