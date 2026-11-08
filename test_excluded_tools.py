import pytest


# Zero, one or two excluded tools still allow a pizza with an allowed tool.
@pytest.mark.parametrize("excluded", [[], ["Knife"], ["Scissors"], ["Knife", "Scissors"]],
                         ids=["none", "one-knife", "one-scissors", "two"])
def test_excluded_tool_is_not_used(api, auth, excluded):
    res = api.post("/api/pizza", json={"excludedTools": excluded}, headers=auth)
    assert res.status_code == 200
    assert res.json()["pizza"]["tool"] not in excluded


# An impossible request must be refused with 400 and a JSON error, not 500.
@pytest.mark.xfail(reason="Defect 1: excluding all three tools returns 500 with an empty body instead of 400 JSON", strict=True, raises=AssertionError)
def test_all_tools_excluded_is_refused(api, auth):
    res = api.post("/api/pizza", json={"excludedTools": ["Knife", "Pizza cutter", "Scissors"]}, headers=auth)
    assert res.status_code == 400
    assert isinstance(res.json().get("error"), str)
    assert res.json()["error"]
