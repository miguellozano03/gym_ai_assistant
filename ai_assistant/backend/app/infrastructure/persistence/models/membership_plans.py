from decimal import Decimal

from sqlalchemy import CheckConstraint, ForeignKey, Integer, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.database import Base


class MembershipPlan(Base):
    __tablename__ = "membership_plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(
        ForeignKey("business.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(), nullable=False)
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)

    business: Mapped["Business"] = relationship(back_populates="membership_plans")

    __table_args__ = (
        CheckConstraint("TRIM(name) <> ''", name="check_membership_plan_name"),
        CheckConstraint("price >= 0", name="check_membership_plan_price"),
        CheckConstraint(
            "duration_days > 0",
            name="check_membership_plan_duration",
        ),
    )
