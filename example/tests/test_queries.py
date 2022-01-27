from textwrap import dedent
from typing import Callable

import pytest
from django.contrib.auth.models import User

from example.models import Organization, Person, Secret, SuperuserOnlyModel
from example.test_utils.client import GraphQLClient
from example.test_utils.introspection import get_introspection_query
from simple_graphql.auth.models import AuthenticationSession


@pytest.mark.parametrize("allowed", (False, True))
def test_introspection(
    disable_introspection_block: Callable[[bool], None],
    gclient: GraphQLClient,
    allowed: bool,
) -> None:
    disable_introspection_block(allowed)
    query = get_introspection_query()
    response = gclient.query(query)
    assert response.status_code == 200
    if allowed:
        gclient.assert_response_has_no_errors(response)
    else:
        gclient.assert_response_has_error_message(
            response, "Introspection is not allowed"
        )


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


@pytest.mark.django_db
def test_query_login_required(
    secret: Secret, session: AuthenticationSession, gclient: GraphQLClient
):
    get_query = dedent(
        f"""
        {{
            getSecret(id: "{secret.graphql_id}") {{
                __typename
                id
                data
            }}
        }}
        """
    )
    list_query = dedent(
        """
        {
            listSecret {
                edges {
                    node {
                        __typename
                        id
                        data
                    }
                }
            }
        }
        """
    )

    for query in (get_query, list_query):
        response = gclient.query(query)
        assert response.status_code == 200
        gclient.assert_response_has_error_message(response, "Unauthorized")

    expected = {
        "__typename": "Secret",
        "data": secret.data,
        "id": secret.graphql_id,
    }
    for query, is_list in ((get_query, False), (list_query, True)):
        response = gclient.query(query, authorization=f"Token {session.key}")
        assert response.status_code == 200
        gclient.assert_response_has_no_errors(response)
        if is_list:
            gclient.assert_first_result_matches_expected(
                response, {"edges": [{"node": expected}]}
            )
        else:
            gclient.assert_first_result_matches_expected(response, expected)


def test_query_manually_registered(gclient: GraphQLClient):
    query = dedent(
        """
        query {
          math {
            add(a: 5, b: 2)
            substract(a: 8, b: 4)
          }
          echo {
            ping(input: "ping")
          }
        }
        """
    )
    response = gclient.query(query)
    assert response.status_code == 200
    gclient.assert_response_has_no_errors(response)
    gclient.assert_response_matches_expected(
        response,
        {
            "math": {
                "add": 7,
                "substract": 4,
            },
            "echo": {
                "ping": "pong",
            },
        },
    )


@pytest.mark.django_db
@pytest.mark.parametrize("is_superuser", (False, True))
def test_superuser_only_query(
    is_superuser: bool, admin_user: User, gclient: GraphQLClient
) -> None:
    admin_user.is_superuser = is_superuser
    admin_user.save()
    session = AuthenticationSession.create_for_user(admin_user)
    som = SuperuserOnlyModel.objects.create(data="test")
    get_query = dedent(
        f"""
        {{
            getSuperuserOnlyModel(id: "{som.graphql_id}") {{
                __typename
                id
                data
            }}
        }}
        """
    )
    list_query = dedent(
        """
        {
            listSuperuserOnlyModel {
                edges {
                    node {
                        __typename
                        id
                        data
                    }
                }
            }
        }
        """
    )

    expected = {
        "__typename": "SuperuserOnlyModel",
        "data": som.data,
        "id": som.graphql_id,
    }
    for query, is_list in ((get_query, False), (list_query, True)):
        response = gclient.query(query, authorization=f"Token {session.key}")
        assert response.status_code == 200
        gclient.assert_response_has_no_errors(response)
        if is_superuser:
            if is_list:
                gclient.assert_first_result_matches_expected(
                    response, {"edges": [{"node": expected}]}
                )
            else:
                gclient.assert_first_result_matches_expected(response, expected)
        else:
            gclient.assert_query_result_is_empty(response)
