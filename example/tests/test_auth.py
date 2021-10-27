from textwrap import dedent
from typing import Any

import pytest

from example.test_utils.client import GraphQLClient
from simple_graphql.auth.models import AuthenticationSession


@pytest.mark.django_db
def test_token_auth(session: AuthenticationSession, gclient: GraphQLClient):
    query = dedent(
        """
        mutation {
            getUserInfo(input: {}) {
                isAuthenticated
                username
            }
        }
        """
    )
    response = gclient.query(query)
    gclient.assert_response_has_no_errors(response)
    gclient.assert_first_result_matches_expected(
        response,
        {
            "isAuthenticated": False,
            "username": "",
        },
    )
    response = gclient.query(query, authorization=f"Token {session.key}")
    gclient.assert_response_has_no_errors(response)
    gclient.assert_first_result_matches_expected(
        response,
        {
            "isAuthenticated": True,
            "username": "admin",
        },
    )


@pytest.mark.django_db
def test_mutation_login(admin_user: Any, gclient: GraphQLClient):
    info_query = dedent(
        """
        mutation {
            getUserInfo(input: {}) {
                isAuthenticated
                username
            }
        }
        """
    )
    response = gclient.query(info_query)
    gclient.assert_response_has_no_errors(response)
    gclient.assert_first_result_matches_expected(
        response,
        {
            "isAuthenticated": False,
            "username": "",
        },
    )

    auth_query = dedent(
        """
        mutation {
            login(input: {username: "admin", password: "password"}) {
                authToken
            }
        }
        """
    )
    response = gclient.query(auth_query)
    gclient.assert_response_has_no_errors(response)
    token = gclient.get_single_query_result(response)["authToken"]

    response = gclient.query(info_query, authorization=f"Token {token}")
    gclient.assert_response_has_no_errors(response)
    gclient.assert_first_result_matches_expected(
        response,
        {
            "isAuthenticated": True,
            "username": "admin",
        },
    )
