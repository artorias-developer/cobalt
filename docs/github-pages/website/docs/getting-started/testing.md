# Testing

This guide explains how to run Cobalt's test suites locally:

- **Unit tests** - backend tests written with [pytest](https://docs.pytest.org/). They don't need running containers.
- **E2E tests** - end-to-end dashboard tests written with [Playwright](https://playwright.dev/). They run against a live dashboard.

All tests live in the `tests` directory of the repository.

## Requirements

#### Operating system

The following operating systems are supported. Other distributions are not officially supported and may not work or may require manual adjustments to the installer.

| Operating system | Supported versions      |
|------------------|-------------------------|
| Ubuntu           | 22.04 LTS or newer      |
| Debian           | 13 (Trixie) or newer    |

---

#### make

Used to run the test commands.

::: code-group
```bash [Ubuntu]
apt install make
```

```bash [Debian]
apt install make
```
:::

---

#### uv

Required for installing Python 3.12 and the backend dependencies used by the unit tests.

::: code-group
```bash [Ubuntu]
curl -LsSf https://astral.sh/uv/install.sh | sh
```

```bash [Debian]
curl -LsSf https://astral.sh/uv/install.sh | sh
```
:::

---

#### npm

Required for installing Playwright for the E2E tests.

::: code-group
```bash [Ubuntu]
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.8/install.sh | bash
\. "$HOME/.nvm/nvm.sh"
nvm install 24
```

```bash [Debian]
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.8/install.sh | bash
\. "$HOME/.nvm/nvm.sh"
nvm install 24
```
:::

## Unit tests

1. Navigate to the backend directory:

```bash
cd cobalt/backend
```

2. Install the backend dependencies, including the dev group with `pytest` and `pytest-asyncio`:

```bash
uv sync
```

3. Activate the virtual environment:

```bash
source .venv/bin/activate
```

4. Go back to the project root and run all unit tests:

```bash
cd ../..
make tests-unit
```

::: tip
To run a single file or test, call pytest directly from the `tests` directory:

```bash
cd tests
python -m pytest unit/services/test_auth_service.py
python -m pytest -k "login"
```
:::

## E2E tests

::: warning
Make sure the dashboard and all required containers are running before executing E2E tests.
:::

1. Navigate to the tests directory:

```bash
cd tests
```

2. Install dependencies and the Playwright browsers:

```bash
npm install
npx playwright install --with-deps
```

3. Create your `.env` file from the example:

```bash
cp .env.example .env
```

4. Fill in the `.env` file with your current login credentials and the link from your dashboard.

5. Go back to the project root and run all E2E tests:

```bash
cd ..
make tests-e2e
```

::: tip
Additional Playwright modes are available from the `tests` directory:

```bash
# Interactive UI mode
npm run test:ui

# Run with a visible browser
npm run test:headed

# Step-by-step debugging
npm run test:debug
```
:::

## Makefile commands

```bash
# Run the unit tests
make tests-unit

# Run the E2E tests
make tests-e2e
```

::: tip
Short aliases are also available, e.g. `make t:u`, `make t:e`.
:::
