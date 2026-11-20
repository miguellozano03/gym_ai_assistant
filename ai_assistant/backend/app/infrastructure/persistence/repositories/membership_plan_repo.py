from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.interfaces.gym_offerings_repository import (
    MembershipPlanRepository as MembershipPlanRepositoryInterface,
)
from app.domain.entities.gym_offerings import MembershipPlan
from app.infrastructure.persistence.models import MembershipPlan as MembershipPlanModel
from app.infrastructure.persistence.repositories._helpers import (
    get_default_business_id,
)


class MembershipPlanRepository(MembershipPlanRepositoryInterface):
    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory

    def get_membership_plans(self) -> list[MembershipPlan]:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return []

            plans = session.scalars(
                select(MembershipPlanModel)
                .where(MembershipPlanModel.business_id == business_id)
                .order_by(MembershipPlanModel.id)
            ).all()

            return [self._to_entity(plan) for plan in plans]

    def create_membership_plan(self, plan: MembershipPlan) -> int:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                raise ValueError("Cannot create a membership plan without a business.")

            model = MembershipPlanModel(
                business_id=business_id,
                name=plan.name,
                price=plan.price,
                duration_days=plan.duration_days,
                description=plan.description,
            )
            session.add(model)
            session.flush()
            plan_id = model.id
            session.commit()
            return plan_id

    def get_membership_plan_by_id(self, plan_id: int) -> MembershipPlan | None:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return None

            plan = session.scalar(
                select(MembershipPlanModel).where(
                    MembershipPlanModel.id == plan_id,
                    MembershipPlanModel.business_id == business_id,
                )
            )
            return self._to_entity(plan) if plan is not None else None

    def update_membership_plan(
        self,
        plan_id: int,
        plan: MembershipPlan,
    ) -> bool:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return False

            model = session.scalar(
                select(MembershipPlanModel).where(
                    MembershipPlanModel.id == plan_id,
                    MembershipPlanModel.business_id == business_id,
                )
            )
            if model is None:
                return False

            model.name = plan.name
            model.price = plan.price
            model.duration_days = plan.duration_days
            model.description = plan.description
            session.commit()
            return True

    def delete_membership_plan(self, plan_id: int) -> bool:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return False

            model = session.scalar(
                select(MembershipPlanModel).where(
                    MembershipPlanModel.id == plan_id,
                    MembershipPlanModel.business_id == business_id,
                )
            )
            if model is None:
                return False

            session.delete(model)
            session.commit()
            return True

    @staticmethod
    def _to_entity(model: MembershipPlanModel) -> MembershipPlan:
        return MembershipPlan(
            id=model.id,
            name=model.name,
            price=model.price,
            duration_days=model.duration_days,
            description=model.description,
        )
