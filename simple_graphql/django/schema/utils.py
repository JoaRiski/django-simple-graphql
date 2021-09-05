from typing import Type, TypeVar

from django.db.models import Model

T = TypeVar("T", bound=Model)


def get_node_name(model_cls: Type[T]) -> str:
    return f"{model_cls.__name__}"
