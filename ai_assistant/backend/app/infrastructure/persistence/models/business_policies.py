from sqlalchemy import Boolean, CheckConstraint, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.database import Base


class BusinessPolicy(Base):
    __tablename__ = "business_policies"

    id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(
        ForeignKey("business.id"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=False)
    active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    business: Mapped["Business"] = relationship(back_populates="policies")

    __table_args__ = (
        CheckConstraint("TRIM(title) <> ''", name="check_business_policy_title"),
        CheckConstraint(
            "TRIM(description) <> ''",
            name="check_business_policy_description",
        ),
    )