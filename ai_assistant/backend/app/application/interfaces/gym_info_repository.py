from abc import ABC, abstractmethod

from app.domain.entities.gym_info import BusinessPolicy, Trainer


class BusinessPolicyRepository(ABC):

    @abstractmethod
    def get_gym_policies(self) -> list[BusinessPolicy]:
        pass

    def create_gym_policy(self, policy: BusinessPolicy) -> int:
        raise NotImplementedError

    def get_gym_policy_by_id(self, policy_id: int) -> BusinessPolicy | None:
        raise NotImplementedError

    def update_gym_policy(self, policy_id: int, policy: BusinessPolicy) -> bool:
        raise NotImplementedError

    def delete_gym_policy(self, policy_id: int) -> bool:
        raise NotImplementedError


class TrainerRepository(ABC):

    @abstractmethod
    def get_trainers(self) -> list[Trainer]:
        pass

    def create_trainer(self, trainer: Trainer) -> int:
        raise NotImplementedError

    def get_trainer_by_id(self, trainer_id: int) -> Trainer | None:
        raise NotImplementedError

    def update_trainer(self, trainer_id: int, trainer: Trainer) -> bool:
        raise NotImplementedError

    def delete_trainer(self, trainer_id: int) -> bool:
        raise NotImplementedError