from abc import ABC, abstractmethod

from app.domain.entities.business import Business, BusinessHours

class BusinessRepository(ABC):

    @abstractmethod
    def get_business(self) -> Business | None:
        pass

    @abstractmethod
    def get_business_hours(self) -> list[BusinessHours]:
        pass