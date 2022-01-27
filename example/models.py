from typing import Any

from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import QuerySet

from example.schema import schema
from simple_graphql.django import ModelSchemaConfig

User = get_user_model()
schema.register_model(
    User,
    ModelSchemaConfig(
        exclude_fields=["password"],
    ),
)


class OrganizationGraphQLConfig:
    default_ordering = "name"
    search_fields = ["name", "address"]
    ordering_fields = ["name", "address"]


@schema.graphql_model(OrganizationGraphQLConfig)
class Organization(models.Model):
    graphql_id: str
    graphql_node_name: str

    name = models.TextField()
    address = models.TextField()


@schema.graphql_model()
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
        search_fields = ["first_name", "last_name", "email"]
        ordering_fields = ["first_name", "last_name", "email"]


@schema.graphql_model()
class Secret(models.Model):
    graphql_id: str
    graphql_node_name: str

    data = models.TextField()

    class GraphQL:
        require_login = True


@schema.graphql_model()
class SuperuserOnlyModel(models.Model):
    graphql_id: str
    graphql_node_name: str

    data = models.TextField()

    class GraphQL:
        @staticmethod
        def get_queryset(queryset: QuerySet["SuperuserOnlyModel"], info: Any):
            if info.context.user.is_superuser:
                return queryset
            return queryset.none()
