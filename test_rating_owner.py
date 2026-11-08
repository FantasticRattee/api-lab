# Another user may not read the owner's rating.
def test_other_user_cannot_read_rating(api, auth, other_auth, rating, record_property):
    path = f"/api/ratings/{rating['id']}"
    res = api.get(path, headers=other_auth)
    record_property("other_user_read_status", res.status_code)
    assert 400 <= res.status_code < 500
    saved = api.get(path, headers=auth)
    assert saved.status_code == 200
    assert saved.json() == rating


# Another user may not update the owner's rating or alter its stored fields.
def test_other_user_cannot_update_rating(api, auth, other_auth, rating, record_property):
    path = f"/api/ratings/{rating['id']}"
    res = api.put(path, json={"stars": 5}, headers=other_auth)
    record_property("other_user_update_status", res.status_code)
    assert 400 <= res.status_code < 500
    saved = api.get(path, headers=auth)
    assert saved.status_code == 200
    assert saved.json() == rating


# Another user may not delete the owner's rating.
def test_other_user_cannot_delete_rating(api, auth, other_auth, rating, record_property):
    path = f"/api/ratings/{rating['id']}"
    res = api.delete(path, headers=other_auth)
    record_property("other_user_delete_status", res.status_code)
    assert 400 <= res.status_code < 500
    saved = api.get(path, headers=auth)
    assert saved.status_code == 200
    assert saved.json() == rating
