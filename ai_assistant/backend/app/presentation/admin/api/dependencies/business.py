from app.application.use_cases.business import CreateBusiness, GetBusinessById, UpdateBusiness, DeleteBusiness
from app.infrastructure.persistence.repositories.business_repo import BusinessRepository
from app.infrastructure.persistence.database import SessionLocal

#Repository
business_repository = BusinessRepository(SessionLocal)


# Get Uses Cases
def get_create_business() -> CreateBusiness:
    return CreateBusiness(business_repository)

def get_business_by_id() -> GetBusinessById:
    return GetBusinessById(business_repository)

def get_update_business() -> UpdateBusiness:
    return UpdateBusiness(business_repository)

def get_delete_business() -> DeleteBusiness:
    return DeleteBusiness(business_repository)