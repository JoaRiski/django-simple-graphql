import pytest
from django.contrib.auth import get_user_model

from example.models import Organization, Person
from example.schema import schema_builder
from simple_graphql.django import SchemaBuilder
from simple_graphql.django.schema.exceptions import SchemaAlreadyBuilt

User = get_user_model()


def test_schema_config_loading():
    person_config = schema_builder.registry.get(Person)
    assert person_config.exclude_fields == ["secret"]

    organization_config = schema_builder.registry.get(Organization)
    assert organization_config.default_ordering == "name"

    user_config = schema_builder.registry.get(User)
    assert user_config.exclude_fields == ["password"]


def test_schema_post_build_registering_errors():
    builder = SchemaBuilder()
    schema = builder.build_schema()

    # Registering should be fine before the schema gets evaluated
    builder.register_model(Person)

    # Registering should fail once the schema has been evaluated
    # Asserting on the schema will evaluate it
    assert schema
    with pytest.raises(SchemaAlreadyBuilt):
        builder.register_model(Organization)
