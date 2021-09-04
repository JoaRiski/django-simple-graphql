from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Type, Union

from django.db.models import Model

# TODO: Delete and replace types relying on this
TypeLater = Any


@dataclass
class ModelRegisterArgs:
    filters: Optional[Union[Dict[str, List[str]], List[str]]]
    exclude_fields: Optional[List[str]]
    search_fields: Optional[List[str]]
    ordering_fields: Optional[List[str]]
    default_ordering: Optional[str]
    extra_queries: Optional[List[TypeLater]]


def build_model_schema(
    model_cl: Type[Model], args: Optional[ModelRegisterArgs]
) -> TypeLater:
    raise NotImplementedError()


class AlreadyRegistered(Exception):
    pass


class SchemaBuilder:
    registry: Dict[Type[Model], TypeLater]

    def register_model(self, model_cls: Type[Model], args: Optional[ModelRegisterArgs]):
        if model_cls in self.registry:
            raise AlreadyRegistered(
                f"Model {model_cls.__name__} has already been registered"
            )
        schema = build_model_schema(model_cls, args)
        self.registry[model_cls] = schema


schema_builder = SchemaBuilder()
