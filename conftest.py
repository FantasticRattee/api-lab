import uuid
import pytest
import requests

SITE = "https://quickpizza.grafana.com"

class QuickPizza(requests.Session):
    """Add the site address before each API path."""
    def request(self, method, url, *args, **kwargs):
        kwargs.setdefault("timeout", 30)
        return super().request(method, SITE + url, *args, **kwargs)

@pytest.fixture(scope="session")
def api():
    with QuickPizza() as session:
        yield session


def log_in_new_user(api):
    """Create a made-up user, log in, and return only its auth header."""
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    res = api.post("/api/users", json=user)
    assert res.status_code == 201
    res = api.post("/api/users/token/login", json=user)
    assert res.status_code == 200
    return {"Authorization": "token " + res.json()["token"]}


@pytest.fixture
def auth(api):
    return log_in_new_user(api)


@pytest.fixture
def pizza_id(api, auth):
    res = api.post("/api/pizza", json={}, headers=auth)
    assert res.status_code == 200
    return res.json()["pizza"]["id"]


@pytest.fixture
def rating(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3}, headers=auth)
    assert res.status_code == 201
    made = res.json()
    try:
        yield made
    finally:
        path = f"/api/ratings/{made['id']}"
        # The delete test already removed its rating; do not delete it twice.
        remaining = api.get(path, headers=auth)
        if remaining.status_code == 200:
            assert api.delete(path, headers=auth).status_code == 204
        else:
            assert remaining.status_code == 404


@pytest.fixture
def other_auth(api):
    return log_in_new_user(api)
