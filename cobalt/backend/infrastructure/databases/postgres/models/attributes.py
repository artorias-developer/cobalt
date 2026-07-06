#  Copyright (C) 2026 Artorias
#  Author: Artorias
#  Repository: https://github.com/artorias-developer/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from sqlalchemy import Column, Integer, String, ForeignKey, Text, UniqueConstraint
from sqlalchemy.orm import relationship

from infrastructure.databases.postgres.models import BaseModel


class AttributeModel(BaseModel):
    __tablename__ = "servers_attributes"
    __table_args__ = (
        UniqueConstraint("server_id", "key", name="uq_server_id_key"),
    )

    id = Column(Integer, primary_key=True)
    server_id = Column(Integer, ForeignKey("servers.id", ondelete="CASCADE"), nullable=False)
    key = Column(String(64), nullable=False)
    value = Column(Text, nullable=False)

    server = relationship(
        "ServerModel",
        back_populates="attributes",
        lazy="raise"
    )