import pytest


# Boundary updates save valid stars and leave the old rating intact on refusal.
@pytest.mark.parametrize("stars, expected_status", [(0, 400), (1, 200), (5, 200), (6, 400)])
def test_update_stars_boundaries(api, auth, rating, stars, expected_status):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": stars}, headers=auth)
    assert res.status_code == expected_status
    if expected_status == 200:
        assert res.json()["stars"] == stars
    else:
        assert res.json() == {"error": "number of stars must be between 1 and 5 (inclusive)"}
    saved = api.get(path, headers=auth)
    assert saved.status_code == 200
    assert saved.json()["stars"] == (stars if expected_status == 200 else rating["stars"])
