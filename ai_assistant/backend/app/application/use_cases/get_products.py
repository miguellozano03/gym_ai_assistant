from app.application.interfaces.gym_offerings_repository import ProductRepository
from app.domain.entities.gym_offerings import Product

class GetProducts:

    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def execute(self) -> list[Product]:
        return self.repository.get_products()
