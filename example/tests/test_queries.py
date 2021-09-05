from textwrap import dedent

import pytest
from graphql_relay import to_global_id

from example.models import Organization, Person
from example.test_utils.client import GraphQLClient
from example.test_utils.introspection import get_introspection_query


def test_introspection(gclient: GraphQLClient) -> None:
    query = get_introspection_query()
    response = gclient.query(query)
    assert response.status_code == 200
    gclient.assert_response_has_no_errors(response)


@pytest.mark.django_db
def test_query(
    person: Person, organization: Organization, gclient: GraphQLClient
) -> None:
    person_id = to_global_id("Person", person.pk)
    query = dedent(
        f"""
        {{
            getPerson(id: "{person_id}") {{
                __typename
                id
                firstName
                lastName
                email
                organization {{
                    __typename
                    id
                    name
                    address
                }}
            }}
        }}
        """
    )
    response = gclient.query(query)
    assert response.status_code == 200
    gclient.assert_response_has_no_errors(response)
    gclient.assert_first_result_matches_expected(
        response,
        {
            "__typename": "Person",
            "id": person_id,
            "firstName": person.first_name,
            "lastName": person.last_name,
            "email": person.email,
            "organization": {
                "__typename": "Organization",
                "id": to_global_id("Organization", organization.pk),
                "name": organization.name,
                "address": organization.address,
            },
        },
    )
