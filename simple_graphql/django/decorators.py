from typing import Callable, Optional, Type, TypeVar

from django.db.models import Model
from graphql_relay import to_global_id

from simple_graphql.django.schema.builder import ModelSchemaConfig, schema_builder
from simple_graphql.django.schema.utils import get_node_name

T = TypeVar("T", bound=Type[Model])
T_co = TypeVar("T_co", bound=Type[Model], covariant=True)


# TODO: Return a properly typed class once intersections are supported.
#       See https://github.com/python/typing/issues/213
# TODO: Unpack model register args
def register_schema(*, args: Optional[ModelSchemaConfig] = None) -> Callable[[T], T]:
    def _model_wrapper(model_class: T) -> T:

        if not issubclass(model_class, Model):
            raise ValueError("Wrapped class must subclass Model.")

        schema_builder.register_model(model_class, args)

        # TODO: Make inclusion configurable
        model_class.graphql_id = property(  # type: ignore
            lambda self: to_global_id(self.graphql_node_name, self.pk)
        )
        model_class.graphql_node_name = get_node_name(model_class)  # type: ignore

        return model_class

    return _model_wrapper
