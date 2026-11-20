from app.infrastructure.persistence.database import SessionLocal
from app.infrastructure.persistence.repositories.product_repo import ProductRepository
from app.application.use_cases.products import (
    CreateProduct,
    DeleteProduct,
    GetProductById,
    GetProducts,
    UpdateProduct,
)


#Repositories
product_repository = ProductRepository(SessionLocal)


# Get Uses Cases
def get_products() -> GetProducts:
    return GetProducts(product_repository)


def get_create_product() -> CreateProduct:
    return CreateProduct(product_repository)


def get_product_by_id() -> GetProductById:
    return GetProductById(product_repository)


def get_update_product() -> UpdateProduct:
    return UpdateProduct(product_repository)


def get_delete_product() -> DeleteProduct:
    return DeleteProduct(product_repository)

