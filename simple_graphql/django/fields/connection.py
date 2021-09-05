from typing import List, Optional, Type, Union

import graphene
from django.db.models import QuerySet
from graphene.types.mountedtype import MountedType
from graphene.types.unmountedtype import UnmountedType
from graphene_django.filter import DjangoFilterConnectionField

from simple_graphql.django.types import ModelInstance


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
    def resolve_queryset(cls, *args, **kwargs) -> QuerySet[ModelInstance]:
        # TODO: Implement search
        # TODO: Implement ordering
        return super().resolve_queryset(*args, **kwargs)
