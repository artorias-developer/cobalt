# Testing

This guide explains how to run Cobalt's end-to-end (E2E) test suite locally.

## Requirements

#### Operating system

The following operating systems are supported. Other distributions are not officially supported and may not work or may require manual adjustments to the installer.

| OS     | Supported versions      |
|--------|-------------------------|
| Ubuntu | 22.04 LTS or newer      |
| Debian | 13 (Trixie) or newer    |

---

#### npm 

Required for installing Playwright.

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

## Quick start

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

4. Fill in the `.env` file with your current login credentials and the link from your dashboard.

5. Run all E2E tests:

```bash
npm run test:e2e
```
