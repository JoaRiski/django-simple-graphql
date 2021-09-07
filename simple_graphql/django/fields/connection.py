from functools import partial
from typing import Any, Dict, List, Optional, Type, Union

import graphene
from django.db.models import QuerySet
from graphene.types.mountedtype import MountedType
from graphene.types.unmountedtype import UnmountedType
from graphene_django.filter import DjangoFilterConnectionField

from simple_graphql.django.search import order_qs, search_qs
from simple_graphql.django.types import ModelInstance


class DjangoAutoConnectionField(DjangoFilterConnectionField):
    search_fields: Optional[List[str]]
    ordering_options: Optional[graphene.Enum]

    def __init__(
        self,
        node_cls: Type[graphene.ObjectType],
        **kwargs: Union[UnmountedType, MountedType],
    ):

        extra_meta = getattr(node_cls, "ExtraMeta", None)
        self.search_fields = getattr(extra_meta, "search_fields", None)
        self.ordering_options = getattr(extra_meta, "ordering_options", None)

        if self.ordering_options:
            kwargs.setdefault("order_by", graphene.Argument(self.ordering_options))
        if self.search_fields:
            kwargs.setdefault("search_query", graphene.String())

        # graphene-django is shadowing "order_by", so we're skipping it's super
        # call by copying its initializaiton here
        self._fields = None
        self._provided_filterset_class = None
        self._filterset_class = None
        self._filtering_args = None
        self._extra_filter_meta = None
        self._base_args = None

        super(DjangoFilterConnectionField, self).__init__(node_cls, **kwargs)

    @classmethod
    def resolve_queryset(
        cls, connection, iterable, info, args: Dict[str, Any], *_args, **kwargs
    ) -> QuerySet[ModelInstance]:
        search_fields = kwargs.pop("search_fields", None)
        ordering_options = kwargs.pop("ordering_options", None)

        qs = super().resolve_queryset(
            connection, iterable, info, args, *_args, **kwargs
        )

        if search_fields:
            qs = search_qs(qs, search_fields, args.get("search_query", None))

        if ordering_options:
            ordering = args.get("order_by", None)
            qs = order_qs(qs, ordering)

        return qs

    def get_queryset_resolver(self):
        return partial(
            self.resolve_queryset,
            filterset_class=self.filterset_class,
            filtering_args=self.filtering_args,
            search_fields=self.search_fields,
            ordering_options=self.ordering_options,
        )
