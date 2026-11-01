from app.application.interfaces.business_repository import BusinessRepository
from app.domain.entities.business import Business, BusinessHours

class GetBusinessHours:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self) -> list[BusinessHours]:
        return self.repository.get_business_hours()

class GetBusinessInformation:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self) -> Business | None:
        return self.repository.get_business()
