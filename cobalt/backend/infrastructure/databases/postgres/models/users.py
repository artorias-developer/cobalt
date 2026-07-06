#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from infrastructure.databases.postgres.models import BaseModel


class UserModel(BaseModel):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String(32), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    salt = Column(String(128), nullable=False)
    role_id = Column(Integer, ForeignKey("users_roles.id"), nullable=False)

    role = relationship(
        "RoleModel",
        back_populates="users",
        lazy="raise"
    )

    settings = relationship(
        "SettingsModel",
        back_populates="user",
        lazy="raise",
        uselist=False
    )