import pytest
from django.test.client import Client
from pytest_django.plugin import _DatabaseBlocker

from example.models import Organization, Person
from example.test_utils.client import GraphQLClient


@pytest.fixture(scope="session")
def organization(
    django_db_setup: None, django_db_blocker: _DatabaseBlocker
) -> Organization:
    with django_db_blocker.unblock():
        return Organization.objects.create(
            name="Test organization",
            address="Test street 123",
        )


@pytest.fixture(scope="session")
def person(
    django_db_setup: None, django_db_blocker: _DatabaseBlocker, organization
) -> Person:
    with django_db_blocker.unblock():
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
