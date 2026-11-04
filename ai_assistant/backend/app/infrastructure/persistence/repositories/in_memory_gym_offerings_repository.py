from decimal import Decimal

from app.application.interfaces.gym_offerings_repository import (
    MembershipPlanRepository,
    ProductRepository,
)
from app.domain.entities.gym_offerings import MembershipPlan, Product


class InMemoryProductRepository(ProductRepository):

    def __init__(self):
        self.products = [
            Product(
                name="Agua mineral",
                price=Decimal("1500"),
                available=True,
                description="Botella de agua mineral de 500 ml.",
            ),
            Product(
                name="Proteina en polvo",
                price=Decimal("25000"),
                available=True,
                description="Suplemento de proteina en polvo.",
            ),
        ]

    def get_products(self) -> list[Product]:
        return self.products.copy()


class InMemoryMembershipPlanRepository(MembershipPlanRepository):

    def __init__(self):
        self.membership_plans = [
            MembershipPlan(
                name="Diario",
                price=Decimal("3000"),
                duration_days=1,
                description="Acceso al gimnasio por un dia.",
            ),
            MembershipPlan(
                name="Mensual",
                price=Decimal("45000"),
                duration_days=30,
                description="Acceso al gimnasio por un mes.",
            ),
        ]

    def get_membership_plans(self) -> list[MembershipPlan]:
        return self.membership_plans.copy()
