from abc import ABC, abstractmethod

from app.domain.entities.gym_offerings import MembershipPlan, Product


class ProductRepository(ABC):

    @abstractmethod
    def get_products(self) -> list[Product]:
        pass

    def create_product(self, product: Product) -> int:
        raise NotImplementedError

    def get_product_by_id(self, product_id: int) -> Product | None:
        raise NotImplementedError

    def update_product(self, product_id: int, product: Product) -> bool:
        raise NotImplementedError

    def delete_product(self, product_id: int) -> bool:
        raise NotImplementedError


class MembershipPlanRepository(ABC):

    @abstractmethod
    def get_membership_plans(self) -> list[MembershipPlan]:
        pass

    def create_membership_plan(self, plan: MembershipPlan) -> int:
        raise NotImplementedError

    def get_membership_plan_by_id(self, plan_id: int) -> MembershipPlan | None:
        raise NotImplementedError

    def update_membership_plan(self, plan_id: int, plan: MembershipPlan) -> bool:
        raise NotImplementedError

    def delete_membership_plan(self, plan_id: int) -> bool:
        raise NotImplementedError