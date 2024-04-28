from sqlalchemy import select, desc, func
from sqlalchemy.orm import joinedload

from backend.models.database import AsyncSessionLocal, Notification


async def get_latest_notification():
    async with AsyncSessionLocal() as session:
        query = select(Notification).options(joinedload(Notification.user)).order_by(desc(Notification.id)).limit(1)
        notifications = await session.execute(query)

        return notifications.scalars().all()


async def get_notifications(page_no: int, entries=50):
    async with AsyncSessionLocal() as session:
        offset = (page_no - 1) * entries
        query = select(Notification).options(joinedload(Notification.user)).order_by(
            desc(Notification.created_at)).offset(offset).limit(50)
        results = await session.execute(query)

        return results.scalars().all()


async def get_total_notification_count() -> int:
    async with AsyncSessionLocal() as session:
        query = select(func.count()).select_from(Notification)
        result = await session.execute(query)
        total_count = result.scalar()
        return total_count


async def create_or_update_notification(n_id: int, content: str, user_id: int):
    async with AsyncSessionLocal() as session:
        if n_id == 0:
            notification = None
        else:
            query = select(Notification).filter_by(id=n_id)
            result = await session.execute(query)
            notification = result.scalars().first()

        if notification:
            notification.content = content
            notification.user_id = user_id
        else:
            notification = Notification(content=content, user_id=user_id)
            session.add(notification)
        await session.commit()
        await session.refresh(notification)

        return notification
