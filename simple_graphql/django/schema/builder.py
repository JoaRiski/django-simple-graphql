from typing import Dict, Iterator, Optional, Tuple, Type, cast

import graphene
from django.db.models import Model

from simple_graphql.django.schema.exceptions import AlreadyRegistered
from simple_graphql.django.schema.models import ModelSchema, ModelSchemaConfig
from simple_graphql.django.schema.node import build_node_schema
from simple_graphql.django.schema.query import build_ordering_enum, build_query_fields


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
    query = build_query_fields(
        model_cls=model_cls, node_cls=node, ordering_options=ordering_options, args=args
    )
    return ModelSchema(
        node=node,
        ordering_options=ordering_options,
        query_fields=query,
        mutation_fields=dict(),
        subscription_fields=dict(),
    )


def build_object_type(
    name: str, field_map: Iterator[Tuple[str, graphene.Field]]
) -> Type[graphene.ObjectType]:
    return cast(
        Type[graphene.ObjectType],
        type(
            name,
            (graphene.ObjectType,),
            {name: field for name, field in field_map},
        ),
    )


class SchemaBuilder:
    model_schemas: Optional[Dict[Type[Model], ModelSchema]] = None
    registry: Dict[Type[Model], Optional[ModelSchemaConfig]] = dict()

    def register_model(
        self, model_cls: Type[Model], config: Optional[ModelSchemaConfig]
    ):
        if model_cls in self.registry:
            raise AlreadyRegistered(model_cls)
        self.registry[model_cls] = config

    def build_schemas(self) -> Dict[Type[Model], ModelSchema]:
        if self.model_schemas is not None:
            return self.model_schemas
        model_schemas = dict()
        for model_cls, config in self.registry.items():
            model_schemas[model_cls] = build_model_schema(model_cls, config)
        self.model_schemas = model_schemas
        return model_schemas

    def query_fields_iter(self) -> Iterator[Tuple[str, graphene.Field]]:
        for schema in self.build_schemas().values():
            for name, field in schema.query_fields.items():
                yield name, field

    def build_query(self) -> Type[graphene.ObjectType]:
        return build_object_type("Query", self.query_fields_iter())

    def mutation_fields_iter(self) -> Iterator[Tuple[str, graphene.Field]]:
        for schema in self.build_schemas().values():
            for name, field in schema.mutation_fields.items():
                yield name, field

    def build_mutation(self) -> Optional[Type[graphene.ObjectType]]:
        return build_object_type("Mutation", self.query_fields_iter())

    def subscription_fields_iter(self) -> Iterator[Tuple[str, graphene.Field]]:
        for schema in self.build_schemas().values():
            for name, field in schema.subscription_fields.items():
                yield name, field

    def build_subscription(self) -> Optional[Type[graphene.ObjectType]]:
        return build_object_type("Subscription", self.query_fields_iter())

    def build_schema(self) -> graphene.Schema:
        # noinspection PyTypeChecker
        return graphene.Schema(
            query=self.build_query(),
            mutation=self.build_mutation(),
            subscription=self.build_subscription(),
        )


schema_builder = SchemaBuilder()


def build_schema() -> graphene.Schema:
    return schema_builder.build_schema()
