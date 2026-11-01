from app.application.interfaces.gym_info_repository import BusinessPolicyRepository
from app.domain.entities.gym_info import BusinessPolicy

class GetGymPolicies:

    def __init__(self, repository: BusinessPolicyRepository):
        self.repository = repository

    def execute(self) -> list[BusinessPolicy]:
        return self.repository.get_gym_policies()