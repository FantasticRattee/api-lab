# API lab

ITCS386 Week 11: API testing with pytest and requests against the shared QuickPizza demo.

## Install and run

Python 3.10 or newer and curl are required. On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -v --tb=short
```

On Windows, create the environment with `python -m venv .venv` and activate it with `.venv\Scripts\activate`. Use `curl.exe` in PowerShell.

To save a self-contained report:

```bash
python -m pytest -v --tb=short --html=report.html --self-contained-html
```

Open `report.html` in a browser. `--tb=short` keeps failure details without printing fixture arguments such as login tokens. One known API defect is marked `xfail(strict=True)`. An unexpected pass makes the run fail so the mark can be reviewed after the server is fixed.

The saved run on 8 November 2026 finished with **32 passed, 1 xfailed in 50.54 seconds**. No unexpected failures or teardown errors remained.

The shared `api` fixture keeps load-balancer cookies. Each test that needs a user logs in with a new UUID-based account. Ratings created by the tests are cleaned up using their owner's token. The explicit-delete test is also runnable alone:

```bash
python -m pytest -v test_ratings.py::test_delete_rating
```

## Input domain model: create a rating

The base is integer `3` stars, a newly generated pizza that exists, and the test user's own token. Each non-base case changes one characteristic only.

| Characteristic | Block | Example | Test in `test_create_rating.py` |
| --- | --- | --- | --- |
| C1: value of stars | Below 1 | `0` | `test_stars_out_of_range[0]` |
| C1 | 1 to 5 (base) | `3` | `test_base_choice_is_saved` |
| C1 | Above 5 | `6` | `test_stars_out_of_range[6]` |
| C2: type of stars | Whole number (base) | `3` | `test_base_choice_is_saved` |
| C2 | Decimal | `3.5` | `test_invalid_star_type[decimal]` |
| C2 | Text | `"3"` | `test_invalid_star_type[text]` |
| C2 | Missing | No `stars` field | `test_invalid_star_type[missing]` |
| C3: pizza | Exists (base) | `pizza_id` fixture | `test_base_choice_is_saved` |
| C3 | Does not exist | `999999999` | `test_nonexistent_pizza_is_refused` |
| C4: token | Own token (base) | `auth` fixture | `test_base_choice_is_saved` |
| C4 | None | No Authorization header | `test_invalid_token_is_refused[none]` |
| C4 | Wrong length | `token short` | `test_invalid_token_is_refused[wrong-length]` |

Base choice needs `1 + (3-1) + (4-1) + (2-1) + (3-1) = 9` cases. All combinations would need `3 × 4 × 2 × 3 = 72`. Update boundary tests separately cover `0`, `1`, `5`, and `6` stars. Ownership tests check that another user cannot read, update or delete a rating and that the owner's data stays unchanged.

## Files and safety

- `conftest.py`: session, login and test-data fixtures.
- `test_*.py`: automated tests, grouped by operation.
- `RESULTS.md`: measured observations, defect report and eight reflection answers.
- `report.html`: the saved full-suite result.
- `auth.txt`, `veg.json`: the worksheet's public-token curl examples.
- `excluded-all.json`: the JSON body used to confirm Defect 1 with curl.
- `madeup.txt`: the worksheet's made-up token, used only for its read-only GET experiment.

Do not use the public or made-up token to create/change ratings. Never touch another user's data. Use made-up usernames/passwords, never real credentials. Run the suite only when needed, not in a loop. The optional no-session experiment was run separately three times and is not included in the final suite.

Guided steps were developed with AI tutoring; the remaining implementation and documentation were completed with AI assistance. Results below come from actual runs, not the worksheet's example output.

## Submission

Push this project to a **public repository named `api-lab`**, then submit its repository link in MyCourses. The report, scripts, README and results are included in the repository; no separate PDF answer is required by the worksheet. Check the assignment deadline in MyCourses.
