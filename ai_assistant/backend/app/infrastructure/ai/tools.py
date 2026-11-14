
from collections.abc import Callable

from langchain_core.tools import tool
from sqlalchemy.orm import Session

from app.application.use_cases import (
    GetBusinessHours,
    GetBusinessInformation,
    GetGymPolicies,
    GetMembershipPlans,
    GetProducts,
    GetTrainersList
)
from app.infrastructure.persistence.database import SessionLocal
from app.infrastructure.persistence.repositories import (
    BusinessPolicyRepository,
    BusinessRepository,
    MembershipPlanRepository,
    ProductRepository,
    TrainerRepository,
)


def create_gym_tools(
    session_factory: Callable[[], Session] | None = None,
):
    session_factory = session_factory or SessionLocal
    business_repository = BusinessRepository(session_factory)
    policy_repository = BusinessPolicyRepository(session_factory)
    trainer_repository = TrainerRepository(session_factory)
    product_repository = ProductRepository(session_factory)
    membership_repository = MembershipPlanRepository(session_factory)

    @tool
    def get_business_information() -> str:
        """Get the gym business name and description."""

        business = GetBusinessInformation(business_repository).execute()

        if business is None:
            return "Business information not available."

        return (
            f"Name: {business.name}\n"
            f"Description: {business.description or 'Not provided'}"
        )

    @tool
    def get_business_hours() -> str:
        """Get the gym opening hours and time intervals for each day."""

        hours = GetBusinessHours(business_repository).execute()

        if not hours:
            return "Business hours not available."

        return "\n".join(
            f"{day.day.value.capitalize()}: "
            + ", ".join(
                f"{interval.opens_at:%H:%M} - {interval.closes_at:%H:%M}"
                for interval in day.intervals
            )
            for day in hours
        )

    @tool
    def get_gym_policies() -> str:
        """Get the gym rules and business policies."""

        policies = GetGymPolicies(policy_repository).execute()

        if not policies:
            return "No gym policies available."

        return "\n".join(str(policy) for policy in policies)

    @tool
    def get_trainers() -> str:
        """Get the gym trainers, specialties, descriptions, and availability."""

        trainers = GetTrainersList(trainer_repository).execute()

        if not trainers:
            return "No trainers available."

        return "\n".join(str(trainer) for trainer in trainers)

    @tool
    def get_products() -> str:
        """Get the gym products, prices and availability."""

        products = GetProducts(product_repository).execute()

        if not products:
            return "No products available."

        return "\n".join(
            f"Product: {product.name}\n"
            f"Price: ${product.price:.2f}\n"
            f"Available: {'Yes' if product.available else 'No'}\n"
            f"Description: {product.description or 'Not provided'}"
            for product in products
        )

    @tool
    def get_membership_plans() -> str:
        """Get membership plans, prices and durations."""

        plans = GetMembershipPlans(membership_repository).execute()

        if not plans:
            return "No membership plans available."

        return "\n".join(
            f"Plan: {plan.name}\n"
            f"Price: ${plan.price:.2f}\n"
            f"Duration: {plan.duration_days} days\n"
            f"Description: {plan.description or 'Not provided'}"
            for plan in plans
        )

    return [
        get_business_information,
        get_business_hours,
        get_gym_policies,
        get_trainers,
        get_products,
        get_membership_plans,
    ]
