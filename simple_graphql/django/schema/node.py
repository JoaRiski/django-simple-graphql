from typing import Any, Protocol, Type, TypeVar, Union

from django.db.models import Model, QuerySet
from django.http import HttpRequest
from graphene import relay
from graphene_django import DjangoObjectType

from simple_graphql.django.schema.models import ModelSchemaConfig
from simple_graphql.django.schema.utils import get_node_name

T = TypeVar("T", bound=Model)


class InfoProto(Protocol):
    context: HttpRequest


# TODO: Change to an intersection type once supported
QueryInfo = Union[Any, InfoProto]


def build_node_meta(model_cls: Type[T], args: ModelSchemaConfig) -> Type:
    class Meta:
        model = model_cls
        name = get_node_name(model_cls)
        filter_fields = args.filters or []
        exclude_fields = args.exclude_fields or []
        interfaces = (relay.Node,)

    return Meta


class GetQueryset(Protocol):
    # noinspection PyMethodParameters
    def __call__(
        self, cls: DjangoObjectType, queryset: QuerySet[T], info: QueryInfo
    ) -> QuerySet[T]:
        ...


def build_node_get_queryset(
    model_cls: Type[Model], args: ModelSchemaConfig
) -> GetQueryset:
    default_ordering = args.default_ordering or "-pk"

    # noinspection PyDecorator
    @classmethod  # type: ignore
    def get_queryset(
        cls: DjangoObjectType, queryset: QuerySet[T], info: QueryInfo
    ) -> QuerySet[T]:
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
    model_cls: Type[Model], args: ModelSchemaConfig
) -> Type[DjangoObjectType]:
    meta = build_node_meta(model_cls, args)

    class AutoNode(DjangoObjectType):
        Meta = meta
        get_queryset = build_node_get_queryset(model_cls, args)

    AutoNode.__name__ = get_node_name(model_cls)
    return AutoNode
