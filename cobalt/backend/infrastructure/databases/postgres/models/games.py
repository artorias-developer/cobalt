#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from infrastructure.databases.postgres.models import BaseModel


class GameModel(BaseModel):
    __tablename__ = "games"

    id = Column(Integer, primary_key=True)
    name = Column(String(32), nullable=False)

    servers = relationship(
        "ServerModel",
        back_populates="game",
        lazy="raise",
        cascade="all, delete-orphan"
    )

    loaders = relationship(
        "LoaderModel",
        back_populates="game",
        lazy="raise",
        cascade="all, delete-orphan"
    )