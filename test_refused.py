import uuid


# A second user with the same username is refused with a clear message.
def test_duplicate_username_is_refused(api):
    user = {"username": "lab-" + uuid.uuid4().hex[:12], "password": "Pizza-2026"}
    assert api.post("/api/users", json=user).status_code == 201
    res = api.post("/api/users", json=user)
    assert res.status_code == 400
    assert res.json() == {"error": "username already taken"}


# A real user cannot log in with a wrong password.
def test_wrong_password_is_refused(api):
    name = "lab-" + uuid.uuid4().hex[:12]
    user = {"username": name, "password": "Pizza-2026"}
    assert api.post("/api/users", json=user).status_code == 201
    res = api.post("/api/users/token/login", json={"username": name, "password": "wrong"})
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}


# An empty username is refused rather than creating an unusable account.
def test_empty_username_is_refused(api):
    res = api.post("/api/users", json={"username": "", "password": "Pizza-2026"})
    assert res.status_code == 400
    assert res.json() == {"error": "username field is empty"}
