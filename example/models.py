from django.db import models

from simple_graphql.django import (
    ModelSchemaConfig,
    graphql_model,
    register_graphql_model,
)


class Organization(models.Model):
    graphql_id: str
    graphql_node_name: str

    name = models.TextField()
    address = models.TextField()


class OrganizationGraphQLConfig:
    pass


register_graphql_model(Organization, ModelSchemaConfig(default_ordering="name"))


@graphql_model()
class Person(models.Model):
    graphql_id: str
    graphql_node_name: str

    first_name = models.TextField()
    last_name = models.TextField()
    email = models.TextField()
    secret = models.TextField()
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)

    class GraphQL:
        exclude_fields = ["secret"]
