from dataclasses import asdict, dataclass
from typing import Dict, List, Optional, Type, Union

import graphene
from graphene_django import DjangoObjectType


@dataclass
class ModelSchemaConfig:
    filters: Optional[Union[Dict[str, List[str]], List[str]]]
    exclude_fields: Optional[List[str]]
    search_fields: Optional[List[str]]
    ordering_fields: Optional[List[str]]
    default_ordering: Optional[str]

    @classmethod
    def get_defaults(cls) -> "ModelSchemaConfig":
        return cls(
            filters=None,
            exclude_fields=None,
            search_fields=None,
            ordering_fields=None,
            default_ordering=None,
        )

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
