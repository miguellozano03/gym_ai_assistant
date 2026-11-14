from abc import ABC, abstractmethod

from app.domain.entities.business import Business, BusinessHours

class BusinessRepository(ABC):

    def create_business(self, business: Business) -> int:
        raise NotImplementedError

    @abstractmethod
    def get_business(self) -> Business | None:
        pass

    def get_business_by_id(self, business_id: int) -> Business | None:
        raise NotImplementedError

    def update_business(self, business_id: int, business: Business) -> bool:
        raise NotImplementedError

    def delete_business(self, business_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_business_hours(self) -> list[BusinessHours]:
        pass

    def create_business_hours(
        self,
        business_hours: BusinessHours,
    ) -> int:
        raise NotImplementedError

    def get_business_hours_by_id(self, schedule_id: int) -> BusinessHours | None:
        raise NotImplementedError

    def update_business_hours(
        self,
        schedule_id: int,
        business_hours: BusinessHours,
    ) -> bool:
        raise NotImplementedError

    def delete_business_hours(self, schedule_id: int) -> bool:
        raise NotImplementedError
    