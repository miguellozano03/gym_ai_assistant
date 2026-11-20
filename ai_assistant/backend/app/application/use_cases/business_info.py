from app.application.interfaces.business_repository import BusinessRepository
from app.domain.entities.business import Business, BusinessHours


class GetBusinessHours:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self) -> list[BusinessHours]:
        return self.repository.get_business_hours()


class CreateBusinessHours:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self, business_hours: BusinessHours) -> int:
        return self.repository.create_business_hours(business_hours)


class GetBusinessHoursById:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self, schedule_id: int) -> BusinessHours | None:
        return self.repository.get_business_hours_by_id(schedule_id)


class UpdateBusinessHours:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self, schedule_id: int, business_hours: BusinessHours) -> bool:
        return self.repository.update_business_hours(schedule_id, business_hours)


class DeleteBusinessHours:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self, schedule_id: int) -> bool:
        return self.repository.delete_business_hours(schedule_id)


class GetBusinessInformation:

    def __init__(self, repository: BusinessRepository):
        self.repository = repository

    def execute(self) -> Business | None:
        return self.repository.get_business()


