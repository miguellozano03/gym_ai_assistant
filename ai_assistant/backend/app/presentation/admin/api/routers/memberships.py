from dataclasses import replace

from fastapi import APIRouter, Depends

from app.application.use_cases.memberships import (
    CreateMembershipPlan,
    DeleteMembershipPlan,
    GetMembershipPlanById,
    GetMembershipPlans,
    UpdateMembershipPlan,
)
from app.domain.entities.gym_offerings import MembershipPlan
from app.presentation.admin.api.dependencies.memberships import (
    get_create_membership_plan,
    get_delete_membership_plan,
    get_membership_plan_by_id as get_membership_plan_by_id_use_case,
    get_membership_plans,
    get_update_membership_plan,
)
from app.presentation.admin.api.schemas.memberships import (
    MembershipPlanCreateSchema,
    MembershipPlanUpdateSchema,
)

router = APIRouter(prefix="/membership-plans", tags=["Admin · Membership Plans"])


@router.get("")
def get_membership_plans_endpoint(
    use_case: GetMembershipPlans = Depends(get_membership_plans),
):
    return use_case.execute()


@router.post("")
def create_membership_plan(
    payload: MembershipPlanCreateSchema,
    use_case: CreateMembershipPlan = Depends(get_create_membership_plan),
):
    return use_case.execute(MembershipPlan(**payload.model_dump()))


@router.get("/{plan_id}")
def get_membership_plan_by_id_endpoint(
    plan_id: int,
    use_case: GetMembershipPlanById = Depends(get_membership_plan_by_id_use_case),
):
    return use_case.execute(plan_id)


@router.patch("/{plan_id}")
def update_membership_plan(
    plan_id: int,
    payload: MembershipPlanUpdateSchema,
    get_use_case: GetMembershipPlanById = Depends(get_membership_plan_by_id_use_case),
    update_use_case: UpdateMembershipPlan = Depends(get_update_membership_plan),
):
    current = get_use_case.execute(plan_id)
    if current is None:
        return False

    updated = replace(current, **payload.model_dump(exclude_unset=True))
    return update_use_case.execute(plan_id, updated)


@router.delete("/{plan_id}")
def delete_membership_plan(
    plan_id: int,
    use_case: DeleteMembershipPlan = Depends(get_delete_membership_plan),
):
    return use_case.execute(plan_id)