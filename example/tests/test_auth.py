from textwrap import dedent

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
