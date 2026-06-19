# Adding a language

This guide explains how to add support for a new language to Cobalt.

## Frontend

1. Make sure you start from the project root.

2. Create a new locale file in `cobalt/frontend/src/locales`, e.g. `de.json`, using one of the existing locale files (`en.json`, `uk.json`, `ru.json`) as a template.

3. Import the new locale file in the `cobalt/frontend/src/bootstrap.ts` file:

```typescript
import de from "@/locales/de.json"
```

4. Add the new locale to `setupI18n`:

```typescript
function setupI18n() {
  return createI18n<[MessageSchema], LanguageEnum>({
    legacy: false,
    locale: LanguageEnum.EN,
    fallbackLocale: LanguageEnum.EN,
    pluralRules: {
      // ...
    },
    messages: { en, uk, ru, de },
  })
}
```

5. Configure custom plural rules for the new language in `setupI18n`, if its pluralization logic differs from the default:

```typescript
pluralRules: {
  [LanguageEnum.UK]: (n: number): number => {
    if (n === 0) return 0
    if (n % 10 === 1 && n % 100 !== 11) return 1
    if (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20)) return 2
    return 3
  },
  [LanguageEnum.DE]: (n: number): number => {
    return n === 1 ? 0 : 1
  },
}
```

::: tip
If the language follows standard singular/plural rules (like English or German), you can skip this step entirely - vue-i18n's default pluralization will work out of the box.
:::

6. Add the new language to the `LanguageEnum` type in `cobalt/frontend/src/types/enums/language.ts`:

```typescript
export enum LanguageEnum {
  EN = "en",
  RU = "ru",
  UK = "uk",
  DE = "de",
}
```

7. Add the new language to the language switcher in `cobalt/frontend/src/components/widgets/blocks/SettingsBlock.vue`, so users can actually select it:

```typescript
const languageOptions: SelectOption[] = [
  {
    value: LanguageEnum.EN,
    label: t("settings.general.language.options.en")
  },
  {
    value: LanguageEnum.RU,
    label: t("settings.general.language.options.ru")
  },
  {
    value: LanguageEnum.UK,
    label: t("settings.general.language.options.uk")
  },
  {
    value: LanguageEnum.DE,
    label: t("settings.general.language.options.de")
  }
]
```

::: tip
Don't forget to add the `settings.general.language.options.de` translation key to all locale files, including the new one.
:::

## Backend

1. Make sure you start from the project root.

2. Create a new locale by initializing it with `pybabel`:

```bash
make locales-init locale=de
```

::: tip
Short alias is also available: `make l:i locale=de`.
:::

3. Run the following commands to extract and update the translation strings:

```bash
make locales-generate
make locales-update
```

::: tip
Short aliases are also available: `make l:g`, `make l:u`.
:::

4. Add translations to the generated file at `cobalt/backend/infrastructure/locales/de/LC_MESSAGES/messages.po`.

5. Compile the translations:

```bash
make locales-compile
```

::: tip
Short alias is also available: `make l:c`.
:::