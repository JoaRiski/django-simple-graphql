from typing import Protocol, Type, TypeVar

from django.db.models import Model

ModelClass = TypeVar("ModelClass", bound=Type[Model])
ModelInstance = TypeVar("ModelInstance", bound=Model)


class GraphQLMetaClass(Protocol):
    pass


# TODO: Convert to a properly typed class once intersections are supported.
#       See https://github.com/python/typing/issues/213
class ModelWithMeta(Model):
    GraphQL: Type[GraphQLMetaClass]

    class Meta:
        abstract = True
