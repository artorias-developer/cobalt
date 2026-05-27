#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB

from infrastructure.databases.postgres.models import BaseModel


class LoaderModel(BaseModel):
    __tablename__ = "games_loaders"
    __table_args__ = (
        UniqueConstraint("game_id", "name", name="uq_game_id_name"),
    )

    id = Column(Integer, primary_key=True)
    game_id = Column(Integer, ForeignKey("games.id", ondelete="CASCADE"), nullable=False)
    name = Column(String(32), nullable=False)
    versions = Column(JSONB, nullable=False)

    game = relationship(
        "GameModel",
        back_populates="loaders",
        lazy="raise"
    )