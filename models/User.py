from sqlalchemy import Column, Integer, String, select

from models.database import Base, AsyncSessionLocal


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    vendor = Column(String, nullable=False)
    token = Column(String, nullable=False)
    profile = Column(String, nullable=False)


async def create_or_update_user(vendor: str, token: str, profile: str, name: str, email: str):
    async with AsyncSessionLocal() as session:
        query = select(User).filter_by(vendor=vendor, token=token)
        result = await session.execute(query)
        user = result.scalars().first()

        if user:
            user.profile = profile
            user.name = name
            user.email = email
        else:
            user = User(vendor=vendor, token=token, profile=profile, name=name, email=email)
            await session.add(user)

        userdict = {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "profile": user.profile,
            "vendor": user.vendor,
            "token": user.token,
        }

        await session.commit()

        return userdict
