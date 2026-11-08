# API lab results

Observed on 8 November 2026 against the shared QuickPizza demo. Python 3.14.6, pytest 9.2.0, requests 2.34.2 and pytest-html 4.2.0 were used. The site may change, so these are observations from this run.

## Part 0

- Step 0.1: 18 pizza names; status 200.
- Step 0.3: without a token, status 401 with `{"error":"authentication failed"}`.
- Step 0.4: the vegetarian pizza was named **The Quick Prosciutto**. The returned name is random.
- Step 0.12 (optional): three separate no-session runs gave **passed, failed, failed**. Both failures were at login: expected 200, actual 401. This temporary experiment is outside the submitted suite.
- Step 0.14: `test_delete_rating` passed when run alone.
- Step 0.16: the blocks are **0, 1, 2 and 3 excluded tools**. Cases use `[]`, `["Knife"]`, `["Scissors"]`, `["Knife","Scissors"]` and all three tools. The two single-tool cases belong to the same block. Excluding all three revealed the defect.

### A2 error messages found with curl

Each request kept valid base values for the other fields and used a new test user's session/token when authentication was required.

| Non-base block | Status | Error |
| --- | ---: | --- |
| Decimal stars | 400 | `json: cannot unmarshal number 3.5 into Go struct field Rating.stars of type int` |
| Text stars | 400 | `json: cannot unmarshal string into Go struct field Rating.stars of type int` |
| Missing stars | 400 | `number of stars must be between 1 and 5 (inclusive)` |
| Missing pizza | 400 | `pizza ID 999999999 not found` |
| No token | 401 | `authentication failed` |
| Wrong-length token | 401 | `authentication failed` |

## Defect report

- Title: Excluding every tool returns an internal error.
- Request: authenticated `POST /api/pizza`, with the test user's own token and body `{"excludedTools":["Knife","Pizza cutter","Scissors"]}` (`excluded-all.json`).
- Expected result: status 400 with a JSON error message, because no pizza can satisfy the restrictions.
- Actual result: status 500 with an empty body. Confirmed with curl and an unmarked failing pytest test before adding the xfail mark.
- Severity: Medium. An unsatisfiable customer request gives an internal error and no useful explanation, although other requests still work.
- Tracking: `test_all_tools_excluded_is_refused` retains the correct expectation and uses `xfail(strict=True)`; it is not deleted or changed to expect 500.

## Part A

- A4 observed statuses for another user: **read 404, update 400, delete 400**. The owner could still read the unchanged rating after each attempt.
- Final full-suite result: **32 passed, 1 xfailed in 50.54 seconds**, exit code 0, with no warnings or unexpected errors. The actual self-contained run is recorded in `report.html`.

## Part B

1. Real API tests can expose wrong status/body handling in the deployed server and failures caused by cookies or load-balancer routing. Stubbed unit tests are still useful because they are fast, deterministic and isolate a function's logic.

2. A new user isolates each test's ratings and avoids changing shared data. For Project 2, create the test's own accounts and records, use their credentials, and clean up only those records rather than another group's data.

3. One session keeps the AWSALB cookie, so related requests reach the backend that knows the new user. Without a session, my three recorded runs were pass, login 401, login 401. This shows why an otherwise unchanged test can be flaky.

4. Excluding all three tools found the defect. A 500 with an empty body gives the calling app no useful input-error message and may also break JSON parsing. Keeping a strict xfail documents the defect and alerts us when the expected behavior starts passing.

5. Base choice: `1 + (3-1) + (4-1) + (2-1) + (3-1) = 9`. All combinations: `3 × 4 × 2 × 3 = 72`.

6. Read returned 404; update and delete returned 400. I would normally expect 403, or 404 to hide another user's resource. The worksheet only requires a 4xx refusal and unchanged owner data, which all three attempts satisfied. Different 4xx codes alone do not establish an authorization defect without a more specific API contract.

7. The made-up 16-character token returned **200** and a JSON `ratings` list with **50 entries**. It was not obtained by login, so accepting it instead of rejecting it with 401 is an authentication/access-control weakness. On a real system, it could expose ratings to someone without a valid account. I only read the required endpoint; I did not try creating, changing or deleting data, and did not include other users' rating contents in this report.

8. API tests can directly and precisely check status codes, response fields and invalid inputs. A UI test is needed to check whether controls and messages are displayed correctly and whether the user can interact with them.
