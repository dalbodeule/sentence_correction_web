from datetime import datetime

from sqlalchemy import select

from backend.models.database import AsyncSessionLocal, Base, User


async def create_or_update_user(vendor: str, token: str, profile: str, name: str, email: str):
    async with AsyncSessionLocal() as session:
        query = select(User).filter_by(vendor=vendor, token=token)
        result = await session.execute(query)
        user = result.scalars().first()

        if user:
            user.profile = profile
            user.name = name
            user.email = email
            user.last_login = datetime.now()
        else:
            user = User(vendor=vendor, token=token, profile=profile, name=name, email=email)
            session.add(user)
        await session.commit()
        await session.refresh(user)

        userdict = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "profile": user.profile,
            "vendor": user.vendor,
            "token": user.token,
        }

        return userdict
