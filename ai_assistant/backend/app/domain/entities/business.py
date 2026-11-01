from dataclasses import dataclass
from datetime import time
from enum import StrEnum

class WeekDay(StrEnum):
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"

@dataclass
class TimeRange:
    description: str | None
    opens_at: time
    closes_at: time

    def __post_init__(self):
        if not isinstance(self.opens_at, time):
            raise ValueError("Opening time must be a valid time")
        if not isinstance(self.closes_at, time):
            raise ValueError("Closing time must be a valid time")
        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("Description must be a string or None")
        if self.opens_at >= self.closes_at:
            raise ValueError("Closing time must be after opening time")

@dataclass
class BusinessHours:
    day: WeekDay
    intervals: list[TimeRange]

    def __post_init__(self):
        if not isinstance(self.day, WeekDay):
            raise ValueError("Day must be a valid WeekDay")
        if not isinstance(self.intervals, list) or not self.intervals:
            raise ValueError("Business hours must contain at least one interval")
        if any(not isinstance(interval, TimeRange) for interval in self.intervals):
            raise ValueError("Intervals must contain only TimeRange values")

        ordered = sorted(self.intervals, key=lambda interval: interval.opens_at)
        for previous, current in zip(ordered, ordered[1:]):
            if current.opens_at < previous.closes_at:
                raise ValueError("Business hour intervals cannot overlap")
   
@dataclass
class Business:
    name: str
    description: str | None
    hours: list[BusinessHours]

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Business name cannot be empty")
        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("Description must be a string or None")
        if not isinstance(self.hours, list) or not self.hours:
            raise ValueError("Business must contain at least one day of hours")
        if any(not isinstance(business_hours, BusinessHours) for business_hours in self.hours):
            raise ValueError("Hours must contain only BusinessHours values")

        days = [business_hours.day for business_hours in self.hours]
        if len(set(days)) != len(days):
            raise ValueError("Business hours cannot contain duplicate days")