from dataclasses import asdict, is_dataclass
from datetime import time
from decimal import Decimal
from enum import Enum
from typing import Any

from langchain_core.tools import BaseTool, StructuredTool

from app.application.use_cases.get_business_info import (
    GetBusinessHours,
    GetBusinessInformation,
)
from app.application.use_cases.get_gym_policies import GetGymPolicies
from app.application.use_cases.get_memberships import GetMembershipPlans
from app.application.use_cases.get_products import GetProducts
from app.application.use_cases.get_trainers import GetTrainersList
from app.infrastructure.persistence.repositories.in_memory_business_repository import (
    InMemoryBusinessRepository,
)
from app.infrastructure.persistence.repositories.in_memory_gym_info_repository import (
    InMemoryBusinessPolicyRepository,
    InMemoryTrainerRepository,
)
from app.infrastructure.persistence.repositories.in_memory_gym_offerings_repository import (
    InMemoryMembershipPlanRepository,
    InMemoryProductRepository,
)


def _serialize(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return _serialize(asdict(value))
    if isinstance(value, (Decimal, time)):
        return str(value)
    if isinstance(value, Enum):
        return value.value
    if isinstance(value, list):
        return [_serialize(item) for item in value]
    if isinstance(value, tuple):
        return [_serialize(item) for item in value]
    if isinstance(value, dict):
        return {key: _serialize(item) for key, item in value.items()}
    return value


def create_gym_tools() -> list[BaseTool]:
    business_repository = InMemoryBusinessRepository()
    policy_repository = InMemoryBusinessPolicyRepository()
    trainer_repository = InMemoryTrainerRepository()
    product_repository = InMemoryProductRepository()
    membership_repository = InMemoryMembershipPlanRepository()

    def get_business_information() -> dict[str, Any] | None:
        return _serialize(
            GetBusinessInformation(business_repository).execute()
        )

    def get_business_hours() -> list[dict[str, Any]]:
        return _serialize(GetBusinessHours(business_repository).execute())

    def get_gym_policies() -> list[dict[str, Any]]:
        return _serialize(GetGymPolicies(policy_repository).execute())

    def get_trainers() -> list[dict[str, Any]]:
        return _serialize(GetTrainersList(trainer_repository).execute())

    def get_products() -> list[dict[str, Any]]:
        return _serialize(GetProducts(product_repository).execute())

    def get_membership_plans() -> list[dict[str, Any]]:
        return _serialize(GetMembershipPlans(membership_repository).execute())

    tool_definitions = [
        (
            get_business_information,
            "get_business_information",
            "Get the gym business name and description.",
        ),
        (
            get_business_hours,
            "get_business_hours",
            "Get the gym opening hours and time intervals for each day.",
        ),
        (
            get_gym_policies,
            "get_gym_policies",
            "Get the gym rules and business policies.",
        ),
        (
            get_trainers,
            "get_trainers",
            "Get the gym trainers, specialties, descriptions, and availability.",
        ),
        (
            get_products,
            "get_products",
            "Get the products available at the gym, including price and availability.",
        ),
        (
            get_membership_plans,
            "get_membership_plans",
            "Get membership plans, prices, durations, and descriptions.",
        ),
    ]

    return [
        StructuredTool.from_function(
            func=func,
            name=name,
            description=description,
        )
        for func, name, description in tool_definitions
    ]
