from app.infrastructure.persistence.repositories.business_policy_repo import BusinessPolicyRepository
from app.infrastructure.persistence.database import SessionLocal
from app.application.use_cases.gym_policies import (
    CreateGymPolicy,
    DeleteGymPolicy,
    GetGymPolicies,
    GetGymPolicyById,
    UpdateGymPolicy,
)

#Repository
business_policy_repository = BusinessPolicyRepository(SessionLocal)


# Get Uses Cases
def get_gym_policies() -> GetGymPolicies:
    return GetGymPolicies(business_policy_repository)


def get_create_gym_policy() -> CreateGymPolicy:
    return CreateGymPolicy(business_policy_repository)


def get_gym_policy_by_id() -> GetGymPolicyById:
    return GetGymPolicyById(business_policy_repository)


def get_update_gym_policy() -> UpdateGymPolicy:
    return UpdateGymPolicy(business_policy_repository)


def get_delete_gym_policy() -> DeleteGymPolicy:
    return DeleteGymPolicy(business_policy_repository)