from datetime import time

from sqlalchemy import (
    CheckConstraint,
    Enum as SAEnum,
    ForeignKey,
    String,
    Time,
    UniqueConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities.business import WeekDay
from app.infrastructure.persistence.database import Base

class Business(Base):
    __tablename__ = "business"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(225), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    schedules: Mapped[list["BusinessSchedule"]] = relationship(
        back_populates="business",
        cascade="all, delete-orphan",
    )
    policies: Mapped[list["BusinessPolicy"]] = relationship(
        back_populates="business",
        cascade="all, delete-orphan",
    )
    trainers: Mapped[list["Trainer"]] = relationship(
        back_populates="business",
        cascade="all, delete-orphan",
    )
    products: Mapped[list["Product"]] = relationship(
        back_populates="business",
        cascade="all, delete-orphan",
    )
    membership_plans: Mapped[list["MembershipPlan"]] = relationship(
        back_populates="business",
        cascade="all, delete-orphan",
    )

    __table_args__ = (
        CheckConstraint("TRIM(name) <> ''", name="check_business_name"),
    )


class BusinessSchedule(Base):
    __tablename__ = "business_schedules"

    id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(ForeignKey("business.id"))

    day: Mapped[WeekDay] = mapped_column(
        SAEnum(
            WeekDay,
            name="weekday",
            values_callable=lambda enum: [day.value for day in enum],
        ),
        nullable=False,
    )

    business: Mapped["Business"] = relationship(
        back_populates="schedules"
    )

    intervals: Mapped[list["BusinessHourInterval"]] = relationship(
        back_populates="schedule",
        cascade="all, delete-orphan"
    )

    __table_args__ = (
        UniqueConstraint("business_id", "day", name="uq_business_schedule_day"),
    )


class BusinessHourInterval(Base):
    __tablename__ = "business_hour_intervals"

    id: Mapped[int] = mapped_column(primary_key=True)

    schedule_id: Mapped[int] = mapped_column(
        ForeignKey("business_schedules.id"),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    opens_at: Mapped[time] = mapped_column(Time, nullable=False)
    closes_at: Mapped[time] = mapped_column(Time, nullable=False)

    schedule: Mapped["BusinessSchedule"] = relationship(
        back_populates="intervals"
    )

    __table_args__ = (
        CheckConstraint("opens_at < closes_at", name="check_business_hour_interval"),
    )