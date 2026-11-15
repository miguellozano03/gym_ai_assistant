from app.application.interfaces.gym_info_repository import TrainerRepository
from app.domain.entities.gym_info import Trainer


class GetTrainersList:

    def __init__(self, repository: TrainerRepository):
        self.repository = repository

    def execute(self) -> list[Trainer]:
        return self.repository.get_trainers()


class CreateTrainer:

    def __init__(self, repository: TrainerRepository):
        self.repository = repository

    def execute(self, trainer: Trainer) -> int:
        return self.repository.create_trainer(trainer)


class GetTrainerById:

    def __init__(self, repository: TrainerRepository):
        self.repository = repository

    def execute(self, trainer_id: int) -> Trainer | None:
        return self.repository.get_trainer_by_id(trainer_id)


class UpdateTrainer:

    def __init__(self, repository: TrainerRepository):
        self.repository = repository

    def execute(self, trainer_id: int, trainer: Trainer) -> bool:
        return self.repository.update_trainer(trainer_id, trainer)


class DeleteTrainer:

    def __init__(self, repository: TrainerRepository):
        self.repository = repository

    def execute(self, trainer_id: int) -> bool:
        return self.repository.delete_trainer(trainer_id)