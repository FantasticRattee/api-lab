# Creating a rating returns its id, stars and pizza id.
def test_create_rating(api, auth, pizza_id):
    res = api.post("/api/ratings", json={"pizza_id": pizza_id, "stars": 5}, headers=auth)
    assert res.status_code == 201
    body = res.json()
    try:
        assert body["stars"] == 5
        assert body["pizza_id"] == pizza_id
        assert isinstance(body["id"], int)
    finally:
        api.delete(f"/api/ratings/{body['id']}", headers=auth)


# A saved rating can be read back with exactly the saved fields.
def test_read_rating(api, auth, rating):
    res = api.get(f"/api/ratings/{rating['id']}", headers=auth)
    assert res.status_code == 200
    assert res.json() == rating


# Changing a rating returns the updated number of stars.
def test_update_rating(api, auth, rating):
    res = api.put(f"/api/ratings/{rating['id']}", json={"stars": 4}, headers=auth)
    assert res.status_code == 200
    assert res.json()["stars"] == 4


# Deleting a rating makes a later read return 404.
def test_delete_rating(api, auth, rating):
    path = f"/api/ratings/{rating['id']}"
    assert api.delete(path, headers=auth).status_code == 204
    assert api.get(path, headers=auth).status_code == 404
