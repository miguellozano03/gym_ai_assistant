from decimal import Decimal

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.infrastructure.ai.tools import create_gym_tools
from app.infrastructure.persistence.database import Base
from app.infrastructure.persistence.models import Business, Product


def test_create_gym_tools_returns_repository_backed_tools():
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine)

    with session_factory() as session:
        business = Business(
            name="Extreme Gym",
            description="Gimnasio de prueba.",
        )
        session.add(business)
        session.flush()
        session.add(
            Product(
                business_id=business.id,
                name="Agua mineral",
                price=Decimal("1500"),
                available=True,
                description="Botella de agua.",
            )
        )
        session.commit()

    try:
        tools = create_gym_tools(session_factory)
        tools_by_name = {tool.name: tool for tool in tools}

        assert set(tools_by_name) == {
            "get_business_information",
            "get_business_hours",
            "get_gym_policies",
            "get_trainers",
            "get_products",
            "get_membership_plans",
        }
        business_result = tools_by_name["get_business_information"].invoke({})
        assert isinstance(business_result, str)
        assert "Extreme Gym" in business_result

        products_result = tools_by_name["get_products"].invoke({})
        assert isinstance(products_result, str)
        assert "Agua mineral" in products_result
    finally:
        engine.dispose()
