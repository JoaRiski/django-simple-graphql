from typing import Any, Callable

import pytest
from django.test.client import Client

from example.models import Organization, Person, Secret
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
def secret() -> Secret:
    return Secret.objects.create(data="hunter2")


@pytest.fixture
def gclient(client: Client) -> GraphQLClient:
    return GraphQLClient(client)


@pytest.fixture
def session(admin_user: Any) -> AuthenticationSession:
    return AuthenticationSession.create_for_user(admin_user)


@pytest.fixture
def disable_introspection_block(settings: Any) -> Callable[[bool], None]:
    def toggle(val: bool):
        settings.TEST_DISABLE_INTROSPECTION_BLOCK = val

    return toggle
