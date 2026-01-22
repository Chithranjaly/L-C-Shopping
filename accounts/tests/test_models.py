import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_user_can_be_created():
    user = User.objects.create_user(
        email="test@example.com",
        password="LK3#chithra"
    )
    assert user.email == 'test@example.com'