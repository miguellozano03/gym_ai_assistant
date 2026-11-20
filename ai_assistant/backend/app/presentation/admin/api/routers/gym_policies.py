from dataclasses import replace

from fastapi import APIRouter, Depends

from app.application.use_cases.gym_policies import (
    CreateGymPolicy,
    DeleteGymPolicy,
    GetGymPolicies,
    GetGymPolicyById,
    UpdateGymPolicy,
)
from app.domain.entities.gym_info import BusinessPolicy
from app.presentation.admin.api.dependencies.gym_policies import (
    get_create_gym_policy,
    get_delete_gym_policy,
    get_gym_policies,
    get_gym_policy_by_id as get_gym_policy_by_id_use_case,
    get_update_gym_policy,
)
from app.presentation.admin.api.schemas.gym_policies import (
    GymPolicyCreateSchema,
    GymPolicyUpdateSchema,
)

router = APIRouter(prefix="/policies", tags=["Admin · Gym Policies"])


@router.get("")
def get_gym_policies_endpoint(
    use_case: GetGymPolicies = Depends(get_gym_policies),
):
    return use_case.execute()


@router.post("")
def create_gym_policy(
    payload: GymPolicyCreateSchema,
    use_case: CreateGymPolicy = Depends(get_create_gym_policy),
):
    return use_case.execute(BusinessPolicy(**payload.model_dump()))


@router.get("/{policy_id}")
def get_gym_policy_by_id_endpoint(
    policy_id: int,
    use_case: GetGymPolicyById = Depends(get_gym_policy_by_id_use_case),
):
    return use_case.execute(policy_id)


@router.patch("/{policy_id}")
def update_gym_policy(
    policy_id: int,
    payload: GymPolicyUpdateSchema,
    get_use_case: GetGymPolicyById = Depends(get_gym_policy_by_id_use_case),
    update_use_case: UpdateGymPolicy = Depends(get_update_gym_policy),
):
    current = get_use_case.execute(policy_id)
    if current is None:
        return False

    updated = replace(current, **payload.model_dump(exclude_unset=True))
    return update_use_case.execute(policy_id, updated)


@router.delete("/{policy_id}")
def delete_gym_policy(
    policy_id: int,
    use_case: DeleteGymPolicy = Depends(get_delete_gym_policy),
):
    return use_case.execute(policy_id)