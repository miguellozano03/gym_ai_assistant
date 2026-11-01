from app.application.interfaces.gym_info_repository import TrainerRepository
from app.domain.entities.gym_info import Trainer

class GetTrainersList:

    def __init__(self, repository: TrainerRepository):
        self.repository = repository

    def execute(self) -> list[Trainer]:
        return self.repository.get_trainers()