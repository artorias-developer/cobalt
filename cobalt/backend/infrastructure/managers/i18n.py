#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from contextvars import ContextVar
from gettext import translation, NullTranslations
from pathlib import Path

from domain.enums import LanguageEnum
from application.contracts.managers import AbstractI18nManager


_translator: ContextVar[NullTranslations] = ContextVar("translator", default=NullTranslations())


class I18nManager(AbstractI18nManager):
    """
    I18n service for per-request gettext translations via ContextVar.
    """
    _locales_dir: Path
    _domain: str
    _default_language: LanguageEnum
    _cache: dict[LanguageEnum, NullTranslations]

    def __init__(
        self,
        locales_dir: Path,
        domain: str = "messages",
        default_language: LanguageEnum = LanguageEnum.UK
    ):
        self._locales_dir = locales_dir
        self._domain = domain
        self._default_language = default_language
        self._cache = {
            lang: translation(
                domain=domain,
                localedir=locales_dir,
                languages=[lang.value]
            )
            for lang in LanguageEnum
        }

    def activate(
        self,
        language: LanguageEnum
    ) -> None:
        """
        Activates translations for the current async context.

        Parameters:
        - language: LanguageEnum object.

        Returns:
        - None.
        """
        _translator.set(
            self._cache.get(language, self._cache[self._default_language])
        )

    def gettext(
        self,
        message: str
    ) -> str:
        """
        Translates a message using the current context translator.

        Parameters:
        - message: Message to translate.

        Returns:
        - str: Translated message.
        """
        return _translator.get().gettext(message)

    def get_default_language(self) -> LanguageEnum:
        """
        Returns the default language.

        Parameters:
        - None.

        Returns:
        - LanguageEnum: Default language.
        """
        return self._default_language