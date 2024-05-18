import pytest
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


@pytest.fixture
def user(db):
    user = User.objects.create_user(username='testuser', password='test_pass')
    Token.objects.create(user=user)
    return user
