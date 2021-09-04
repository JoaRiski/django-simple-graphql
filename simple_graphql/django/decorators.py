from typing import Callable, Optional, Type, TypeVar

from django.db.models import Model

from simple_graphql.django.schema import ModelRegisterArgs, schema_builder

T = TypeVar("T", bound=Type[Model])


# TODO: Unpack model register args
def register_schema(*, args: Optional[ModelRegisterArgs] = None) -> Callable[[T], T]:
    def _model_wrapper(model_class: T) -> T:
        if not issubclass(model_class, Model):
            raise ValueError("Wrapped class must subclass Model.")

        schema_builder.register_model(model_class, args)

        return model_class

    return _model_wrapper
