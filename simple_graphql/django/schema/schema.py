import copy
from typing import Any, Callable, Dict, Optional, Type, cast

import graphene
from django.utils.functional import LazyObject

from ..types import ModelClass, ModelConfig
from .builder import SchemaBuilder


class _Schema(LazyObject):
    builder: SchemaBuilder

    def __init__(self, builder: Optional[SchemaBuilder] = None):
        if builder is None:
            builder = SchemaBuilder[ModelClass]()
        self.__dict__["builder"] = builder
        super().__init__()

    def register_model(
        self,
        model_cls: ModelClass,
        config: Optional[ModelConfig] = None,
    ) -> None:
        self.builder.register_model(model_cls, config)

    def graphql_model(
        self, config: Optional[ModelConfig] = None
    ) -> Callable[[ModelClass], ModelClass]:
        return self.builder.graphql_model(config)

    def _setup(self):
        self._wrapped = self.builder.build_schema()

    def __copy__(self) -> "_Schema":
        # We have to use type(self), not self.__class__, because the
        # latter is proxied.
        return type(self)(self.builder)

    def __deepcopy__(self, memo: Dict[Any, Any]) -> "_Schema":
        # We have to use type(self), not self.__class__, because the
        # latter is proxied.
        # noinspection PyArgumentList
        result = type(self)(copy.deepcopy(self.builder, memo))
        memo[id(self)] = result
        return result


# Stupid hacks to get mypy working properly
# noinspection PyMissingConstructor
class SchemaType(graphene.Schema):
    def __init__(self):
        ...

    def register_model(
        self,
        model_cls: ModelClass,
        config: Optional[ModelConfig] = None,
    ):
        ...

    def graphql_model(
        self, config: Optional[ModelConfig] = None
    ) -> Callable[[ModelClass], ModelClass]:
        ...


Schema: Type[SchemaType] = cast(Type[SchemaType], _Schema)
