from app.infrastructure.persistence.database import SessionLocal
from app.infrastructure.persistence.repositories.trainer_repo import TrainerRepository
from app.application.use_cases.trainers import (
    CreateTrainer,
    DeleteTrainer,
    GetTrainerById,
    GetTrainersList,
    UpdateTrainer,
)

#Repositories

trainer_repository = TrainerRepository(SessionLocal)


# Get Uses Cases
def get_trainers() -> GetTrainersList:
    return GetTrainersList(trainer_repository)


def get_create_trainer() -> CreateTrainer:
    return CreateTrainer(trainer_repository)


def get_trainer_by_id() -> GetTrainerById:
    return GetTrainerById(trainer_repository)


def get_update_trainer() -> UpdateTrainer:
    return UpdateTrainer(trainer_repository)


def get_delete_trainer() -> DeleteTrainer:
    return DeleteTrainer(trainer_repository)