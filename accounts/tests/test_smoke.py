import pytest
from django.urls import reverse

@pytest.mark.django_db
def test_homepage_responds(client):
    # change this to a real URL name you have
    # e.g. reverse("home") or reverse("accounts:login")
    url = reverse("home")
    res = client.get(url)
    assert res.status_code in (200, 302)

    # res = client.get("/")
    # assert res.status_code == 404   # <-- intentionally wrong

