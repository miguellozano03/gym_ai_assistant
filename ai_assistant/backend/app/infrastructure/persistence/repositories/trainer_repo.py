from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.interfaces.gym_info_repository import (
    TrainerRepository as TrainerRepositoryInterface,
)
from app.domain.entities.gym_info import Trainer
from app.infrastructure.persistence.models import Trainer as TrainerModel
from app.infrastructure.persistence.repositories._helpers import (
    get_default_business_id,
)


class TrainerRepository(TrainerRepositoryInterface):
    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory

    def get_trainers(self) -> list[Trainer]:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return []

            trainers = session.scalars(
                select(TrainerModel)
                .where(TrainerModel.business_id == business_id)
                .order_by(TrainerModel.id)
            ).all()

            return [self._to_entity(trainer) for trainer in trainers]

    def create_trainer(self, trainer: Trainer) -> int:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                raise ValueError("Cannot create a trainer without a business.")

            model = TrainerModel(
                business_id=business_id,
                name=trainer.name,
                description=trainer.description,
                specialties=trainer.specialties.copy()
                if trainer.specialties is not None
                else None,
                available=trainer.available,
            )
            session.add(model)
            session.flush()
            trainer_id = model.id
            session.commit()
            return trainer_id

    def get_trainer_by_id(self, trainer_id: int) -> Trainer | None:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return None

            trainer = session.scalar(
                select(TrainerModel).where(
                    TrainerModel.id == trainer_id,
                    TrainerModel.business_id == business_id,
                )
            )
            return self._to_entity(trainer) if trainer is not None else None

    def update_trainer(self, trainer_id: int, trainer: Trainer) -> bool:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return False

            model = session.scalar(
                select(TrainerModel).where(
                    TrainerModel.id == trainer_id,
                    TrainerModel.business_id == business_id,
                )
            )
            if model is None:
                return False

            model.name = trainer.name
            model.description = trainer.description
            model.specialties = (
                trainer.specialties.copy()
                if trainer.specialties is not None
                else None
            )
            model.available = trainer.available
            session.commit()
            return True

    def delete_trainer(self, trainer_id: int) -> bool:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return False

            model = session.scalar(
                select(TrainerModel).where(
                    TrainerModel.id == trainer_id,
                    TrainerModel.business_id == business_id,
                )
            )
            if model is None:
                return False

            session.delete(model)
            session.commit()
            return True

    @staticmethod
    def _to_entity(model: TrainerModel) -> Trainer:
        return Trainer(
            name=model.name,
            description=model.description,
            specialties=model.specialties.copy()
            if model.specialties is not None
            else None,
            available=model.available,
        )
