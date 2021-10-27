import pytest
from graphql.language import ast

from simple_graphql.django.fields import GlobalIDInput


@pytest.mark.parametrize(
    "unparsed, parsed", [["Rm9vOjQyMA==", "420"], ["QmFyOmh1bnRlcjI=", "hunter2"]]
)
def test_global_id_input_parse_value(unparsed, parsed):
    scalar = GlobalIDInput()
    assert scalar.parse_value(unparsed) == parsed


@pytest.mark.parametrize(
    "unparsed, parsed", [["Rm9vOjQyMA==", "420"], ["QmFyOmh1bnRlcjI=", "hunter2"]]
)
def test_global_id_input_parse_literal(unparsed, parsed):
    scalar = GlobalIDInput()
    assert scalar.parse_literal(ast.StringValue(unparsed)) == parsed


# TODO: Improve once behavior is decided upon
def test_global_id_input_parse_literal_not_string():
    scalar = GlobalIDInput()
    scalar.parse_literal(ast.IntValue("42"))


def test_global_id_input_serialize():
    scalar = GlobalIDInput()
    with pytest.raises(
        NotImplementedError, match="GlobalIDInput supports no serialization"
    ):
        scalar.serialize(None)
