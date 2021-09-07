from django.contrib.auth import get_user_model

from example.models import Organization, Person
from example.schema import schema_builder

User = get_user_model()


def test_schema_config_loading():
    person_config = schema_builder.registry.get(Person)
    assert person_config.exclude_fields == ["secret"]

    organization_config = schema_builder.registry.get(Organization)
    assert organization_config.default_ordering == "name"

    user_config = schema_builder.registry.get(User)
    assert user_config.exclude_fields == ["password"]
