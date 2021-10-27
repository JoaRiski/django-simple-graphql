import graphene
from graphene import relay

from simple_graphql.django import Schema

schema = Schema()


@schema.graphql_mutation("addition")
class AdditionMutation(relay.ClientIDMutation):
    class Input:
        a = graphene.Int(required=True)
        b = graphene.Int(required=True)

    result = graphene.Int(required=True)

    @classmethod
    def mutate_and_get_payload(cls, root, info, a: int, b: int):
        return AdditionMutation(result=a + b)
