/*
 * Copyright (C) 2026 Artorias
 * Author: Artorias
 * Repository: https://github.com/artorias-developer/cobalt
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

import { createI18n } from "vue-i18n"

import { LanguageEnum } from "@/types"

import en from "@/locales/en.json"
import uk from "@/locales/uk.json"
import ru from "@/locales/ru.json"

type MessageSchema = typeof en

/**
 * Creates and configures the vue-i18n instance with support for
 * English and Ukrainian locales, including Ukrainian plural rules.
 *
 * Parameters:
 * - null.
 *
 * Returns:
 * - I18n: Configured i18n instance ready to be used with app.use().
 */
export function setupI18n() {
  return createI18n<[MessageSchema], LanguageEnum>({
    legacy: false,
    locale: LanguageEnum.EN,
    fallbackLocale: LanguageEnum.EN,
    pluralRules: {
      [LanguageEnum.UK]: (n: number): number => {
        if (n === 0) return 0
        if (n % 10 === 1 && n % 100 !== 11) return 1
        if (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20)) return 2
        return 3
      },
      [LanguageEnum.RU]: (n: number): number => {
        if (n === 0) return 0
        if (n % 10 === 1 && n % 100 !== 11) return 1
        if (n % 10 >= 2 && n % 10 <= 4 && (n % 100 < 10 || n % 100 >= 20)) return 2
        return 3
      },
    },
    messages: { en, uk, ru },
  })
}