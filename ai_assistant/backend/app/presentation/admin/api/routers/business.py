from fastapi import APIRouter, Depends

from app.application.use_cases.business import (
    CreateBusiness,
    DeleteBusiness,
    GetBusinessById,
    UpdateBusiness,
)
from app.presentation.admin.api.dependencies.business import (
    get_business_by_id as get_business_by_id_use_case,
    get_create_business,
    get_delete_business,
    get_update_business,
)
from app.presentation.admin.api.schemas.business import (
    BusinessCreateSchema,
    BusinessUpdateSchema,
)

router = APIRouter(prefix="/business", tags=["Admin · Business"])


@router.post("")
def create_business(
    payload: BusinessCreateSchema,
    use_case: CreateBusiness = Depends(get_create_business),
):
    return use_case.execute(payload)


@router.get("/{business_id}")
def get_business_by_id(
    business_id: int,
    use_case: GetBusinessById = Depends(get_business_by_id_use_case),
):
    return use_case.execute(business_id)


@router.patch("/{business_id}")
def update_business(
    business_id: int,
    payload: BusinessUpdateSchema,
    use_case: UpdateBusiness = Depends(get_update_business),
):
    data = payload.model_dump(exclude_unset=True)
    return use_case.execute(business_id, data)


@router.delete("/{business_id}")
def delete_business(
    business_id: int,
    use_case: DeleteBusiness = Depends(get_delete_business),
):
    return use_case.execute(business_id)