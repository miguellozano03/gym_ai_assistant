from app.application.use_cases.business_info import (
    CreateBusinessHours,
    DeleteBusinessHours,
    GetBusinessHours,
    GetBusinessHoursById,
    UpdateBusinessHours,
)
from app.infrastructure.persistence.repositories.business_repo import BusinessRepository
from app.infrastructure.persistence.database import SessionLocal

#Repository
business_repository = BusinessRepository(SessionLocal)


# Get Uses Cases
def get_business_hours() -> GetBusinessHours:
    return GetBusinessHours(business_repository)


def get_create_business_hours() -> CreateBusinessHours:
    return CreateBusinessHours(business_repository)


def get_business_hours_by_id() -> GetBusinessHoursById:
    return GetBusinessHoursById(business_repository)


def get_update_business_hours() -> UpdateBusinessHours:
    return UpdateBusinessHours(business_repository)


def get_delete_business_hours() -> DeleteBusinessHours:
    return DeleteBusinessHours(business_repository)