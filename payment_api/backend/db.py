from sqlalchemy.ext.asyncio import (
    create_async_engine, async_sessionmaker, AsyncSession)
from sqlalchemy.orm import DeclarativeBase


async_engine = create_async_engine(
    'Вставьте адресс своей базы',
    echo=True)

async_session_maker = async_sessionmaker(
    async_engine, expire_on_commit=False, class_=AsyncSession)


class Base(DeclarativeBase):
    ...
