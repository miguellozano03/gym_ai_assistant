from dataclasses import replace

from fastapi import APIRouter, Depends

from app.application.use_cases.products import (
    CreateProduct,
    DeleteProduct,
    GetProductById,
    GetProducts,
    UpdateProduct,
)
from app.domain.entities.gym_offerings import Product
from app.presentation.admin.api.dependencies.products import (
    get_create_product,
    get_delete_product,
    get_product_by_id as get_product_by_id_use_case,
    get_products,
    get_update_product,
)
from app.presentation.admin.api.schemas.products import (
    ProductCreateSchema,
    ProductUpdateSchema,
)

router = APIRouter(prefix="/products", tags=["Admin · Products"])


@router.get("")
def get_products_endpoint(use_case: GetProducts = Depends(get_products)):
    return use_case.execute()


@router.post("")
def create_product(
    payload: ProductCreateSchema,
    use_case: CreateProduct = Depends(get_create_product),
):
    return use_case.execute(Product(**payload.model_dump()))


@router.get("/{product_id}")
def get_product_by_id_endpoint(
    product_id: int,
    use_case: GetProductById = Depends(get_product_by_id_use_case),
):
    return use_case.execute(product_id)


@router.patch("/{product_id}")
def update_product(
    product_id: int,
    payload: ProductUpdateSchema,
    get_use_case: GetProductById = Depends(get_product_by_id_use_case),
    update_use_case: UpdateProduct = Depends(get_update_product),
):
    current = get_use_case.execute(product_id)
    if current is None:
        return False

    updated = replace(current, **payload.model_dump(exclude_unset=True))
    return update_use_case.execute(product_id, updated)


@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    use_case: DeleteProduct = Depends(get_delete_product),
):
    return use_case.execute(product_id)