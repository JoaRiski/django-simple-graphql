from example.models import Organization, Person
from simple_graphql.django import schema_builder


def test_schema_config_parsing():
    person_config = schema_builder.registry.get(Person)
    assert person_config.exclude_fields == ["secret"]

    organization_config = schema_builder.registry.get(Organization)
    assert organization_config.default_ordering == "name"
