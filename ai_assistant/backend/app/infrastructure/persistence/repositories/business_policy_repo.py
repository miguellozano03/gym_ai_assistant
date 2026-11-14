from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.interfaces.gym_info_repository import (
    BusinessPolicyRepository as BusinessPolicyRepositoryInterface,
)
from app.domain.entities.gym_info import BusinessPolicy
from app.infrastructure.persistence.models import BusinessPolicy as BusinessPolicyModel
from app.infrastructure.persistence.repositories._helpers import (
    get_default_business_id,
)


class BusinessPolicyRepository(BusinessPolicyRepositoryInterface):
    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory

    def get_gym_policies(self) -> list[BusinessPolicy]:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return []

            policies = session.scalars(
                select(BusinessPolicyModel)
                .where(
                    BusinessPolicyModel.business_id == business_id,
                    BusinessPolicyModel.active.is_(True),
                )
                .order_by(BusinessPolicyModel.id)
            ).all()

            return [self._to_entity(policy) for policy in policies]

    def create_gym_policy(self, policy: BusinessPolicy) -> int:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                raise ValueError("Cannot create a policy without a business.")

            model = BusinessPolicyModel(
                business_id=business_id,
                title=policy.title,
                description=policy.description,
                active=policy.active,
            )
            session.add(model)
            session.flush()
            policy_id = model.id
            session.commit()
            return policy_id

    def get_gym_policy_by_id(self, policy_id: int) -> BusinessPolicy | None:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return None

            policy = session.scalar(
                select(BusinessPolicyModel).where(
                    BusinessPolicyModel.id == policy_id,
                    BusinessPolicyModel.business_id == business_id,
                )
            )
            return self._to_entity(policy) if policy is not None else None

    def update_gym_policy(self, policy_id: int, policy: BusinessPolicy) -> bool:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return False

            model = session.scalar(
                select(BusinessPolicyModel).where(
                    BusinessPolicyModel.id == policy_id,
                    BusinessPolicyModel.business_id == business_id,
                )
            )
            if model is None:
                return False

            model.title = policy.title
            model.description = policy.description
            model.active = policy.active
            session.commit()
            return True

    def delete_gym_policy(self, policy_id: int) -> bool:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return False

            model = session.scalar(
                select(BusinessPolicyModel).where(
                    BusinessPolicyModel.id == policy_id,
                    BusinessPolicyModel.business_id == business_id,
                )
            )
            if model is None:
                return False

            session.delete(model)
            session.commit()
            return True

    @staticmethod
    def _to_entity(model: BusinessPolicyModel) -> BusinessPolicy:
        return BusinessPolicy(
            title=model.title,
            description=model.description,
            active=model.active,
        )
