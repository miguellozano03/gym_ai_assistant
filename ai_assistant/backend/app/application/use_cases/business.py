from app.application.interfaces.business_repository import BusinessRepository
from app.domain.entities.business import Business

class CreateBusiness:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self, business: Business) -> int:
        return self.repository.create_business(business)


class GetBusinessById:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self, business_id: int) -> Business | None:
        return self.repository.get_business_by_id(business_id)


class UpdateBusiness:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self, business_id: int, business: Business) -> bool:
        return self.repository.update_business(business_id, business)


class DeleteBusiness:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self, business_id: int) -> bool:
        return self.repository.delete_business(business_id)
