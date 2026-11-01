from abc import ABC, abstractmethod

from app.domain.entities.gym_info import BusinessPolicy, Trainer


class BusinessPolicyRepository(ABC):

    @abstractmethod
    def get_gym_policies(self) -> list[BusinessPolicy]:
        pass

class TrainerRepository(ABC):

    @abstractmethod
    def get_trainers(self) -> list[Trainer]:
        pass