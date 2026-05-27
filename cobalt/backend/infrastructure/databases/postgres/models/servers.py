#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy import Column, Integer, String, ForeignKey, Enum
from sqlalchemy.orm import relationship

from domain.enums import ServerStatusEnum
from infrastructure.databases.postgres.models import BaseModel


class ServerModel(BaseModel):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False)
    loader_id = Column(Integer, ForeignKey("games_loaders.id", ondelete="RESTRICT"), nullable=False)
    version = Column(String(16), nullable=False)
    status = Column(Enum(ServerStatusEnum), nullable=False, default=ServerStatusEnum.PENDING)

    game = relationship(
        "GameModel",
        back_populates="servers",
        lazy="raise"
    )

    loader = relationship(
        "LoaderModel",
        lazy="raise"
    )

    attributes = relationship(
        "AttributeModel",
        back_populates="server",
        lazy="raise",
        cascade="all, delete-orphan"
    )