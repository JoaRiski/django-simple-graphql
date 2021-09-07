from simple_graphql.django import SchemaBuilder
from simple_graphql.django.types import ModelClass

schema_builder: SchemaBuilder = SchemaBuilder[ModelClass]()
schema = schema_builder.build_schema()
