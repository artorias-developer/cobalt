#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy import Column, Integer, String, Enum, ARRAY
from sqlalchemy.orm import relationship

from domain.enums import PermissionEnum
from infrastructure.databases.postgres.models import BaseModel


class RoleModel(BaseModel):
    __tablename__ = "users_roles"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True, nullable=False)
    permissions = Column(ARRAY(Enum(PermissionEnum)), nullable=False, default=list)

    users = relationship(
        "UserModel",
        back_populates="role",
        lazy="raise"
    )