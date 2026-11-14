from sqlalchemy import select
from sqlalchemy.orm import Session

from app.infrastructure.persistence.models import Business


def get_default_business_id(session: Session) -> int | None:
    return session.scalar(select(Business.id).order_by(Business.id).limit(1))
