from simple_graphql.django import build_schema


def test_schema_building() -> None:
    from example.models import Organization, Person  # noqa: F401

    schema = build_schema()
    assert schema
