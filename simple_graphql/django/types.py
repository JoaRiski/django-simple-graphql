from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Type, TypeVar, Union

import graphene
from django.db.models import Model
from graphene_django import DjangoObjectType

ModelClass = TypeVar("ModelClass", bound=Type[Model])
ModelInstance = TypeVar("ModelInstance", bound=Model)


@dataclass
class ModelSchemaConfig:
    filters: Optional[Union[Dict[str, List[str]], List[str]]] = None
    exclude_fields: Optional[List[str]] = None
    search_fields: Optional[List[str]] = None
    ordering_fields: Optional[List[str]] = None
    default_ordering: Optional[str] = None

    @classmethod
    def get_defaults(cls) -> "ModelSchemaConfig":
        return cls()

    @classmethod
    def to_dict(cls, instance: Optional["ModelSchemaConfig"]):
        if instance:
            return asdict(instance)
        return {}


ModelConfig = Union[Type, ModelSchemaConfig]


# TODO: Convert to a properly typed class once intersections are supported.
#       See https://github.com/python/typing/issues/213
class ModelWithMeta(Model):
    GraphQL: Type

    class Meta:
        abstract = True


@dataclass
class ModelSchema:
    ordering_options: Optional[graphene.Enum]
    node: Type[DjangoObjectType]
    query_fields: Dict[str, graphene.Field]
    mutation_fields: Dict[str, graphene.Field]
    subscription_fields: Dict[str, graphene.Field]
