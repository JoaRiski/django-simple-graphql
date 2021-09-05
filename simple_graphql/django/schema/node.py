from typing import Any, Protocol, Type

from django.db.models import Model, QuerySet
from graphene import relay
from graphene_django import DjangoObjectType

from simple_graphql.django.schema.models import ModelSchemaConfig

# TODO: Delete and replace types relying on this
TypeLater = Any


def build_node_meta(model_cls: Type[Model], args: ModelSchemaConfig) -> Type:
    class Meta:
        model = model_cls
        filter_fields = args.filters or []
        exclude_fields = args.exclude_fields or []
        interfaces = (relay.Node,)

    return Meta


class GetQueryset(Protocol):
    # noinspection PyMethodParameters
    def __call__(
        self, cls: DjangoObjectType, queryset: QuerySet[TypeLater], info: TypeLater
    ) -> QuerySet[TypeLater]:
        ...


def build_node_get_queryset(
    model_cls: Type[Model], args: ModelSchemaConfig
) -> GetQueryset:
    default_ordering = args.default_ordering or "-pk"

    # noinspection PyDecorator
    @classmethod  # type: ignore
    def get_queryset(
        cls: DjangoObjectType, queryset: QuerySet[TypeLater], info: TypeLater
    ) -> QuerySet[TypeLater]:
        # TODO: Check if this is a valid way to handle related managers
        if not hasattr(queryset, "query"):
            return queryset
        is_ordered = bool(queryset.query.order_by)
        if is_ordered:
            return queryset
        else:
            return queryset.order_by(default_ordering)

    return get_queryset


def build_node_schema(
    model_cls: Type[Model], args: ModelSchemaConfig
) -> Type[DjangoObjectType]:
    meta = build_node_meta(model_cls, args)

    class AutoNode(DjangoObjectType):
        Meta = meta
        get_queryset = build_node_get_queryset(model_cls, args)

    AutoNode.__name__ = f"{model_cls.__name__}AutoNode"
    return AutoNode
