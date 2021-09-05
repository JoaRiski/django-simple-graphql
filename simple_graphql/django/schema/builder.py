from typing import Dict, Optional, Type

from django.db.models import Model

from simple_graphql.django.schema.exceptions import AlreadyRegistered
from simple_graphql.django.schema.models import ModelSchema, ModelSchemaConfig
from simple_graphql.django.schema.node import build_node_schema
from simple_graphql.django.schema.query import build_ordering_enum, build_query_schema


def build_model_schema(
    model_cls: Type[Model], args: Optional[ModelSchemaConfig]
) -> ModelSchema:
    args = args or ModelSchemaConfig(
        filters=[],
        exclude_fields=[],
        search_fields=[],
        ordering_fields=[],
        default_ordering=None,
    )
    node = build_node_schema(model_cls=model_cls, args=args)
    ordering_options = build_ordering_enum(model_cls=model_cls, args=args)
    query = build_query_schema(
        model_cls=model_cls, node_cls=node, ordering_options=ordering_options, args=args
    )
    return ModelSchema(
        ordering_options=ordering_options,
        query=query,
        node=node,
    )


class SchemaBuilder:
    registry: Dict[Type[Model], ModelSchema]

    def register_model(self, model_cls: Type[Model], args: Optional[ModelSchemaConfig]):
        if model_cls in self.registry:
            raise AlreadyRegistered(model_cls)
        schema = build_model_schema(model_cls, args)
        self.registry[model_cls] = schema


schema_builder = SchemaBuilder()
