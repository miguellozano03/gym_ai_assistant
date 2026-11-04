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
    assert tools_by_name["get_business_information"].invoke({})["name"] == "Extreme Gym"
    assert tools_by_name["get_products"].invoke({})
