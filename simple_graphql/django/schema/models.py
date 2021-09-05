from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Type, Union

import graphene
from graphene_django import DjangoObjectType


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


@dataclass
class ModelSchema:
    ordering_options: Optional[graphene.Enum]
    node: Type[DjangoObjectType]
    query_fields: Dict[str, graphene.Field]
    mutation_fields: Dict[str, graphene.Field]
    subscription_fields: Dict[str, graphene.Field]
