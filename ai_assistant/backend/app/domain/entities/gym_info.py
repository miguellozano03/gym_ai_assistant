from dataclasses import dataclass


@dataclass
class Trainer:
    name: str
    description: str | None = None
    specialties: list[str] | None = None
    available: bool = True

    def __post_init__(self):
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("Trainer name cannot be empty")
        if self.description is not None and not isinstance(self.description, str):
            raise ValueError("Description must be a string or None")
        if self.specialties is not None:
            if not isinstance(self.specialties, list):
                raise ValueError("Specialties must be a list or None")
            if any(not isinstance(specialty, str) or not specialty.strip()
                   for specialty in self.specialties):
                raise ValueError("Specialties must contain non-empty strings")
        if not isinstance(self.available, bool):
            raise ValueError("Available must be a boolean")


@dataclass
class BusinessPolicy:
    title: str
    description: str
    active: bool = True

    def __post_init__(self):
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("Policy title cannot be empty")
        if not isinstance(self.description, str) or not self.description.strip():
            raise ValueError("Policy description cannot be empty")
        if not isinstance(self.active, bool):
            raise ValueError("Active must be a boolean")