import pytest
from datetime import time
from app.domain.entities.business import BusinessHours, Business, TimeRange, WeekDay


def test_business_creation():
    business = Business(
        name="Extreme Gym",
        description="The best gym in your town",
    )

    assert business.name == "Extreme Gym"
    assert business.description == "The best gym in your town"


def test_business_hours_creation():
    hours = BusinessHours(
        day=WeekDay.MONDAY,
        intervals=[
            TimeRange(
                description="Morning",
                opens_at=time(6),
                closes_at=time(11),
            ),
            TimeRange(
                description="Afternoon",
                opens_at=time(12),
                closes_at=time(14),
            ),
        ],
    )

    assert hours.day == WeekDay.MONDAY
    assert hours.intervals[0].description == "Morning"


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
        )