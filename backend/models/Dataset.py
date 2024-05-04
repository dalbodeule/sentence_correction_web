from sqlalchemy import select, desc, func
from sqlalchemy.orm import joinedload

from backend.models.database import AsyncSessionLocal, Dataset, DatasetStatus


async def get_datasets(page_no: int, entries=50):
    async with AsyncSessionLocal() as session:
        offset = (page_no - 1) * entries
        query = select(Dataset).options(joinedload(Dataset.user)).order_by(desc(Dataset.created_at)).offset(offset).limit(50)
        results = await session.execute(query)

        return results.scalars().all()


async def create_dataset(uid: int, text: str, corrected: str, memo: str):
    async with AsyncSessionLocal() as session:
        session.add(Dataset(user_id=uid, text=text, corrected=corrected, memo=memo))
        await session.commit()

        return True


async def update_dataset(id: int, status: DatasetStatus, text: str, corrected: str, memo: str):
    async with AsyncSessionLocal() as session:
        query = select(Dataset).options(joinedload(Dataset.user)).filter_by(id=id)
        results = await session.execute(query)
        result = results.scalar()

        if result is None:
            raise Exception("Dataset not found")

        result.status = status
        result.memo = memo

        await session.commit()
        await session.refresh(result)

        return result


async def get_total_datasets_count() -> int:
    async with AsyncSessionLocal() as session:
        query = select(func.count()).select_from(Dataset)
        result = await session.execute(query)
        total_count = result.scalar()
        return total_count
