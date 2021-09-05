from typing import Dict, List, Optional, Type, TypeVar, Union

import graphene
from django.db.models import Model, QuerySet
from graphene import relay
from graphene.types.mountedtype import MountedType
from graphene.types.unmountedtype import UnmountedType
from graphene.utils.str_converters import to_snake_case
from graphene_django import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField

from simple_graphql.django.schema.models import ModelSchemaConfig

T = TypeVar("T", bound=Model)


class DjangoAutoConnectionField(DjangoFilterConnectionField):
    search_fields: Optional[List[str]]

    def __init__(
        self,
        node_cls: Type[graphene.ObjectType],
        search_fields: Optional[List[str]],
        ordering_options: Optional[graphene.Enum],
        **kwargs: Union[UnmountedType, MountedType],
    ):
        self.search_fields = search_fields

        if ordering_options:
            kwargs.setdefault("order_by", graphene.Argument(ordering_options))
        if search_fields:
            kwargs.setdefault("search_query", graphene.String())

        super().__init__(node_cls, **kwargs)

    @classmethod
    def resolve_queryset(cls, *args, **kwargs) -> QuerySet[T]:
        # TODO: Implement search
        # TODO: Implement ordering
        return super().resolve_queryset(*args, **kwargs)


def build_ordering_enum(
    *, model_cls: Type[Model], args: ModelSchemaConfig
) -> Optional[graphene.Enum]:
    if not args.ordering_fields:
        return None
    return graphene.Enum(
        f"{model_cls.__name__}Ordering",
        [
            (f"{x}_{direction}".upper(), x if direction == "asc" else f"-{x}")
            for x in (args.ordering_fields or [])
            for direction in ("asc", "desc")
        ],
    )


def build_query_fields(
    *,
    model_cls: Type[Model],
    node_cls: Type[DjangoObjectType],
    ordering_options: Optional[graphene.Enum],
    args: ModelSchemaConfig,
) -> Dict[str, graphene.Field]:
    query_name = to_snake_case(model_cls.__name__)
    return {
        f"get_{query_name}": relay.Node.Field(node_cls),
        f"list_{query_name}": DjangoAutoConnectionField(
            node_cls=node_cls,
            search_fields=args.search_fields,
            ordering_options=ordering_options,
        ),
    }
