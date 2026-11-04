from app.application.interfaces.gym_info_repository import (
    BusinessPolicyRepository,
    TrainerRepository,
)
from app.domain.entities.gym_info import BusinessPolicy, Trainer


class InMemoryBusinessPolicyRepository(BusinessPolicyRepository):

    def __init__(self):
        self.gym_policies = [
            BusinessPolicy(
                title="Uso de vestuarios",
                description="Mantener el vestuario limpio y utilizar lockers durante la permanencia en el gimnasio.",
            ),
            BusinessPolicy(
                title="Higiene y seguridad",
                description="Limpiar los equipos despues de usarlos y guardar las pesas en su lugar correspondiente.",
            ),
        ]

    def get_gym_policies(self) -> list[BusinessPolicy]:
        return self.gym_policies.copy()


class InMemoryTrainerRepository(TrainerRepository):

    def __init__(self):
        self.trainers = [
            Trainer(
                name="Carlos Ramirez",
                description="Entrenador especializado en musculacion y fuerza.",
                specialties=["Musculacion", "Fuerza"],
                available=True,
            ),
            Trainer(
                name="Laura Gomez",
                description="Entrenadora especializada en acondicionamiento fisico.",
                specialties=["Acondicionamiento fisico", "Movilidad"],
                available=True,
            ),
        ]

    def get_trainers(self) -> list[Trainer]:
        return self.trainers.copy()
