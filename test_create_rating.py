import pytest

STARS_ERROR = "number of stars must be between 1 and 5 (inclusive)"


# Base choice: integer 3 stars, an existing pizza and the user's own token.
def test_base_choice_is_saved(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3}, headers=auth)
    assert res.status_code == 201
    body = res.json()
    try:
        assert body["stars"] == 3
        assert body["pizza_id"] == pizza_id
    finally:
        api.delete(f"/api/ratings/{body['id']}", headers=auth)


# C1: stars below or above the accepted range are refused.
@pytest.mark.parametrize("stars", [0, 6])
def test_stars_out_of_range(api, auth, pizza_id, stars):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": stars}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": STARS_ERROR}


# C2: decimal, text and missing stars each exercise one non-base type block.
@pytest.mark.parametrize("field, error", [
    ({"stars": 3.5}, "json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int"),
    ({"stars": "3"}, "json: cannot unmarshal string into Go struct field Rating.stars of type int"),
    ({}, STARS_ERROR),
], ids=["decimal", "text", "missing"])
def test_invalid_star_type(api, auth, pizza_id, field, error):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, **field}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": error}


# C3: a nonexistent pizza is refused while stars and token stay at base.
def test_nonexistent_pizza_is_refused(api, auth):
    res = api.post("/api/ratings", json={"pizza_id": 999999999, "stars": 3}, headers=auth)
    assert res.status_code == 400
    assert res.json() == {"error": "pizza ID 999999999 not found"}


# C4: missing and wrong-length tokens are refused; pizza and stars stay at base.
@pytest.mark.parametrize("headers", [{}, {"Authorization": "token short"}], ids=["none", "wrong-length"])
def test_invalid_token_is_refused(api, pizza_id, headers):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 3}, headers=headers)
    assert res.status_code == 401
    assert res.json() == {"error": "authentication failed"}
