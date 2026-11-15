from app.application.interfaces.gym_info_repository import BusinessPolicyRepository
from app.domain.entities.gym_info import BusinessPolicy


class GetGymPolicies:

    def __init__(self, repository: BusinessPolicyRepository):
        self.repository = repository

    def execute(self) -> list[BusinessPolicy]:
        return self.repository.get_gym_policies()


class CreateGymPolicy:

    def __init__(self, repository: BusinessPolicyRepository):
        self.repository = repository

    def execute(self, policy: BusinessPolicy) -> int:
        return self.repository.create_gym_policy(policy)


class GetGymPolicyById:

    def __init__(self, repository: BusinessPolicyRepository):
        self.repository = repository

    def execute(self, policy_id: int) -> BusinessPolicy | None:
        return self.repository.get_gym_policy_by_id(policy_id)


class UpdateGymPolicy:

    def __init__(self, repository: BusinessPolicyRepository):
        self.repository = repository

    def execute(self, policy_id: int, policy: BusinessPolicy) -> bool:
        return self.repository.update_gym_policy(policy_id, policy)


class DeleteGymPolicy:

    def __init__(self, repository: BusinessPolicyRepository):
        self.repository = repository

    def execute(self, policy_id: int) -> bool:
        return self.repository.delete_gym_policy(policy_id)