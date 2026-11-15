from app.application.interfaces.gym_offerings_repository import MembershipPlanRepository
from app.domain.entities.gym_offerings import MembershipPlan


class GetMembershipPlans:

    def __init__(self, repository: MembershipPlanRepository):
        self.repository = repository

    def execute(self) -> list[MembershipPlan]:
        return self.repository.get_membership_plans()


class CreateMembershipPlan:

    def __init__(self, repository: MembershipPlanRepository):
        self.repository = repository

    def execute(self, plan: MembershipPlan) -> int:
        return self.repository.create_membership_plan(plan)


class GetMembershipPlanById:

    def __init__(self, repository: MembershipPlanRepository):
        self.repository = repository

    def execute(self, plan_id: int) -> MembershipPlan | None:
        return self.repository.get_membership_plan_by_id(plan_id)


class UpdateMembershipPlan:

    def __init__(self, repository: MembershipPlanRepository):
        self.repository = repository

    def execute(self, plan_id: int, plan: MembershipPlan) -> bool:
        return self.repository.update_membership_plan(plan_id, plan)


class DeleteMembershipPlan:

    def __init__(self, repository: MembershipPlanRepository):
        self.repository = repository

    def execute(self, plan_id: int) -> bool:
        return self.repository.delete_membership_plan(plan_id)