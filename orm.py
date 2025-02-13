import uuid
from datetime import datetime, timedelta
from models import Base
from database import engine, new_session
from models import UserModels, ReferralCode, ReferrersModels
from passlib.context import CryptContext
from sqlalchemy import select
from schemas import UserSchema

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def create_user(new_user: UserSchema) -> None:
    async with new_session() as session:
        user = UserModels(
            email = new_user.email,
            hashed_password = await get_password_hash(new_user.password),
        )
        session.add(user)
        await session.flush()
        code = new_user.referral_code
        stmt = select(ReferralCode).filter(ReferralCode.code == code)
        result = await session.execute(stmt)
        code = result.scalar_one_or_none()

        if code:
            user.referral_code_id = code.id
            new_referrer_info = ReferrersModels(
                referrer = code.owner_id,
                referral = user.id
            )
            session.add(new_referrer_info)
            await session.delete(code)

        await session.commit()

async def generate_referral_code() -> str:
    return str(uuid.uuid4()).replace("-", "")[:10]

async def set_referral_code(user_id: int) -> str:
    async with new_session() as session:
        code = await generate_referral_code()
        new_code = ReferralCode(
            code = code,
            owner_id = user_id,
            expiration_date = datetime.now() + timedelta(days=30)
        )
        session.add(new_code)

        await session.commit()
        return code

async def get_referral_code(user_id: int) -> str | None:
    async with new_session() as session:
        stmt = select(ReferralCode).filter(ReferralCode.owner_id == user_id)
        result = await session.execute(stmt)
        code = result.scalar_one_or_none()
        if code and code.expiration_date < datetime.now():
            await session.delete(code)
            return None

        return code

async def get_user_by_email(email: str):
    async with new_session() as session:
        stmt = select(UserModels).filter(UserModels.email == email)
        result = await session.execute(stmt)

        return result.scalar_one_or_none()

async def get_referrer_by_email(email: str) -> str | None:
    async with new_session() as session:
        stmt = (
            select(ReferralCode.code)
            .join(UserModels, ReferralCode.owner_id == UserModels.id)
            .where(UserModels.email == email)
        )
        result = await session.execute(stmt)
        referrer_code = result.scalar()
        return referrer_code


async def get_referrals(referrer_id: int) -> list | None:
    async with new_session() as session:
        result = await session.execute(
            select(UserModels)
            .join(ReferrersModels, UserModels.id == ReferrersModels.referral)
            .where(ReferrersModels.referrer == referrer_id)
        )
        referrals = result.scalars().all()
        return referrals
