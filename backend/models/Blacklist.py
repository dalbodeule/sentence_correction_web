from datetime import datetime, timedelta
from sqlalchemy import select

from backend.models.database import AsyncSessionLocal, Blacklist


async def find_blacklist(token: str) -> bool:
    async with AsyncSessionLocal() as session:
        query = select(Blacklist).filter_by(token=token)
        result = await session.execute(query)
        token = result.scalars().first()

        if token:
            return True
        return False


async def add_blacklist(token: str) -> bool:
    async with AsyncSessionLocal() as session:
        blacklist = Blacklist(token=token, datetime=datetime.now() + timedelta(days=1))
        session.add(blacklist)

        await session.commit()

    return True


async def delete_blacklist() -> bool:
    async with AsyncSessionLocal() as session:
        query = select(Blacklist).filter(Blacklist.datetime < datetime.now())
        result = await session.execute(query)

        blacklist = result.scalars().all()
        if blacklist:
            await session.delete(blacklist)
            await session.commit()

        return True
