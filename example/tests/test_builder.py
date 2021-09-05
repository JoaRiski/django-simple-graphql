from example.models import Person
from simple_graphql.django import schema_builder


def test_schema_config_parsing():
    config = schema_builder.registry.get(Person)
    assert config.exclude_fields == ["secret"]
