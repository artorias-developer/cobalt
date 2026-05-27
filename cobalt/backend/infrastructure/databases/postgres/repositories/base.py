#  Copyright (C) 2026 ArtoriasCode
#  Author: ArtoriasCode
#  Repository: https://github.com/ArtoriasCode/cobalt
#  SPDX-License-Identifier: AGPL-3.0-or-later

from contextlib import asynccontextmanager
from math import ceil
from re import compile
from typing import Tuple, Sequence, Dict, Optional, AsyncGenerator

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.exc import IntegrityError


class BaseRepository:
    """
    Base repository for all Postgres repositories.
    """
    REGEX_DETAIL_KEY = compile(r"DETAIL:\s*Key \((.*?)\)=\((.*?)\)")

    session_factory: async_sessionmaker

    def __init__(
        self,
        session_factory: async_sessionmaker
    ):
        self.session_factory = session_factory

    @asynccontextmanager
    async def _get_session(
        self,
        session: Optional[AsyncSession] = None
    ) -> AsyncGenerator[AsyncSession, None]:
        """
        Returns an existing session or creates a new one.

        Parameters:
        - session: AsyncSession object.

        Yields:
        - AsyncSession: AsyncSession instance.
        """
        if session is not None:
            yield session
        else:
            async with self.session_factory() as session:
                yield session

    @staticmethod
    async def paginate(
        session: AsyncSession,
        stmt,
        page: int,
        limit: int = 10
    ) -> Tuple[Sequence, int, int, int]:
        """
        Applies pagination to a SQLAlchemy select statement.

        Returns:
        - Tuple: List of records, total count, current page, total pages.
        """
        count_stmt = select(
            func.count()
        ).select_from(
            stmt.order_by(None).subquery()
        )

        count_result = await session.execute(count_stmt)

        total = count_result.scalar() or 0
        offset = (page - 1) * limit

        stmt = stmt.limit(
            limit
        ).offset(
            offset
        )

        result = await session.execute(stmt)

        items = result.scalars().all()
        pages = ceil(total / limit) if total else 0

        return items, total, page, pages

    def parse_asyncpg_detail_to_dict(
        self,
        e: IntegrityError
    ) -> Dict[str, str]:
        """
        Extracts key=value pairs from the asyncpg error DETAIL.

        Parameters:
        - e: IntegrityError object.

        Returns:
        - Dict: Dictionary of key value pairs.
        """
        message = e.orig.args[0] if hasattr(e, "orig") and e.orig.args else str(e)
        match = self.REGEX_DETAIL_KEY.search(message)

        if match:
            keys = match.group(1).split(", ")
            values = match.group(2).split(", ")

            return dict(zip(keys, values))

        return {}
