from app.infrastructure.persistence.models import Business, BusinessPolicy


def test_business_policy_relationship_is_bidirectional():
    business = Business(name="Extreme Gym")
    policy = BusinessPolicy(
        title="Cancellation",
        description="Cancel with 24 hours notice.",
    )

    business.policies.append(policy)

    assert policy.business is business
    assert policy in business.policies
