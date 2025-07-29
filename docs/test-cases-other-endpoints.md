# Test Cases — Other Endpoints (GET, PATCH, DELETE)

## 📑 Contents

- [TC_API_PATCH_001 — Update user with invalid data](#tc-api-patch-001)
- [TC_API_GET_001 — Attempt GET with invalid PATCH payload](#tc-api-get-001)
- [TC_API_DELETE_001 — Basic user deletion by ID](#tc-api-delete-001)
- [TC_API_PATCH_002 — PATCH — Valid user update](#tc-api-patch-002)
- [TC_API_GET_002 — GET — Fetch user by ID after update](#tc-api-get-002)
- [TC_API_GET_003 — GET — Validate response schema (reqres.in)](#tc-api-get-003)
- [TC_API_PATCH_003 — PATCH — Update user with valid data (duplicate case check)](#tc-api-patch-003)
- [TC_API_DELETE_002 — DELETE — Attempt to delete already deleted user](#tc-api-delete-002)
- [TC_API_GET_004 — GET — Validate users endpoint schema (alt variant)](#tc-api-get-004)
- [TC_API_GET_005 — GET — Third schema validation (reqres.in)](#tc-api-get-005)
- [TC_API_PATCH_004 — PATCH — Update non-existent user](#tc-api-patch-004)
- [TC_API_DELETE_003 — DELETE — Without authorization token](#tc-api-delete-003)
- [TC_API_POST_011 — POST — Register with missing fields (reqres)](#tc-api-post-011)

---

## Test Case: Update user with invalid data

| Field              | Value                                                                 |
|-------------------|-----------------------------------------------------------------------|
| **ID**            | TC_API_PATCH_001                                                      |
| **Title**         | PATCH `/users/{{createdUserId}}` — Update user with invalid data      |
| **Priority**      | Medium                                                                |
| **Test Type**     | Negative / API / Input validation                                     |
| **Preconditions** | <ul><li>User is authorized</li><li>Bearer token is present in headers</li></ul> |
| **Steps to Reproduce** | 1. Send a `PATCH` request to the endpoint <br>2. Request body:  
```json
{
  "name": "Updated Test User",
  "status": "inactive",
  "gender": "female"
}
```  
3. Add header: `Content-Type: application/json` |
| **Expected Result** | - HTTP 422 Unprocessable Entity <br>- Response body contains validation error message |
| **Actual Result** | Validation error message is received                                |
| **Status**        | ✅ Passed                                                              |
| **Comment**       | Auto-generated from Postman Collection                               |
| **Date**          | 2025-07-28                                                            |
| **Author**        | Andrei800                                                             |

### Example request (curl)

```bash
curl -X PATCH https://gorest.co.in/public/v2/users/{{createdUserId}} \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "name": "Updated Test User",
  "status": "inactive",
  "gender": "female"
}'
```

---

## Test Case: Attempt GET with invalid PATCH payload

| Field              | Value                                                                 |
|-------------------|-----------------------------------------------------------------------|
| **ID**            | TC_API_GET_001                                                        |
| **Title**         | GET `/users/{{createdUserId}}` — Attempt GET with invalid PATCH payload |
| **Priority**      | Medium                                                                |
| **Test Type**     | Negative / API / Input validation                                     |
| **Preconditions** | <ul><li>User is authorized</li><li>Bearer token is present in headers</li></ul> |
| **Steps to Reproduce** | 1. Send a `GET` request to the endpoint <br>2. Request body:  
```json
{
  "name": "PatchUser",
  "gender": "male",
  "email": "autouser_{{randomNumber}}@mail.com",
  "status": "active"
}
```  
3. Add header: `Content-Type: application/json` |
| **Expected Result** | - HTTP 422 Unprocessable Entity <br>- Response body contains validation error message |
| **Actual Result** | Validation error message is received                                |
| **Status**        | ✅ Passed                                                              |
| **Comment**       | Auto-generated from Postman Collection                               |
| **Date**          | 2025-07-28                                                            |
| **Author**        | Andrei800                                                             |

### Example request (curl)

```bash
curl -X GET https://gorest.co.in/public/v2/users/{{createdUserId}} \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "name": "PatchUser",
  "gender": "male",
  "email": "autouser_{{randomNumber}}@mail.com",
  "status": "active"
}'
```

---

## Test Case: Basic user deletion by ID

| Field              | Value                                                                 |
|-------------------|-----------------------------------------------------------------------|
| **ID**            | TC_API_DELETE_001                                                     |
| **Title**         | DELETE `/users/{{createdUserId}}` — Basic user deletion by ID         |
| **Priority**      | Medium                                                                |
| **Test Type**     | API / DELETE                                                          |
| **Preconditions** | User is authorized and has access to the API                          |
| **Steps to Reproduce** | 1. Send a `DELETE` request to the endpoint <br>2. Request body:  
```json
{}
```  
3. Add header: `Content-Type: application/json` |
| **Expected Result** | HTTP 204 No Content or valid 404/validation response depending on state |
| **Actual Result** | Response matches expected behavior                                     |
| **Status**        | ✅ Passed                                                              |
| **Comment**       | Auto-generated from Postman Collection                               |
| **Date**          | 2025-07-28                                                            |
| **Author**        | Andrei800                                                             |

### Example request (curl)

```bash
curl -X DELETE https://gorest.co.in/public/v2/users/{{createdUserId}} \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{}'
```
---

## Test Case: PATCH — Valid user update

| Field              | Value                                                                 |
|-------------------|------------------------------------------------------------------------|
| **ID**            | TC_API_PATCH_002                                                       |
| **Title**         | PATCH `/users/{{createdUserId}}` — Valid user update                   |
| **Priority**      | Medium                                                                 |
| **Test Type**     | API / PATCH                                                            |
| **Preconditions** | User is authorized and has access to the API                           |
| **Steps to Reproduce** | 1. Send a `PATCH` request to the endpoint <br>2. Request body:  
```json
{
  "name": "Updated User Name",
  "gender": "male",
  "status": "inactive"
}
```  
3. Add header: `Content-Type: application/json` |
| **Expected Result** | Successful HTTP response (200 or 204) or schema/logic validation passes |
| **Actual Result** | Response matches expected behavior                                     |
| **Status**        | ✅ Passed                                                               |
| **Comment**       | Auto-generated from Postman Collection                                |
| **Date**          | 2025-07-28                                                             |
| **Author**        | Andrei800                                                              |

### Example request (curl)

```bash
curl -X PATCH https://gorest.co.in/public/v2/users/{{createdUserId}} \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "name": "Updated User Name",
  "gender": "male",
  "status": "inactive"
}'
```

---

## Test Case: GET — Fetch user by ID after update

| Field              | Value                                                                 |
|-------------------|------------------------------------------------------------------------|
| **ID**            | TC_API_GET_002                                                         |
| **Title**         | GET `/users/{{createdUserId}}` — Fetch user by ID after update         |
| **Priority**      | Medium                                                                 |
| **Test Type**     | API / GET                                                              |
| **Preconditions** | User is authorized and has access to the API                           |
| **Steps to Reproduce** | 1. Send a `GET` request to the endpoint <br>2. Optional request body:  
```json
{
  "name": "PatchUser",
  "gender": "male",
  "email": "autouser_{{randomNumber}}@mail.com",
  "status": "active"
}
```  
3. Add header: `Content-Type: application/json` |
| **Expected Result** | Successful HTTP response with user data or valid schema               |
| **Actual Result** | Response matches expected behavior                                     |
| **Status**        | ✅ Passed                                                               |
| **Comment**       | Auto-generated from Postman Collection                                |
| **Date**          | 2025-07-28                                                             |
| **Author**        | Andrei800                                                              |

### Example request (curl)

```bash
curl -X GET https://gorest.co.in/public/v2/users/{{createdUserId}} \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "name": "PatchUser",
  "gender": "male",
  "email": "autouser_{{randomNumber}}@mail.com",
  "status": "active"
}'
```

---

## Test Case: GET — Validate response schema (reqres.in)

| Field              | Value                                                                 |
|-------------------|------------------------------------------------------------------------|
| **ID**            | TC_API_GET_003                                                         |
| **Title**         | GET `https://reqres.in/api/users?page=2` — Validate JSON Schema        |
| **Priority**      | Medium                                                                 |
| **Test Type**     | API / GET / JSON Schema                                                |
| **Preconditions** | Access to API (authorization not required)                             |
| **Steps to Reproduce** | 1. Send a `GET` request to the endpoint <br>2. Validate that the response body matches the expected JSON Schema <br>3. Add header: `Content-Type: application/json` |
| **Expected Result** | Schema validation passes, `data[]` is valid                          |
| **Actual Result** | Schema is confirmed                                                    |
| **Status**        | ✅ Passed                                                               |
| **Comment**       | Auto-generated from JSON Schema test collection                        |
| **Date**          | 2025-07-28                                                             |
| **Author**        | Andrei800                                                              |

### Example request (curl)

```bash
curl -X GET "https://reqres.in/api/users?page=2" \
  -H "Content-Type: application/json"
```
---

## Test Case: PATCH — Update user with valid data (duplicate case check)

| Field              | Value                                                                 |
|-------------------|------------------------------------------------------------------------|
| **ID**            | TC_API_PATCH_003                                                       |
| **Title**         | PATCH `/users/{{createdUserId}}` — Update user with valid data         |
| **Priority**      | Medium                                                                 |
| **Test Type**     | API / PATCH                                                            |
| **Preconditions** | User is authorized and has access to the API                           |
| **Steps to Reproduce** | 1. Send a `PATCH` request to the endpoint <br>2. Request body:  
```json
{
  "name": "Updated User Name",
  "gender": "male",
  "status": "inactive"
}
```  
3. Add header: `Content-Type: application/json` |
| **Expected Result** | Successful HTTP response and correct user update                     |
| **Actual Result** | Response matches expected behavior                                     |
| **Status**        | ✅ Passed                                                               |
| **Comment**       | Confirming idempotency of PATCH operation                              |
| **Date**          | 2025-07-28                                                             |
| **Author**        | Andrei800                                                              |

### Example request (curl)

```bash
curl -X PATCH https://gorest.co.in/public/v2/users/{{createdUserId}} \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "name": "Updated User Name",
  "gender": "male",
  "status": "inactive"
}'
```

---

## Test Case: DELETE — Attempt to delete already deleted user

| Field              | Value                                                                 |
|-------------------|------------------------------------------------------------------------|
| **ID**            | TC_API_DELETE_002                                                      |
| **Title**         | DELETE `/users/{{createdUserId}}` — Attempt to delete already deleted user |
| **Priority**      | Medium                                                                 |
| **Test Type**     | API / DELETE                                                           |
| **Preconditions** | User is authorized and has access to the API                           |
| **Steps to Reproduce** | 1. Send a `DELETE` request to the endpoint for the same ID twice <br>2. Second request body:  
```json
{}
```  
3. Add header: `Content-Type: application/json` |
| **Expected Result** | HTTP 404 Not Found or a valid error response                         |
| **Actual Result** | Response matches expected behavior                                     |
| **Status**        | ✅ Passed                                                               |
| **Comment**       | Check handling of repeated deletions                                   |
| **Date**          | 2025-07-28                                                             |
| **Author**        | Andrei800                                                              |

### Example request (curl)

```bash
curl -X DELETE https://gorest.co.in/public/v2/users/{{createdUserId}} \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{}'
```

---

## Test Case: GET — Validate users endpoint schema (alt variant)

| Field              | Value                                                                 |
|-------------------|------------------------------------------------------------------------|
| **ID**            | TC_API_GET_004                                                         |
| **Title**         | GET `https://reqres.in/api/users?page=2` — Validate response schema (alt) |
| **Priority**      | Medium                                                                 |
| **Test Type**     | API / GET / JSON Schema                                                |
| **Preconditions** | Access to API                                                          |
| **Steps to Reproduce** | 1. Send a `GET` request to the endpoint <br>2. Check schema validity <br>3. Header: `Content-Type: application/json` |
| **Expected Result** | JSON Schema validation successful                                     |
| **Actual Result** | Validation passed                                                      |
| **Status**        | ✅ Passed                                                               |
| **Comment**       | Duplicate schema validation variant                                    |
| **Date**          | 2025-07-28                                                             |
| **Author**        | Andrei800                                                              |

### Example request (curl)

```bash
curl -X GET "https://reqres.in/api/users?page=2" \
  -H "Content-Type: application/json"
```
---

## Test Case: GET — Third schema validation (reqres.in)

| Field              | Value                                                                 |
|-------------------|------------------------------------------------------------------------|
| **ID**            | TC_API_GET_005                                                         |
| **Title**         | GET `https://reqres.in/api/users?page=2` — Third schema validation     |
| **Priority**      | Medium                                                                 |
| **Test Type**     | API / GET / JSON Schema                                                |
| **Preconditions** | Access to API                                                          |
| **Steps to Reproduce** | 1. Send a `GET` request to the endpoint <br>2. Validate response matches JSON Schema <br>3. Header: `Content-Type: application/json` |
| **Expected Result** | JSON Schema matches expected structure                               |
| **Actual Result** | Schema is successfully validated                                       |
| **Status**        | ✅ Passed                                                               |
| **Comment**       | Third version of response schema validation test                       |
| **Date**          | 2025-07-28                                                             |
| **Author**        | Andrei800                                                              |

### Example request (curl)

```bash
curl -X GET "https://reqres.in/api/users?page=2" \
  -H "Content-Type: application/json"
```
---

## Test Case: PATCH — Update non-existent user

| Field              | Value                                                                 |
|-------------------|------------------------------------------------------------------------|
| **ID**            | TC_API_PATCH_004                                                       |
| **Title**         | PATCH `/users/12` — Update non-existent user                           |
| **Priority**      | Medium                                                                 |
| **Test Type**     | Negative / API / Not Found                                             |
| **Preconditions** | User is authorized and has access to the API                           |
| **Steps to Reproduce** | 1. Send a `PATCH` request to `/users/12` with valid body <br>2. Add header: `Content-Type: application/json` |
| **Expected Result** | HTTP 404 Not Found                                                    |
| **Actual Result** | 404 Not Found returned                                                 |
| **Status**        | ✅ Passed                                                               |
| **Comment**       | Non-existent user scenario                                             |
| **Date**          | 2025-07-29                                                             |
| **Author**        | Andrei800                                                              |

### Example request (curl)

```bash
curl -X PATCH https://gorest.co.in/public/v2/users/12 \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "name": "Updated QA"
}'
```

---

## Test Case: DELETE — Without authorization token

| Field              | Value                                                                 |
|-------------------|------------------------------------------------------------------------|
| **ID**            | TC_API_DELETE_003                                                      |
| **Title**         | DELETE `/users/:id` — Without token                                    |
| **Priority**      | Medium                                                                 |
| **Test Type**     | Negative / API / Authorization                                         |
| **Preconditions** | No authorization headers included                                      |
| **Steps to Reproduce** | 1. Send a `DELETE` request without Bearer token <br>2. Add header: `Content-Type: application/json` |
| **Expected Result** | HTTP 401 Unauthorized                                                 |
| **Actual Result** | 401 Unauthorized                                                       |
| **Status**        | ✅ Passed                                                               |
| **Comment**       | Token must be required                                                 |
| **Date**          | 2025-07-29                                                             |
| **Author**        | Andrei800                                                              |

### Example request (curl)

```bash
curl -X DELETE https://gorest.co.in/public/v2/users/{{createdUserId}} \
  -H "Content-Type: application/json"
```

---

## Test Case: POST — Register with missing fields (reqres)

| Field              | Value                                                                 |
|-------------------|------------------------------------------------------------------------|
| **ID**            | TC_API_POST_011                                                        |
| **Title**         | POST `/register` — Missing required fields                             |
| **Priority**      | Medium                                                                 |
| **Test Type**     | Negative / API / Input validation                                      |
| **Preconditions** | Public API, no token needed                                            |
| **Steps to Reproduce** | 1. Send a `POST` request to `/register` with only email<br>2. Add header: `Content-Type: application/json` |
| **Expected Result** | HTTP 400 or 422 <br> Response includes validation message            |
| **Actual Result** | Error response with `error` field                                      |
| **Status**        | ✅ Passed                                                               |
| **Comment**       | Covers client error from incomplete request                            |
| **Date**          | 2025-07-29                                                             |
| **Author**        | Andrei800                                                              |

### Example request (curl)

```bash
curl -X POST https://reqres.in/api/register \
  -H "Content-Type: application/json" \
  -d '{
  "email": "sydney@fife"
}'
```
