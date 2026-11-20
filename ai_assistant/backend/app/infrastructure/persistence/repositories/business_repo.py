from collections.abc import Callable, Sequence

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.application.interfaces.business_repository import (
    BusinessRepository as BusinessRepositoryInterface,
)
from app.domain.entities.business import (
    Business as BusinessEntity,
    BusinessHours,
    TimeRange,
    WeekDay,
)
from app.infrastructure.persistence.models.business import (
    Business as BusinessModel,
    BusinessHourInterval,
    BusinessSchedule,
)
from app.infrastructure.persistence.repositories._helpers import (
    get_default_business_id,
)


class BusinessRepository(BusinessRepositoryInterface):
    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory

    def get_business(self) -> BusinessEntity | None:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return None

            model = session.get(BusinessModel, business_id)
            if model is None:
                return None

            return self._to_business_entity(model)

    def create_business(self, business: BusinessEntity) -> int:
        with self._session_factory() as session:
            model = BusinessModel(
                name=business.name,
                description=business.description,
            )
            session.add(model)
            session.flush()
            business_id = model.id
            session.commit()
            return business_id

    def get_business_by_id(self, business_id: int) -> BusinessEntity | None:
        with self._session_factory() as session:
            model = session.get(BusinessModel, business_id)
            return self._to_business_entity(model) if model is not None else None

    def update_business(self, business_id: int, data: dict) -> bool:

        with self._session_factory() as session:
            model = session.get(BusinessModel, business_id)

            if model is None:
                return False

            for key, value in data.items():
                setattr(model, key, value)

            session.commit()
            return True

    def delete_business(self, business_id: int) -> bool:
        with self._session_factory() as session:
            model = session.get(BusinessModel, business_id)
            if model is None:
                return False

            session.delete(model)
            session.commit()
            return True

    def get_business_hours(self) -> list[BusinessHours]:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return []

            schedules = session.scalars(
                select(BusinessSchedule)
                .where(BusinessSchedule.business_id == business_id)
                .options(selectinload(BusinessSchedule.intervals))
            ).all()

            return [
                self._to_business_hours(schedule)
                for schedule in self._ordered_schedules(schedules)
            ]

    def create_business_hours(self, business_hours: BusinessHours) -> int:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                raise ValueError("Cannot create business hours without a business.")

            schedule = BusinessSchedule(
                business_id=business_id,
                day=business_hours.day,
                intervals=[
                    BusinessHourInterval(
                        description=interval.description,
                        opens_at=interval.opens_at,
                        closes_at=interval.closes_at,
                    )
                    for interval in business_hours.intervals
                ],
            )
            session.add(schedule)
            session.flush()
            schedule_id = schedule.id
            session.commit()
            return schedule_id

    def get_business_hours_by_id(self, schedule_id: int) -> BusinessHours | None:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return None

            schedule = session.scalar(
                select(BusinessSchedule)
                .where(
                    BusinessSchedule.id == schedule_id,
                    BusinessSchedule.business_id == business_id,
                )
                .options(selectinload(BusinessSchedule.intervals))
            )
            return self._to_business_hours(schedule) if schedule is not None else None

    def update_business_hours(
        self,
        schedule_id: int,
        business_hours: BusinessHours,
    ) -> bool:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return False

            schedule = session.scalar(
                select(BusinessSchedule)
                .where(
                    BusinessSchedule.id == schedule_id,
                    BusinessSchedule.business_id == business_id,
                )
                .options(selectinload(BusinessSchedule.intervals))
            )
            if schedule is None:
                return False

            schedule.day = business_hours.day
            schedule.intervals = [
                BusinessHourInterval(
                    description=interval.description,
                    opens_at=interval.opens_at,
                    closes_at=interval.closes_at,
                )
                for interval in business_hours.intervals
            ]
            session.commit()
            return True

    def delete_business_hours(self, schedule_id: int) -> bool:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return False

            schedule = session.scalar(
                select(BusinessSchedule).where(
                    BusinessSchedule.id == schedule_id,
                    BusinessSchedule.business_id == business_id,
                )
            )
            if schedule is None:
                return False

            session.delete(schedule)
            session.commit()
            return True

    @staticmethod
    def _to_business_entity(model: BusinessModel) -> BusinessEntity:
        return BusinessEntity(name=model.name, description=model.description)

    @staticmethod
    def _to_business_hours(schedule: BusinessSchedule) -> BusinessHours:
        return BusinessHours(
            day=schedule.day,
            intervals=[
                TimeRange(
                    description=interval.description,
                    opens_at=interval.opens_at,
                    closes_at=interval.closes_at,
                )
                for interval in sorted(
                    schedule.intervals,
                    key=lambda interval: interval.opens_at,
                )
            ],
        )

    @staticmethod
    def _ordered_schedules(
        schedules: Sequence[BusinessSchedule],
    ) -> list[BusinessSchedule]:
        day_order = {day: index for index, day in enumerate(WeekDay)}
        return sorted(schedules, key=lambda schedule: day_order[schedule.day])