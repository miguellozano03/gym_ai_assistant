from dataclasses import replace

from fastapi import APIRouter, Depends

from app.application.use_cases.business_info import (
    CreateBusinessHours,
    DeleteBusinessHours,
    GetBusinessHours,
    GetBusinessHoursById,
    UpdateBusinessHours,
)
from app.domain.entities.business import BusinessHours, TimeRange
from app.presentation.admin.api.dependencies.business_hours import (
    get_business_hours,
    get_business_hours_by_id as get_business_hours_by_id_use_case,
    get_create_business_hours,
    get_delete_business_hours,
    get_update_business_hours,
)
from app.presentation.admin.api.schemas.business_hours import (
    BusinessHoursCreateSchema,
    BusinessHoursUpdateSchema,
)

router = APIRouter(prefix="/business-hours", tags=["Admin · Business Hours"])


@router.get("")
def get_business_hours_endpoint(
    use_case: GetBusinessHours = Depends(get_business_hours),
):
    return use_case.execute()


@router.post("")
def create_business_hours(
    payload: BusinessHoursCreateSchema,
    use_case: CreateBusinessHours = Depends(get_create_business_hours),
):
    business_hours = BusinessHours(
        day=payload.day,
        intervals=[TimeRange(**interval.model_dump()) for interval in payload.intervals],
    )
    return use_case.execute(business_hours)


@router.get("/{schedule_id}")
def get_business_hours_by_id_endpoint(
    schedule_id: int,
    use_case: GetBusinessHoursById = Depends(get_business_hours_by_id_use_case),
):
    return use_case.execute(schedule_id)


@router.patch("/{schedule_id}")
def update_business_hours(
    schedule_id: int,
    payload: BusinessHoursUpdateSchema,
    get_use_case: GetBusinessHoursById = Depends(get_business_hours_by_id_use_case),
    update_use_case: UpdateBusinessHours = Depends(get_update_business_hours),
):
    current = get_use_case.execute(schedule_id)
    if current is None:
        return False

    data = payload.model_dump(exclude_unset=True)
    if "intervals" in data:
        data["intervals"] = [TimeRange(**interval) for interval in data["intervals"]]
    return update_use_case.execute(schedule_id, replace(current, **data))


@router.delete("/{schedule_id}")
def delete_business_hours(
    schedule_id: int,
    use_case: DeleteBusinessHours = Depends(get_delete_business_hours),
):
    return use_case.execute(schedule_id)