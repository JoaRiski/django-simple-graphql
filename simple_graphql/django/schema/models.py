from dataclasses import dataclass
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


@dataclass
class ModelSchema:
    ordering_options: Optional[graphene.Enum]
    node: Type[DjangoObjectType]
    query: Type[graphene.ObjectType]
