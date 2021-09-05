from simple_graphql.django import build_schema


def test_schema_building() -> None:
    schema = build_schema()
    assert schema

    expected_queries = (
        "getOrganization",
        "listOrganization",
        "getPerson",
        "listPerson",
        "getUser",
        "listUser",
    )

    query = schema.get_query_type()
    assert len(query.fields) == len(expected_queries)
    for field_name in expected_queries:
        assert field_name in query.fields
