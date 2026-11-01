import pytest
from datetime import time
from app.domain.entities.business import BusinessHours, Business, TimeRange, WeekDay


@pytest.fixture
def business_hours():
    weekdays = [
        BusinessHours(
            day=day,
            intervals=[
                TimeRange(
                    description="Morning",
                    opens_at=time(6,0),
                    closes_at=time(11,0)
                ),
                TimeRange(
                    description="Afternoon",
                    opens_at=time(6,0),
                    closes_at=time(11,0)
                    )]
        ) for day in WeekDay if day not in WeekDay.SATURDAY
    ]

    weekends = [
        BusinessHours(
            day=WeekDay.SATURDAY,
            intervals=[
                TimeRange(
                    description="Morning",
                    opens_at=time(6,0),
                    closes_at=time(11,0)
                )
            ]
        )
    ]

    return [weekdays, weekends]


def test_business_creation(business_hours):

    weekdays, weekends = business_hours

    business = Business(
        name="Extreme Gym",
        description="The best gym in your town",
        hours=weekdays + weekends
    )

    assert business.hours[0].day == WeekDay.MONDAY
    assert business.hours[0].intervals[0].description == "Morning"


def test_time_range_rejects_invalid_order():
    with pytest.raises(ValueError):
        TimeRange(description=None, opens_at=time(11), closes_at=time(6))


def test_business_hours_rejects_overlapping_intervals():
    intervals = [
        TimeRange(None, time(6), time(12)),
        TimeRange(None, time(11), time(14)),
    ]

    with pytest.raises(ValueError):
        BusinessHours(day=WeekDay.MONDAY, intervals=intervals)


def test_business_rejects_empty_name():
    with pytest.raises(ValueError):
        Business(
            name=" ",
            description=None,
            hours=[BusinessHours(WeekDay.MONDAY, [TimeRange(None, time(6), time(12))])],
        )


def test_business_rejects_duplicate_days():
    hours = BusinessHours(WeekDay.MONDAY, [TimeRange(None, time(6), time(12))])

    with pytest.raises(ValueError):
        Business(name="Extreme Gym", description=None, hours=[hours, hours])