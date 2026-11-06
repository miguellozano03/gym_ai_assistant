from app.infrastructure.ai.tools import create_gym_tools


def test_create_gym_tools_returns_repository_backed_tools():
    tools = create_gym_tools()
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
