from typing import Any, Protocol, Type, Union

from django.db.models import QuerySet
from django.http import HttpRequest
from graphene import relay
from graphene_django import DjangoObjectType

from simple_graphql.django.schema.utils import get_node_name
from simple_graphql.django.types import ModelClass, ModelInstance, ModelSchemaConfig


class InfoProto(Protocol):
    context: HttpRequest


# TODO: Change to an intersection type once supported
QueryInfo = Union[Any, InfoProto]


def build_node_meta(model_cls: ModelClass, args: ModelSchemaConfig) -> Type:
    class Meta:
        model = model_cls
        name = get_node_name(model_cls)
        filter_fields = args.filters or []
        exclude = args.exclude_fields or []
        interfaces = (relay.Node,)

    return Meta


class GetQueryset(Protocol):
    # noinspection PyMethodParameters
    def __call__(
        self, cls: DjangoObjectType, queryset: QuerySet[ModelInstance], info: QueryInfo
    ) -> QuerySet[ModelInstance]:
        ...


def build_node_get_queryset(
    model_cls: ModelClass, args: ModelSchemaConfig
) -> GetQueryset:
    default_ordering = args.default_ordering or "-pk"

    # noinspection PyDecorator
    @classmethod  # type: ignore
    def get_queryset(
        cls: DjangoObjectType, queryset: QuerySet[ModelInstance], info: QueryInfo
    ) -> QuerySet[ModelInstance]:
        # TODO: Check if this is a valid way to handle related managers.
        #       Related managers have no "query" attribute, but should still be
        #       handled somehow most likely.
        if not hasattr(queryset, "query"):
            return queryset
        is_ordered = bool(queryset.query.order_by)
        if is_ordered:
            return queryset
        else:
            return queryset.order_by(default_ordering)

    return get_queryset


def build_node_schema(
    model_cls: ModelClass, args: ModelSchemaConfig
) -> Type[DjangoObjectType]:
    meta = build_node_meta(model_cls, args)

    class AutoNode(DjangoObjectType):
        Meta = meta
        get_queryset = build_node_get_queryset(model_cls, args)

    AutoNode.__name__ = get_node_name(model_cls)
    return AutoNode
