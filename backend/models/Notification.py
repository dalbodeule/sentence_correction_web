from sqlalchemy import select, desc, func

from backend.models.database import AsyncSessionLocal, Notification


async def get_latest_notification():
    async with AsyncSessionLocal() as session:
        query = select(Notification).order_by(desc(Notification.id)).limit(1)
        notifications = await session.execute(query)

        return notifications.scalars().all()


async def get_notifications(page_no: int, entries=50):
    async with AsyncSessionLocal() as session:
        offset = (page_no - 1) * entries
        query = select(Notification).order_by(desc(Notification.created_at)).offset(offset).limit(50)
        results = await session.execute(query)

        return results.scalars().all()


async def get_total_notification_count() -> int:
    async with AsyncSessionLocal() as session:
        query = select(func.count()).select_from(Notification)
        result = await session.execute(query)
        total_count = result.scalar()
        return total_count
