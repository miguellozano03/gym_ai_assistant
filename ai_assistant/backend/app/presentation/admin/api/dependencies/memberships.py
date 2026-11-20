from app.infrastructure.persistence.repositories.membership_plan_repo import MembershipPlanRepository
from app.infrastructure.persistence.database import SessionLocal
from app.application.use_cases.memberships import (
    CreateMembershipPlan,
    DeleteMembershipPlan,
    GetMembershipPlanById,
    GetMembershipPlans,
    UpdateMembershipPlan,
)


#Repositories
membership_plan_repository = MembershipPlanRepository(SessionLocal)


# Get Uses Cases
def get_membership_plans() -> GetMembershipPlans:
    return GetMembershipPlans(membership_plan_repository)


def get_create_membership_plan() -> CreateMembershipPlan:
    return CreateMembershipPlan(membership_plan_repository)


def get_membership_plan_by_id() -> GetMembershipPlanById:
    return GetMembershipPlanById(membership_plan_repository)


def get_update_membership_plan() -> UpdateMembershipPlan:
    return UpdateMembershipPlan(membership_plan_repository)


def get_delete_membership_plan() -> DeleteMembershipPlan:
    return DeleteMembershipPlan(membership_plan_repository)
