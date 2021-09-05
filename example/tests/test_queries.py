from textwrap import dedent

import pytest

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
    query = dedent(
        f"""
        {{
            getPerson(id: "{person.graphql_id}") {{
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
            "id": person.graphql_id,
            "firstName": person.first_name,
            "lastName": person.last_name,
            "email": person.email,
            "organization": {
                "__typename": "Organization",
                "id": organization.graphql_id,
                "name": organization.name,
                "address": organization.address,
            },
        },
    )


@pytest.mark.django_db
def test_query_excluded_field_fails(person: Person, gclient: GraphQLClient):
    query = dedent(
        f"""
        {{
            getPerson(id: "{person.graphql_id}") {{
                __typename
                id
                secret
            }}
        }}
        """
    )
    response = gclient.query(query)
    assert response.status_code == 400
    gclient.assert_response_has_error_message(
        response, 'Cannot query field \\"secret\\" on type \\"Person\\".'
    )
