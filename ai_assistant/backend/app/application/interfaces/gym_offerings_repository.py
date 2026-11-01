from abc import ABC, abstractmethod

from app.domain.entities.gym_offerings import MembershipPlan, Product


class ProductRepository(ABC):

    @abstractmethod
    def get_products(self) -> list[Product]:
        pass


class MembershipPlanRepository(ABC):

    @abstractmethod
    def get_membership_plans(self) -> list[MembershipPlan]:
        pass