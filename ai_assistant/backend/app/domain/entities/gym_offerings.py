from dataclasses import dataclass
from decimal import Decimal

@dataclass
class Product:
    name: str
    price: Decimal
    available: bool
    description: str | None = None

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Name cannot be empty")
        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("Description must be a string or None")
        if not isinstance(self.price, Decimal) or not self.price.is_finite():
            raise ValueError("Price must be a finite Decimal value")
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if not isinstance(self.available, bool):
            raise ValueError("Available must be a boolean")

@dataclass
class MembershipPlan:
    name: str
    price: Decimal
    duration_days: int
    description: str | None = None

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Name cannot be empty")
        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("Description must be a string or None")
        if not isinstance(self.price, Decimal) or not self.price.is_finite():
            raise ValueError("Price must be a finite Decimal value")
        if self.price < 0:
            raise ValueError("Price cannot be negative")
        if isinstance(self.duration_days, bool) or not isinstance(self.duration_days, int):
            raise ValueError("Duration days must be an integer")
        if self.duration_days <= 0:
            raise ValueError("Duration days cannot be less or equal than zero")