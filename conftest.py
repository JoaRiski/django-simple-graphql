from typing import Any

import pytest
from django.test.client import Client

from example.models import Organization, Person
from example.test_utils.client import GraphQLClient
from simple_graphql.auth.models import AuthenticationSession


@pytest.fixture
def organization() -> Organization:
    return Organization.objects.create(
        name="Test organization",
        address="Test street 123",
    )


@pytest.fixture
def person(organization: Organization) -> Person:
    return Person.objects.create(
        first_name="First Name",
        last_name="Last Name",
        email="firstname.lastname@example.com",
        secret="hunter2",
        organization=organization,
    )


@pytest.fixture
def gclient(client: Client) -> GraphQLClient:
    return GraphQLClient(client)


@pytest.fixture
def session(admin_user: Any) -> AuthenticationSession:
    return AuthenticationSession.create_for_user(admin_user)
