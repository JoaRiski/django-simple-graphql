from typing import Type

from django.db.models import Model


def get_node_name(model_cls: Type[Model]) -> str:
    return f"{model_cls.__name__}"
