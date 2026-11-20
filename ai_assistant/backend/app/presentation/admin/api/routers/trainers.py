from dataclasses import replace

from fastapi import APIRouter, Depends

from app.application.use_cases.trainers import (
    CreateTrainer,
    DeleteTrainer,
    GetTrainerById,
    GetTrainersList,
    UpdateTrainer,
)
from app.domain.entities.gym_info import Trainer
from app.presentation.admin.api.dependencies.trainers import (
    get_create_trainer,
    get_delete_trainer,
    get_trainer_by_id as get_trainer_by_id_use_case,
    get_trainers,
    get_update_trainer,
)
from app.presentation.admin.api.schemas.trainers import (
    TrainerCreateSchema,
    TrainerUpdateSchema,
)

router = APIRouter(prefix="/trainers", tags=["Admin · Trainers"])


@router.get("")
def get_trainers_endpoint(use_case: GetTrainersList = Depends(get_trainers)):
    return use_case.execute()


@router.post("")
def create_trainer(
    payload: TrainerCreateSchema,
    use_case: CreateTrainer = Depends(get_create_trainer),
):
    return use_case.execute(Trainer(**payload.model_dump()))


@router.get("/{trainer_id}")
def get_trainer_by_id_endpoint(
    trainer_id: int,
    use_case: GetTrainerById = Depends(get_trainer_by_id_use_case),
):
    return use_case.execute(trainer_id)


@router.patch("/{trainer_id}")
def update_trainer(
    trainer_id: int,
    payload: TrainerUpdateSchema,
    get_use_case: GetTrainerById = Depends(get_trainer_by_id_use_case),
    update_use_case: UpdateTrainer = Depends(get_update_trainer),
):
    current = get_use_case.execute(trainer_id)
    if current is None:
        return False

    updated = replace(current, **payload.model_dump(exclude_unset=True))
    return update_use_case.execute(trainer_id, updated)


@router.delete("/{trainer_id}")
def delete_trainer(
    trainer_id: int,
    use_case: DeleteTrainer = Depends(get_delete_trainer),
):
    return use_case.execute(trainer_id)