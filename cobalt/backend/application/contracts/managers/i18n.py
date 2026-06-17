#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from abc import ABC, abstractmethod

from domain.enums import LanguageEnum


class AbstractI18nManager(ABC):
    """
    Abstract i18n service.
    """

    @abstractmethod
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
        ...

    @abstractmethod
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
        ...

    @abstractmethod
    def get_default_language(self) -> LanguageEnum:
        """
        Returns the default language.

        Parameters:
        - None.

        Returns:
        - LanguageEnum: Default language.
        """
        ...