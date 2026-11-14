from datetime import time
from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.application.interfaces.gym_info_repository import (
    BusinessPolicyRepository as BusinessPolicyRepositoryInterface,
    TrainerRepository as TrainerRepositoryInterface,
)
from app.application.interfaces.gym_offerings_repository import (
    MembershipPlanRepository as MembershipPlanRepositoryInterface,
    ProductRepository as ProductRepositoryInterface,
)
from app.domain.entities.business import Business as BusinessEntity
from app.domain.entities.business import BusinessHours, TimeRange, WeekDay
from app.domain.entities.gym_info import BusinessPolicy, Trainer
from app.domain.entities.gym_offerings import MembershipPlan, Product
from app.infrastructure.persistence.database import Base
from app.infrastructure.persistence.models import (
    Business,
    BusinessPolicy as BusinessPolicyModel,
    MembershipPlan as MembershipPlanModel,
    Product as ProductModel,
    Trainer as TrainerModel,
)
from app.infrastructure.persistence.repositories import (
    BusinessPolicyRepository,
    BusinessRepository,
    MembershipPlanRepository,
    ProductRepository,
    TrainerRepository,
)


def test_sqlalchemy_repositories_map_records_for_default_business():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    with session_factory() as session:
        business = Business(name="Extreme Gym")
        other_business = Business(name="Other Gym")
        session.add_all([business, other_business])
        session.flush()
        session.add_all(
            [
                BusinessPolicyModel(
                    business_id=business.id,
                    title="Higiene",
                    description="Limpiar los equipos.",
                    active=True,
                ),
                BusinessPolicyModel(
                    business_id=business.id,
                    title="Inactiva",
                    description="No mostrar.",
                    active=False,
                ),
                TrainerModel(
                    business_id=business.id,
                    name="Laura",
                    description="Acondicionamiento",
                    specialties=["Movilidad"],
                    available=True,
                ),
                ProductModel(
                    business_id=business.id,
                    name="Agua mineral",
                    price=Decimal("1500"),
                    available=True,
                    description="Botella de 500 ml.",
                ),
                MembershipPlanModel(
                    business_id=business.id,
                    name="Mensual",
                    price=Decimal("45000"),
                    duration_days=30,
                    description="Acceso por un mes.",
                ),
                ProductModel(
                    business_id=other_business.id,
                    name="Otro producto",
                    price=Decimal("100"),
                    available=True,
                ),
            ]
        )
        session.commit()

    try:
        policy_repository = BusinessPolicyRepository(session_factory)
        trainer_repository = TrainerRepository(session_factory)
        product_repository = ProductRepository(session_factory)
        membership_repository = MembershipPlanRepository(session_factory)

        assert isinstance(policy_repository, BusinessPolicyRepositoryInterface)
        assert policy_repository.get_gym_policies() == [
            BusinessPolicy(
                title="Higiene",
                description="Limpiar los equipos.",
                active=True,
            )
        ]

        assert isinstance(trainer_repository, TrainerRepositoryInterface)
        assert trainer_repository.get_trainers() == [
            Trainer(
                name="Laura",
                description="Acondicionamiento",
                specialties=["Movilidad"],
                available=True,
            )
        ]

        assert isinstance(product_repository, ProductRepositoryInterface)
        assert product_repository.get_products() == [
            Product(
                name="Agua mineral",
                price=Decimal("1500"),
                available=True,
                description="Botella de 500 ml.",
            )
        ]

        assert isinstance(membership_repository, MembershipPlanRepositoryInterface)
        assert membership_repository.get_membership_plans() == [
            MembershipPlan(
                name="Mensual",
                price=Decimal("45000"),
                duration_days=30,
                description="Acceso por un mes.",
            )
        ]

        business_repository = BusinessRepository(session_factory)
        business_id = business_repository.create_business(
            BusinessEntity(name="New Gym", description="Nueva sede.")
        )
        assert business_repository.get_business_by_id(business_id) == BusinessEntity(
            name="New Gym",
            description="Nueva sede.",
        )
        assert business_repository.update_business(
            business_id,
            BusinessEntity(name="Updated Gym"),
        )
        assert business_repository.get_business_by_id(business_id) == BusinessEntity(
            name="Updated Gym"
        )
        assert business_repository.delete_business(business_id)
        assert business_repository.get_business_by_id(business_id) is None

        hours = BusinessHours(
            day=WeekDay.SUNDAY,
            intervals=[TimeRange("Evening", time(18), time(22))],
        )
        schedule_id = business_repository.create_business_hours(hours)
        assert business_repository.get_business_hours_by_id(schedule_id) == hours
        updated_hours = BusinessHours(
            day=WeekDay.SATURDAY,
            intervals=[TimeRange("Morning", time(8), time(12))],
        )
        assert business_repository.update_business_hours(schedule_id, updated_hours)
        assert (
            business_repository.get_business_hours_by_id(schedule_id) == updated_hours
        )
        assert business_repository.delete_business_hours(schedule_id)
        assert business_repository.get_business_hours_by_id(schedule_id) is None

        policy_id = policy_repository.create_gym_policy(
            BusinessPolicy(
                title="New policy",
                description="New description.",
            )
        )
        assert policy_repository.get_gym_policy_by_id(policy_id) == BusinessPolicy(
            title="New policy",
            description="New description.",
        )
        assert policy_repository.update_gym_policy(
            policy_id,
            BusinessPolicy(
                title="Updated policy",
                description="Updated description.",
                active=False,
            ),
        )
        assert policy_repository.get_gym_policy_by_id(policy_id) == BusinessPolicy(
            title="Updated policy",
            description="Updated description.",
            active=False,
        )
        assert policy_repository.delete_gym_policy(policy_id)
        assert policy_repository.get_gym_policy_by_id(policy_id) is None

        trainer_id = trainer_repository.create_trainer(Trainer(name="New trainer"))
        assert trainer_repository.get_trainer_by_id(trainer_id) == Trainer(
            name="New trainer"
        )
        assert trainer_repository.update_trainer(
            trainer_id,
            Trainer(name="Updated trainer", available=False),
        )
        assert trainer_repository.get_trainer_by_id(trainer_id) == Trainer(
            name="Updated trainer",
            available=False,
        )
        assert trainer_repository.delete_trainer(trainer_id)
        assert trainer_repository.get_trainer_by_id(trainer_id) is None

        product_id = product_repository.create_product(
            Product(name="New product", price=Decimal("10"), available=True)
        )
        assert product_repository.get_product_by_id(product_id) == Product(
            name="New product",
            price=Decimal("10"),
            available=True,
        )
        assert product_repository.update_product(
            product_id,
            Product(name="Updated product", price=Decimal("12"), available=False),
        )
        assert product_repository.get_product_by_id(product_id) == Product(
            name="Updated product",
            price=Decimal("12"),
            available=False,
        )
        assert product_repository.delete_product(product_id)
        assert product_repository.get_product_by_id(product_id) is None

        plan_id = membership_repository.create_membership_plan(
            MembershipPlan(
                name="New plan",
                price=Decimal("100"),
                duration_days=7,
            )
        )
        assert membership_repository.get_membership_plan_by_id(plan_id) == (
            MembershipPlan(
                name="New plan",
                price=Decimal("100"),
                duration_days=7,
            )
        )
        assert membership_repository.update_membership_plan(
            plan_id,
            MembershipPlan(
                name="Updated plan",
                price=Decimal("200"),
                duration_days=14,
            ),
        )
        assert membership_repository.get_membership_plan_by_id(plan_id) == (
            MembershipPlan(
                name="Updated plan",
                price=Decimal("200"),
                duration_days=14,
            )
        )
        assert membership_repository.delete_membership_plan(plan_id)
        assert membership_repository.get_membership_plan_by_id(plan_id) is None
    finally:
        engine.dispose()
