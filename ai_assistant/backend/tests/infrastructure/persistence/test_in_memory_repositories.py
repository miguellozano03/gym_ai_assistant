from app.application.interfaces.gym_info_repository import (
    BusinessPolicyRepository,
    TrainerRepository,
)
from app.application.interfaces.gym_offerings_repository import (
    MembershipPlanRepository,
    ProductRepository,
)
from app.domain.entities.gym_info import BusinessPolicy, Trainer
from app.domain.entities.gym_offerings import MembershipPlan, Product
from app.infrastructure.persistence.repositories.in_memory_gym_info_repository import (
    InMemoryBusinessPolicyRepository,
    InMemoryTrainerRepository,
)
from app.infrastructure.persistence.repositories.in_memory_gym_offerings_repository import (
    InMemoryMembershipPlanRepository,
    InMemoryProductRepository,
)


def test_in_memory_business_policy_repository():
    repository = InMemoryBusinessPolicyRepository()

    policies = repository.get_gym_policies()

    assert isinstance(repository, BusinessPolicyRepository)
    assert policies
    assert all(isinstance(policy, BusinessPolicy) for policy in policies)
    assert policies is not repository.gym_policies


def test_in_memory_trainer_repository():
    repository = InMemoryTrainerRepository()

    trainers = repository.get_trainers()

    assert isinstance(repository, TrainerRepository)
    assert trainers
    assert all(isinstance(trainer, Trainer) for trainer in trainers)
    assert trainers is not repository.trainers


def test_in_memory_product_repository():
    repository = InMemoryProductRepository()

    products = repository.get_products()

    assert isinstance(repository, ProductRepository)
    assert products
    assert all(isinstance(product, Product) for product in products)
    assert products is not repository.products


def test_in_memory_membership_plan_repository():
    repository = InMemoryMembershipPlanRepository()

    plans = repository.get_membership_plans()

    assert isinstance(repository, MembershipPlanRepository)
    assert plans
    assert all(isinstance(plan, MembershipPlan) for plan in plans)
    assert plans is not repository.membership_plans
