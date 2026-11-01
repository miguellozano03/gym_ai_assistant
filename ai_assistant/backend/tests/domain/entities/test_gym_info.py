import pytest

from app.domain.entities.gym_info import BusinessPolicy, Trainer


@pytest.mark.parametrize("name", ["", "  ", None])
def test_trainer_rejects_invalid_name(name):
    with pytest.raises(ValueError):
        Trainer(name=name)


def test_trainer_rejects_invalid_specialty():
    with pytest.raises(ValueError):
        Trainer(name="Alex", specialties=["", "Strength"])


@pytest.mark.parametrize(
    ("title", "description"),
    [
        ("", "Valid description"),
        ("Valid title", ""),
    ],
)
def test_business_policy_rejects_empty_text(title, description):
    with pytest.raises(ValueError):
        BusinessPolicy(title=title, description=description)
