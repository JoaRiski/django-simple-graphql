from textwrap import dedent

from example.test_utils.client import GraphQLClient


def test_mutation_addition(gclient: GraphQLClient):
    query = dedent(
        """
        mutation {
            addition(input: {a: 1, b: 2}) {
                result
            }
        }
        """
    )
    response = gclient.query(query)
    gclient.assert_response_has_no_errors(response)
    gclient.assert_first_result_matches_expected(
        response,
        {
            "result": 3,
        },
    )
