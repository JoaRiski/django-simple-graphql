from typing import Any

import graphene
from graphene import relay

from simple_graphql.auth.mutations import LoginMutation
from simple_graphql.django import Schema

schema = Schema()


@schema.graphql_mutation("addition")
class AdditionMutation(relay.ClientIDMutation):
    class Input:
        a = graphene.Int(required=True)
        b = graphene.Int(required=True)

    result = graphene.Int(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: Any, a: int, b: int):
        return AdditionMutation(result=a + b)


@schema.graphql_mutation("get_user_info")
class GetUserInfoMutation(relay.ClientIDMutation):
    is_authenticated = graphene.Boolean(required=True)
    username = graphene.String(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root: Any, info: Any):
        return GetUserInfoMutation(
            is_authenticated=info.context.user.is_authenticated,
            username=info.context.user.username,
        )


schema.register_mutation("login", LoginMutation.Field())
