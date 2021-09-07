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


@pytest.mark.django_db
def test_query_search_query(gclient: GraphQLClient):
    org_a = Organization.objects.create(name="Foo", address="Foo street 123")
    org_b = Organization.objects.create(name="Bar", address="Bar street 123")
    query = dedent(
        """
        query ListOrganization($query: String) {
            listOrganization(searchQuery: $query) {
                edges {
                    node {
                        id
                    }
                }
            }
        }
        """
    )
    response = gclient.query(query, variables={"query": "Foo"})
    assert response.status_code == 200
    gclient.assert_query_result_node_ids_match(response, [org_a.graphql_id])

    response = gclient.query(query, variables={"query": "Bar"})
    assert response.status_code == 200
    gclient.assert_query_result_node_ids_match(response, [org_b.graphql_id])

    response = gclient.query(query, variables={"query": "street"})

    assert response.status_code == 200
    gclient.assert_query_result_node_ids_match(
        response,
        [
            org_b.graphql_id,
            org_a.graphql_id,
        ],
    )


@pytest.mark.django_db
def test_query_order_by(gclient: GraphQLClient):
    org_a = Organization.objects.create(name="Foo", address="Foo street 123")
    org_b = Organization.objects.create(name="Bar", address="Bar street 123")
    query = dedent(
        """
        query ListOrganization($ordering: OrganizationOrdering) {
            listOrganization(orderBy: $ordering) {
                edges {
                    node {
                        id
                    }
                }
            }
        }
        """
    )
    response = gclient.query(query, variables={"ordering": "NAME_ASC"})
    assert response.status_code == 200
    ids = gclient.get_node_ids(response)
    assert ids == [
        org_b.graphql_id,
        org_a.graphql_id,
    ]

    response = gclient.query(query, variables={"ordering": "NAME_DESC"})

    assert response.status_code == 200
    ids = gclient.get_node_ids(response)
    assert ids == [
        org_a.graphql_id,
        org_b.graphql_id,
    ]
