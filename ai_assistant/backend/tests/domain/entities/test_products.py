import pytest
from decimal import Decimal
from app.domain.entities.gym_offerings import Product, MemberShipPlan


def test_create_new_product():
    water = Product(
        name="Water 500 ml",
        description="Bottle of water",
        price=Decimal(2000),
        available=True
    )

    assert water.name == "Water 500 ml"


def test_create_membership_plan():
    membership_plan = MemberShipPlan(
        name="Daily",
        description="Pay once, workout once",
        price=Decimal(4000),
        duration_days=1
    )

    assert membership_plan.name == "Daily"


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("name", ""),
        ("price", Decimal("-1")),
    ],
)
def test_product_rejects_invalid_values(field, value):
    data = {
        "name": "Water 500 ml",
        "description": None,
        "price": Decimal("2000"),
        "available": True,
    }
    data[field] = value

    with pytest.raises(ValueError):
        Product(**data)


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("name", " "),
        ("price", Decimal("-1")),
        ("duration_days", 0),
    ],
)
def test_membership_plan_rejects_invalid_values(field, value):
    data = {
        "name": "Daily",
        "description": None,
        "price": Decimal("4000"),
        "duration_days": 1,
    }
    data[field] = value

    with pytest.raises(ValueError):
        MemberShipPlan(**data)