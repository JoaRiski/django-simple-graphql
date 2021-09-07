from typing import (
    Any,
    Callable,
    Dict,
    Generic,
    Iterator,
    Optional,
    Tuple,
    Type,
    Union,
    cast,
)

import graphene
from django.db.models import Model
from graphql_relay import to_global_id

from simple_graphql.django.config import extract_schema_config, get_model_graphql_meta
from simple_graphql.django.schema.exceptions import (
    AlreadyRegistered,
    SchemaAlreadyBuilt,
)
from simple_graphql.django.schema.node import build_node_schema
from simple_graphql.django.schema.query import build_ordering_enum, build_query_fields
from simple_graphql.django.schema.utils import get_node_name
from simple_graphql.django.types import (
    ModelClass,
    ModelConfig,
    ModelSchema,
    ModelSchemaConfig,
    ModelWithMeta,
)


def build_model_schema(model_cls: ModelClass, args: ModelSchemaConfig) -> ModelSchema:
    ordering_options = build_ordering_enum(model_cls=model_cls, args=args)
    node = build_node_schema(
        model_cls=model_cls, args=args, ordering_options=ordering_options
    )
    query = build_query_fields(model_cls=model_cls, node_cls=node)
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


def attach_graphql_meta(
    model_cls: ModelClass,
) -> Union[ModelClass, Type[ModelWithMeta]]:
    # TODO: Remove casts once mypy supports intersection types
    # TODO: Make inclusion configurable, implicitly mutating model classes
    #       might not be a very nice thing to do
    cast(Any, model_cls).graphql_id = property(
        lambda self: to_global_id(self.graphql_node_name, self.pk)
    )
    cast(Any, model_cls).graphql_node_name = get_node_name(model_cls)
    return model_cls


class SchemaBuilder(Generic[ModelClass]):
    model_schemas: Optional[Dict[ModelClass, ModelSchema]]
    registry: Dict[ModelClass, ModelSchemaConfig]
    _schema: Optional[graphene.Schema]

    def __init__(self):
        self.model_schemas = None
        self._schema = None
        self.registry = dict()

    def register_model(
        self,
        model_cls: ModelClass,
        config: Optional[ModelConfig] = None,
    ) -> None:
        if self.model_schemas is not None:
            raise SchemaAlreadyBuilt(
                "The GraphQL schema has already been built and can no longer "
                "be modified. Ensure all models are registered before accessing"
                "the schema."
            )

        attach_graphql_meta(model_cls)
        merged_config = ModelSchemaConfig(
            **{
                **ModelSchemaConfig.to_dict(ModelSchemaConfig.get_defaults()),
                **(ModelSchemaConfig.to_dict(get_model_graphql_meta(model_cls))),
                **(ModelSchemaConfig.to_dict(extract_schema_config(config))),
            }
        )

        if model_cls in self.registry:
            raise AlreadyRegistered(model_cls)
        self.registry[model_cls] = merged_config

    def graphql_model(
        self, config: Optional[ModelConfig] = None
    ) -> Callable[[ModelClass], ModelClass]:
        def _model_wrapper(model_cls: ModelClass) -> ModelClass:

            if not issubclass(model_cls, Model):
                raise ValueError("Wrapped class must subclass Model.")

            self.register_model(model_cls, config)
            return model_cls

        return _model_wrapper

    def build_schemas(self) -> Dict[ModelClass, ModelSchema]:
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
        result = build_object_type("Mutation", self.mutation_fields_iter())
        return result if result._meta.fields else None

    def subscription_fields_iter(self) -> Iterator[Tuple[str, graphene.Field]]:
        for schema in self.build_schemas().values():
            for name, field in schema.subscription_fields.items():
                yield name, field

    def build_subscription(self) -> Optional[Type[graphene.ObjectType]]:
        result = build_object_type("Subscription", self.subscription_fields_iter())
        return result if result._meta.fields else None

    def build_schema(self) -> graphene.Schema:
        # noinspection PyTypeChecker
        return graphene.Schema(
            query=self.build_query(),
            mutation=self.build_mutation(),
            subscription=self.build_subscription(),
        )
