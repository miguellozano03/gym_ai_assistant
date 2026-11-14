from collections.abc import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.application.interfaces.gym_offerings_repository import (
    ProductRepository as ProductRepositoryInterface,
)
from app.domain.entities.gym_offerings import Product
from app.infrastructure.persistence.models import Product as ProductModel
from app.infrastructure.persistence.repositories._helpers import (
    get_default_business_id,
)


class ProductRepository(ProductRepositoryInterface):
    def __init__(self, session_factory: Callable[[], Session]):
        self._session_factory = session_factory

    def get_products(self) -> list[Product]:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return []

            products = session.scalars(
                select(ProductModel)
                .where(ProductModel.business_id == business_id)
                .order_by(ProductModel.id)
            ).all()

            return [self._to_entity(product) for product in products]

    def create_product(self, product: Product) -> int:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                raise ValueError("Cannot create a product without a business.")

            model = ProductModel(
                business_id=business_id,
                name=product.name,
                price=product.price,
                available=product.available,
                description=product.description,
            )
            session.add(model)
            session.flush()
            product_id = model.id
            session.commit()
            return product_id

    def get_product_by_id(self, product_id: int) -> Product | None:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return None

            product = session.scalar(
                select(ProductModel).where(
                    ProductModel.id == product_id,
                    ProductModel.business_id == business_id,
                )
            )
            return self._to_entity(product) if product is not None else None

    def update_product(self, product_id: int, product: Product) -> bool:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return False

            model = session.scalar(
                select(ProductModel).where(
                    ProductModel.id == product_id,
                    ProductModel.business_id == business_id,
                )
            )
            if model is None:
                return False

            model.name = product.name
            model.price = product.price
            model.available = product.available
            model.description = product.description
            session.commit()
            return True

    def delete_product(self, product_id: int) -> bool:
        with self._session_factory() as session:
            business_id = get_default_business_id(session)
            if business_id is None:
                return False

            model = session.scalar(
                select(ProductModel).where(
                    ProductModel.id == product_id,
                    ProductModel.business_id == business_id,
                )
            )
            if model is None:
                return False

            session.delete(model)
            session.commit()
            return True

    @staticmethod
    def _to_entity(model: ProductModel) -> Product:
        return Product(
            name=model.name,
            price=model.price,
            available=model.available,
            description=model.description,
        )
