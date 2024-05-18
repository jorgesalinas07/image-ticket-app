import pytest
from django.test import Client
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User

@pytest.fixture
def client():
    return Client()

@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', password='testpass')
    Token.objects.create(user=user)
    return user

def test_login(client, user):
    response = client.post('/login/', {'username': 'testuser', 'password': 'testpass'})
    assert response.status_code == 200
    assert 'token' in response.json()
    assert 'user' in response.json()

def test_signup(client):
    response = client.post('/signup/', {'username': 'newuser', 'password': 'newpass', 'email': 'newuser@example.com'})
    assert response.status_code == 201
    assert 'token' in response.json()
    assert 'user' in response.json()

def test_test_token(client, user):
    token = Token.objects.get(user__username='testuser')
    client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
    response = client.get('/test_token/')
    assert response.status_code == 200
    assert response.content.decode() == 'Passed for testuser'