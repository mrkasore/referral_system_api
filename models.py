from sqlalchemy import Column, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey
from typing import Optional

class Base(DeclarativeBase):
    pass

class UserModels(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str]
    referral_code_id: Mapped[Optional[int]] = mapped_column(ForeignKey("referral_codes.id"), nullable=True)

class ReferralCode(Base):
    __tablename__ = "referral_codes"

    id: Mapped[int] = mapped_column(primary_key=True)
    code: Mapped[str] = mapped_column(unique=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    expiration_date = Column(DateTime(timezone=True))

class ReferrersModels(Base):
    __tablename__ = "referrers_info"

    id: Mapped[int] = mapped_column(primary_key=True)
    referrer: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    referral: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))