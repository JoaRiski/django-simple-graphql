from django.contrib.auth import get_user_model
from django.db import models

from simple_graphql.django import (
    ModelSchemaConfig,
    graphql_model,
    register_graphql_model,
)

User = get_user_model()
register_graphql_model(
    User,
    ModelSchemaConfig(
        exclude_fields=["password"],
    ),
)


class Organization(models.Model):
    graphql_id: str
    graphql_node_name: str

    name = models.TextField()
    address = models.TextField()


class OrganizationGraphQLConfig:
    default_ordering = "name"


register_graphql_model(Organization, OrganizationGraphQLConfig)


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
