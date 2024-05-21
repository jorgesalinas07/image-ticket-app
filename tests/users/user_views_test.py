import pytest
from rest_framework.authtoken.models import Token
from rest_framework import status

from apps.users.types import LoginSuccessResponse, SignUpSuccessResponse

endpoint = "/users"

## Replace test with auth client to test authenticated endpoints


def test_login_endpoint_should_return_200_status_when_login_successful(client, user):
    response = client.post(
        f"{endpoint}/login/", {"username": "testuser", "password": "test_pass"}
    )
    assert isinstance(response, LoginSuccessResponse)
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.json()
    assert "user" in response.json()


@pytest.mark.django_db
def test_login_endpoint_should_return_404_status_when_user_note_found(client):
    response = client.post(
        f"{endpoint}/login/", {"username": "testuser", "password": "test_pass"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND


def test_login_endpoint_should_return_404_status_when_password_is_invalid(client, user):
    response = client.post(
        f"{endpoint}/login/", {"username": "testuser", "password": "invalid_pass"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"error": "Invalid password"}


@pytest.mark.django_db
def test_signup_endpoint_should_return_201_status_when_user_creation_was_successful(
    client,
):
    response = client.post(
        f"{endpoint}/signup/",
        {
            "username": "newuser",
            "password": "new_pass",
            "email": "newuser@example.com",
            "first_name": "test_first_name",
            "last_name": "test_last_name",
        },
    )
    assert isinstance(response, SignUpSuccessResponse)
    assert response.status_code == status.HTTP_201_CREATED
    assert "token" in response.json()
    assert "user" in response.json()
    assert response.json()["user"]["username"] == "newuser"
    assert response.json()["user"]["email"] == "newuser@example.com"
    assert response.json()["user"]["first_name"] == "test_first_name"
    assert response.json()["user"]["last_name"] == "test_last_name"


@pytest.mark.django_db
def test_signup_endpoint_should_return_400_status_when_user_invalid_form(client):
    response = client.post(f"{endpoint}/signup/", {"username": "newuser"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_test_token_should_return_200_status_when_authentication_was_successful(
    client, user
):
    token = Token.objects.get(user__username="testuser")
    client.credentials(HTTP_AUTHORIZATION="token " + token.key)
    response = client.get(f"{endpoint}/test_token/")
    assert response.status_code == status.HTTP_200_OK
    assert response.content.decode().strip('"') == "Passed for testuser"
    client.credentials()
