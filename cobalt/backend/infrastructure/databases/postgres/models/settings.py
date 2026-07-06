#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy import Column, Integer, ForeignKey, Enum, event
from sqlalchemy.orm import relationship

from domain.enums import (
    LanguageEnum,
    ThemeEnum,
    TimezoneEnum
)
from infrastructure.databases.postgres.models import BaseModel


class SettingsModel(BaseModel):
    __tablename__ = "users_settings"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, unique=True)
    language = Column(Enum(LanguageEnum), nullable=False, default=LanguageEnum.EN)
    theme = Column(Enum(ThemeEnum), nullable=False, default=ThemeEnum.DARK)
    timezone = Column(Enum(TimezoneEnum), nullable=False, default=TimezoneEnum.UTC)

    user = relationship(
        "UserModel",
        back_populates="settings",
        lazy="raise"
    )

@event.listens_for(SettingsModel, "before_delete")
def prevent_direct_settings_delete(mapper, connection, target):
    raise PermissionError("Settings can only be deleted via user deletion (CASCADE)")