from sqlalchemy import Boolean, CheckConstraint, ForeignKey, JSON, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.persistence.database import Base


class Trainer(Base):
    __tablename__ = "trainers"

    id: Mapped[int] = mapped_column(primary_key=True)
    business_id: Mapped[int] = mapped_column(
        ForeignKey("business.id"),
        nullable=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(String(255), nullable=True)
    specialties: Mapped[list[str] | None] = mapped_column(
        JSON,
        nullable=True,
        default=None,
    )
    available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    business: Mapped["Business"] = relationship(back_populates="trainers")

    __table_args__ = (
        CheckConstraint("TRIM(name) <> ''", name="check_trainer_name"),
        CheckConstraint(
            "description IS NULL OR TRIM(description) <> ''",
            name="check_trainer_description",
        ),
    )