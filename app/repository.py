from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Optional, Type, TypeVar

from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.models import Base

T = TypeVar("T", bound=Base)


class AbstractRepository(ABC, Generic[T]):
    @abstractmethod
    def __init__(self, session: Callable[[], AsyncSession], model: Type[T]) -> None:
        raise NotImplementedError

    @abstractmethod
    async def find_one(self, id: int) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def find_all(self, filter_by: Optional[Any]) -> list[Any]:
        raise NotImplementedError

    @abstractmethod
    async def add_one(self, data: dict[Any, Any]) -> int:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, id: int, data: dict[Any, Any]) -> T | None:
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, id: int) -> int:
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository[T]):
    def __init__(
        self, session: async_sessionmaker[AsyncSession], model: Type[T]
    ) -> None:
        self.session: AsyncSession = session()
        self.model = model

    async def find_one(self, id: int) -> T | None:
        stmt = select(self.model).filter_by(id=id)
        res = await self.session.execute(stmt)
        row = res.scalar_one_or_none()
        await self.session.close_all()
        return row

    async def get_id_by_username(self, username: str) -> int | None:
        stmt = select(self.model).filter_by(username=username)
        res = await self.session.execute(stmt)
        row = res.scalar_one_or_none()
        if row is None:
            return None
        await self.session.close_all()
        return row.id

    async def find_all(
        self,
        filter_by: Optional[Any] = None,
        join_by: Optional[tuple[Any, Any, Any]] = None,
    ) -> list[T]:
        stmt = select(self.model)
        if join_by:
            stmt = select(self.model, join_by[1])
            stmt = stmt.select_from(join_by[0]).join(*join_by[1:])
        if filter_by is not None:
            stmt = stmt.where(filter_by)

        result = await self.session.execute(stmt)
        res = [row[0] for row in result.all()]
        await self.session.close_all()
        return res

    async def add_one(self, data: dict[str, Any]) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        res = await self.session.execute(stmt)
        await self.session.commit()
        await self.session.close_all()
        return res.scalar_one()

    async def update_one(self, id: int, data: dict[str, Any]) -> T | None:
        stmt = (
            update(self.model)
            .values(**data)
            .where(self.model.id == id)
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        await self.session.commit()
        await self.session.close_all()
        return res.scalar_one_or_none()

    async def delete_one(self, id: int) -> int:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model.id)
        res = await self.session.execute(stmt)
        await self.session.commit()
        await self.session.close_all()
        return res.scalar_one()
