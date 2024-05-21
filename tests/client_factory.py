import pytest
from rest_framework.test import APIClient


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def auth_client(client, user):
    _, token = user
    client.credentials(HTTP_AUTHORIZATION="Token " + token.key)
    return client
