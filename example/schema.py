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


@schema.graphql_query("math")
class Math(graphene.ObjectType):
    add = graphene.Field(
        graphene.NonNull(graphene.Int),
        a=graphene.NonNull(graphene.Int),
        b=graphene.NonNull(graphene.Int),
    )
    substract = graphene.Field(
        graphene.NonNull(graphene.Int),
        a=graphene.NonNull(graphene.Int),
        b=graphene.NonNull(graphene.Int),
    )

    def resolve_add(self, info: Any, a: int, b: int, **kwargs: Any) -> int:
        return a + b

    def resolve_substract(self, info: Any, a: int, b: int, **kwargs: Any) -> int:
        return a - b


class Echo(graphene.ObjectType):
    ping = graphene.Field(
        graphene.NonNull(graphene.String), input=graphene.NonNull(graphene.String)
    )

    def resolve_ping(self, info: Any, input: str, **kwargs: Any) -> str:
        if input == "ping":
            return "pong"
        return input


schema.register_mutation("login", LoginMutation.Field())
schema.register_query(
    "echo", graphene.Field(Echo, required=True), lambda *args, **kwargs: Echo()
)
