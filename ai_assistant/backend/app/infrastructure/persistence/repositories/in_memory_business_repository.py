from datetime import time

from app.domain.entities.business import (
    Business,
    BusinessHours,
    TimeRange,
    WeekDay,
)
from app.application.interfaces.business_repository import BusinessRepository


class InMemoryBusinessRepository(BusinessRepository):

    def __init__(self):
        self.business = Business(
            id=1,
            name="Extreme Gym",
            description="Gimnasio especializado en musculación y acondicionamiento físico.",
        )

        self.business_hours = [
            BusinessHours(
                id=1,
                day=WeekDay.MONDAY,
                intervals=[
                    TimeRange("Morning", time(6, 0), time(11, 0)),
                    TimeRange("Afternoon", time(15, 0), time(20, 0)),
                ],
            ),
            BusinessHours(
                id=2,
                day=WeekDay.TUESDAY,
                intervals=[
                    TimeRange("Morning", time(6, 0), time(11, 0)),
                    TimeRange("Afternoon", time(15, 0), time(20, 0)),
                ],
            ),
            BusinessHours(
                id=3,
                day=WeekDay.WEDNESDAY,
                intervals=[
                    TimeRange("Morning", time(6, 0), time(11, 0)),
                    TimeRange("Afternoon", time(15, 0), time(20, 0)),
                ],
            ),
            BusinessHours(
                id=4,
                day=WeekDay.THURSDAY,
                intervals=[
                    TimeRange("Morning", time(6, 0), time(11, 0)),
                    TimeRange("Afternoon", time(15, 0), time(20, 0)),
                ],
            ),
            BusinessHours(
                id=5,
                day=WeekDay.FRIDAY,
                intervals=[
                    TimeRange("Morning", time(6, 0), time(11, 0)),
                    TimeRange("Afternoon", time(15, 0), time(20, 0)),
                ],
            ),
            BusinessHours(
                id=6,
                day=WeekDay.SATURDAY,
                intervals=[
                    TimeRange("Morning", time(7, 0), time(12, 0)),
                ],
            ),
        ]

    def get_business(self) -> Business | None:
        return self.business

    def get_business_hours(self) -> list[BusinessHours]:
        return self.business_hours.copy()