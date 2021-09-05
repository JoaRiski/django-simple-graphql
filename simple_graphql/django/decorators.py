from dataclasses import fields
from typing import Callable, Optional, Union, cast

from django.db.models import Model
from graphql_relay import to_global_id

from simple_graphql.django.schema.builder import schema_builder
from simple_graphql.django.schema.utils import get_node_name
from simple_graphql.django.types import (
    ModelClass,
    ModelConfig,
    ModelSchemaConfig,
    ModelWithMeta,
)


# TODO: Move to a better location
def extract_schema_config(config: Optional[ModelConfig]) -> Optional[ModelSchemaConfig]:
    if not config:
        return None

    # TODO: Maybe add type validation (pydantic?)
    return ModelSchemaConfig(
        **{
            field.name: getattr(config, field.name, None)
            for field in fields(ModelSchemaConfig)
        }
    )


# TODO: Move to a better location
def get_model_graphql_meta(
    model_cls: Union[ModelClass, ModelWithMeta]
) -> Optional[ModelSchemaConfig]:
    if not hasattr(model_cls, "GraphQL"):
        return None
    # TODO: Remove the cast once mypy is more smart
    return extract_schema_config(cast(ModelWithMeta, model_cls).GraphQL)


# TODO: Move to a better location
def register_graphql_model(
    model_cls: Union[ModelClass, ModelWithMeta],
    config: Optional[ModelConfig] = None,
) -> None:

    # TODO: Make inclusion configurable, implicitly mutating model classes
    #       might not be a very nice thing to do
    model_cls.graphql_id = property(  # type: ignore
        lambda self: to_global_id(self.graphql_node_name, self.pk)
    )
    model_cls.graphql_node_name = get_node_name(model_cls)  # type: ignore

    merged_config = ModelSchemaConfig(
        **{
            **ModelSchemaConfig.to_dict(ModelSchemaConfig.get_defaults()),
            **(ModelSchemaConfig.to_dict(get_model_graphql_meta(model_cls))),
            **(ModelSchemaConfig.to_dict(extract_schema_config(config))),
        }
    )

    schema_builder.register_model(model_cls, merged_config)


# TODO: Return a properly typed class once intersections are supported.
#       See https://github.com/python/typing/issues/213
# TODO: Unpack model register args
def graphql_model(
    config: Optional[ModelConfig] = None,
) -> Callable[[ModelClass], ModelClass]:
    def _model_wrapper(model_cls: ModelClass) -> ModelClass:

        if not issubclass(model_cls, Model):
            raise ValueError("Wrapped class must subclass Model.")

        register_graphql_model(model_cls, config)
        return model_cls

    return _model_wrapper
