#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from application.contracts.managers import AbstractI18nManager
from infrastructure.managers import I18nManager
from infrastructure.configs import ApplicationConfig


def create_i18n_manager(
    config: ApplicationConfig
) -> AbstractI18nManager:
    """
    Creates the i18n service.

    Parameters:
    - config: ApplicationConfig object.

    Returns:
    - AbstractI18nManager: AbstractI18nManager object.
    """
    return I18nManager(
        locales_dir=config.i18n.locales_dir,
        domain=config.i18n.domain,
        default_language=config.i18n.default_language
    )