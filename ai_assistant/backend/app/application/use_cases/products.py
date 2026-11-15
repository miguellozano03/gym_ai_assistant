from app.application.interfaces.gym_offerings_repository import ProductRepository
from app.domain.entities.gym_offerings import Product


class GetProducts:

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self) -> list[Product]:
        return self.repository.get_products()


class CreateProduct:

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, product: Product) -> int:
        return self.repository.create_product(product)


class GetProductById:

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, product_id: int) -> Product | None:
        return self.repository.get_product_by_id(product_id)


class UpdateProduct:

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, product_id: int, product: Product) -> bool:
        return self.repository.update_product(product_id, product)


class DeleteProduct:

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self, product_id: int) -> bool:
        return self.repository.delete_product(product_id)
