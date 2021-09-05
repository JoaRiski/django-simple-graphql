from typing import Type

from django.db.models import Model


class AlreadyRegistered(Exception):
    def __init__(self, model_cls: Type[Model]):
        super().__init__(
            f"Model {model_cls.__name__} "
            "has already been registered to the GraphQL schema"
        )
