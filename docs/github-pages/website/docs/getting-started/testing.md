# Testing

This guide explains how to run Cobalt's end-to-end (E2E) test suite locally.

## Requirements

#### Operating system

Ubuntu 22.04 LTS or newer, or macOS. Other distributions are not officially supported and may require manual adjustments to the installer.

---

#### npm 

Required for installing Playwright.

::: code-group
```bash [Ubuntu]
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.8/install.sh | bash
\. "$HOME/.nvm/nvm.sh"
nvm install 24
```

```bash [macOS]
brew install node
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
