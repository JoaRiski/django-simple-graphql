from simple_graphql.django.types import ModelClass


class AlreadyRegistered(Exception):
    def __init__(self, model_cls: ModelClass):
        super().__init__(
            f"Model {model_cls.__name__} "
            "has already been registered to the GraphQL schema"
        )


class SchemaAlreadyBuilt(Exception):
    pass
