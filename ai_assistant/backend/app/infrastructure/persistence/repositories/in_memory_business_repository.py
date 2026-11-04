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
            name="Extreme Gym",
            description="Gimnasio especializado en musculación y acondicionamiento físico.",
        )

        self.business_hours = [
            BusinessHours(
                day=WeekDay.MONDAY,
                intervals=[
                    TimeRange("Morning", time(6, 0), time(11, 0)),
                    TimeRange("Afternoon", time(15, 0), time(20, 0)),
                ],
            ),
            BusinessHours(
                day=WeekDay.TUESDAY,
                intervals=[
                    TimeRange("Morning", time(6, 0), time(11, 0)),
                    TimeRange("Afternoon", time(15, 0), time(20, 0)),
                ],
            ),
            BusinessHours(
                day=WeekDay.WEDNESDAY,
                intervals=[
                    TimeRange("Morning", time(6, 0), time(11, 0)),
                    TimeRange("Afternoon", time(15, 0), time(20, 0)),
                ],
            ),
            BusinessHours(
                day=WeekDay.THURSDAY,
                intervals=[
                    TimeRange("Morning", time(6, 0), time(11, 0)),
                    TimeRange("Afternoon", time(15, 0), time(20, 0)),
                ],
            ),
            BusinessHours(
                day=WeekDay.FRIDAY,
                intervals=[
                    TimeRange("Morning", time(6, 0), time(11, 0)),
                    TimeRange("Afternoon", time(15, 0), time(20, 0)),
                ],
            ),
            BusinessHours(
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