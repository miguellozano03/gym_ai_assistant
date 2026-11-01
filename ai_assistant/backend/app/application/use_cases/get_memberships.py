from app.application.interfaces.gym_offerings_repository import MembershipPlanRepository
from app.domain.entities.gym_offerings import MembershipPlan

class GetMembershipPlans:

    def __init__(self, repository: MembershipPlanRepository):
        self.repository = repository

    def execute(self) -> list[MembershipPlan]:
        return self.repository.get_membership_plans()