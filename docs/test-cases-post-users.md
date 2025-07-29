
# Test Cases: POST /users (Negative Scenarios)

## 📑 Contents

- [TC_API_POST_001 — Invalid email](#tc_api_post_001--invalid-email)
- [TC_API_POST_002 — Empty request body](#tc_api_post_002--empty-request-body)
- [TC_API_POST_003 — Missing email field](#tc_api_post_003--missing-email-field)
- [TC_API_POST_004 — Missing gender field](#tc_api_post_004--missing-gender-field)
- [TC_API_POST_005 — Missing name field](#tc_api_post_005--missing-name-field)
- [TC_API_POST_006 — Invalid gender value](#tc_api_post_006--invalid-gender-value)
- [TC_API_POST_007 — Invalid status value](#tc_api_post_007--invalid-status-value)
- [TC_API_POST_008 — Duplicate email](#tc_api_post_008--duplicate-email)
- [TC_API_POST_009 — Incorrect data types](#tc_api_post_009--incorrect-data-types)
- [TC_API_POST_010 — Fields contain only spaces](#tc_api_post_010--fields-contain-only-spaces)

---

## Test Case: Negative email validation in `/users` API

| Field                | Value                                                                   |
|----------------------|-------------------------------------------------------------------------|
| **ID**               | `TC_API_POST_001_email_invalid`                                         |
| **Title**            | POST `/users` — Invalid email input                                     |
| **Priority**         | Medium                                                                  |
| **Test Type**        | Negative / API / Input validation                                       |
| **Preconditions**    | <ul><li>User is authorized</li><li>Bearer token is present in headers</li></ul> |
| **Steps to Reproduce** | 1. Send a `POST` request to `/users` <br>2. Request body: `{"email": "not-an-email"}` <br>3. Add `Content-Type: application/json` in Headers |
| **Expected Result**  | - HTTP response: **422 Unprocessable Entity** <br>- JSON contains email validation error message |
| **Actual Result**    | Status code: `422`, validation error message received                   |
| **Status**           | ✅ Passed                                                                |
| **Comment**          | Validates handling of invalid email format                              |
| **Date**             | 2025-07-22                                                              |
| **Author**           | Andrei800                                                               |

### Example request (curl)

```bash
curl -X POST https://example.com/api/users \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"email": "not-an-email"}'
```

---

## Test Case: Submitting an empty request body to POST `/users`

| Field                | Value                                                                   |
|----------------------|-------------------------------------------------------------------------|
| **ID**               | `TC_API_POST_002`                                                       |
| **Title**            | POST `/users` — Empty request body                                      |
| **Priority**         | Medium                                                                  |
| **Test Type**        | Negative / API / Input validation                                       |
| **Preconditions**    | <ul><li>User is authorized</li><li>Bearer token is present in headers</li></ul> |
| **Steps to Reproduce** | 1. Send a `POST` request to `/users` <br>2. Request body: `{}` <br>3. Add `Content-Type: application/json` in Headers |
| **Expected Result**  | - HTTP response: **422 Unprocessable Entity** <br>- JSON contains message **"422 expected for empty fields"** |
| **Actual Result**    | Response contains list of field validation errors                       |
| **Status**           | ✅ Passed                                                                |
| **Comment**          | Checks handling of completely empty body                                |
| **Date**             | 2025-07-28                                                              |
| **Author**           | Andrei800                                                               |

### Example request (curl)

```bash
curl -X POST https://gorest.co.in/public/v2/users \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{}'
```


---

## Test Case: Missing all fields

| Field                | Value                                                                   |
|----------------------|-------------------------------------------------------------------------|
| **ID**               | `TC_API_POST_003`                                                       |
| **Title**            | POST `https://gorest.co.in/public/v2/users` — Missing all fields        |
| **Priority**         | Medium                                                                  |
| **Test Type**        | Negative / API / Input validation                                       |
| **Preconditions**    | <ul><li>User is authorized</li><li>Bearer token is present in headers</li></ul> |
| **Steps to Reproduce** | 1. Send a `POST` request to `https://gorest.co.in/public/v2/users` <br>2. Request body:  
```json
{
  "name": "",
  "job": ""
}
```  
3. Set header `Content-Type: application/json` |
| **Expected Result**  | - HTTP 422 Unprocessable Entity <br>- Response body contains validation error message |
| **Actual Result**    | Response contains validation error message                              |
| **Status**           | ✅ Passed                                                                |
| **Comment**          | Auto-generated from Postman Collection                                  |
| **Date**             | 2025-07-28                                                              |
| **Author**           | Andrei800                                                               |

### Example request (curl)

```bash
curl -X POST https://gorest.co.in/public/v2/users \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "name": "",
  "job": ""
}'
```

---

## Test Case: Missing email

| Field                | Value                                                                   |
|----------------------|-------------------------------------------------------------------------|
| **ID**               | `TC_API_POST_004`                                                       |
| **Title**            | POST `https://gorest.co.in/public/v2/users` — Missing email             |
| **Priority**         | Medium                                                                  |
| **Test Type**        | Negative / API / Input validation                                       |
| **Preconditions**    | <ul><li>User is authorized</li><li>Bearer token is present in headers</li></ul> |
| **Steps to Reproduce** | 1. Send a `POST` request to `https://gorest.co.in/public/v2/users` <br>2. Request body:  
```json
{
  "name": "Test User",
  "gender": "male",
  "status": "active"
}
```  
3. Set header `Content-Type: application/json` |
| **Expected Result**  | - HTTP 422 Unprocessable Entity <br>- Response body contains validation error message |
| **Actual Result**    | Response contains validation error message                              |
| **Status**           | ✅ Passed                                                                |
| **Comment**          | Auto-generated from Postman Collection                                  |
| **Date**             | 2025-07-28                                                              |
| **Author**           | Andrei800                                                               |

### Example request (curl)

```bash
curl -X POST https://gorest.co.in/public/v2/users \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "name": "Test User",
  "gender": "male",
  "status": "active"
}'
```


---

## Test Case: Missing gender

| Field                | Value                                                                   |
|----------------------|-------------------------------------------------------------------------|
| **ID**               | `TC_API_POST_005`                                                       |
| **Title**            | POST `https://gorest.co.in/public/v2/users` — Missing gender            |
| **Priority**         | Medium                                                                  |
| **Test Type**        | Negative / API / Input validation                                       |
| **Preconditions**    | <ul><li>User is authorized</li><li>Bearer token is present in headers</li></ul> |
| **Steps to Reproduce** | 1. Send a `POST` request to `https://gorest.co.in/public/v2/users` <br>2. Request body:  
```json
{
  "name": "No Gender User",
  "email": "nogender@example.com",
  "status": "active"
}
```  
3. Set header `Content-Type: application/json` |
| **Expected Result**  | - HTTP 422 Unprocessable Entity <br>- Response body contains validation error message |
| **Actual Result**    | Response contains validation error message                              |
| **Status**           | ✅ Passed                                                                |
| **Comment**          | Auto-generated from Postman Collection                                  |
| **Date**             | 2025-07-28                                                              |
| **Author**           | Andrei800                                                               |

### Example request (curl)

```bash
curl -X POST https://gorest.co.in/public/v2/users \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "name": "No Gender User",
  "email": "nogender@example.com",
  "status": "active"
}'
```

---

## Test Case: Missing name

| Field                | Value                                                                   |
|----------------------|-------------------------------------------------------------------------|
| **ID**               | `TC_API_POST_006`                                                       |
| **Title**            | POST `https://gorest.co.in/public/v2/users` — Missing name              |
| **Priority**         | Medium                                                                  |
| **Test Type**        | Negative / API / Input validation                                       |
| **Preconditions**    | <ul><li>User is authorized</li><li>Bearer token is present in headers</li></ul> |
| **Steps to Reproduce** | 1. Send a `POST` request to `https://gorest.co.in/public/v2/users` <br>2. Request body:  
```json
{
  "email": "missing_name@example.com",
  "gender": "male",
  "status": "active"
}
```  
3. Set header `Content-Type: application/json` |
| **Expected Result**  | - HTTP 422 Unprocessable Entity <br>- Response body contains validation error message |
| **Actual Result**    | Response contains validation error message                              |
| **Status**           | ✅ Passed                                                                |
| **Comment**          | Auto-generated from Postman Collection                                  |
| **Date**             | 2025-07-28                                                              |
| **Author**           | Andrei800                                                               |

### Example request (curl)

```bash
curl -X POST https://gorest.co.in/public/v2/users \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "email": "missing_name@example.com",
  "gender": "male",
  "status": "active"
}'
```


---

## Test Case: Invalid email

| Field                | Value                                                                   |
|----------------------|-------------------------------------------------------------------------|
| **ID**               | `TC_API_POST_007`                                                       |
| **Title**            | POST `https://gorest.co.in/public/v2/users` — Invalid email             |
| **Priority**         | Medium                                                                  |
| **Test Type**        | Negative / API / Input validation                                       |
| **Preconditions**    | <ul><li>User is authorized</li><li>Bearer token is present in headers</li></ul> |
| **Steps to Reproduce** | 1. Send a `POST` request to `https://gorest.co.in/public/v2/users` <br>2. Request body:  
```json
{
  "email": "not-an-email",
  "name": "Test User",
  "gender": "robot",
  "status": ""
}
```  
3. Set header `Content-Type: application/json` |
| **Expected Result**  | - HTTP 422 Unprocessable Entity <br>- Response body contains validation error message |
| **Actual Result**    | Response contains validation error message                              |
| **Status**           | ✅ Passed                                                                |
| **Comment**          | Auto-generated from Postman Collection                                  |
| **Date**             | 2025-07-28                                                              |
| **Author**           | Andrei800                                                               |

### Example request (curl)

```bash
curl -X POST https://gorest.co.in/public/v2/users \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "email": "not-an-email",
  "name": "Test User",
  "gender": "robot",
  "status": ""
}'
```

---

## Test Case: Invalid gender

| Field                | Value                                                                   |
|----------------------|-------------------------------------------------------------------------|
| **ID**               | `TC_API_POST_008`                                                       |
| **Title**            | POST `https://gorest.co.in/public/v2/users` — Invalid gender            |
| **Priority**         | Medium                                                                  |
| **Test Type**        | Negative / API / Input validation                                       |
| **Preconditions**    | <ul><li>User is authorized</li><li>Bearer token is present in headers</li></ul> |
| **Steps to Reproduce** | 1. Send a `POST` request to `https://gorest.co.in/public/v2/users` <br>2. Request body:  
```json
{
  "name": "Test User",
  "email": "test_invalid_gender@example.com",
  "gender": "robot",
  "status": "active"
}
```  
3. Set header `Content-Type: application/json` |
| **Expected Result**  | - HTTP 422 Unprocessable Entity <br>- Response body contains validation error message |
| **Actual Result**    | Response contains validation error message                              |
| **Status**           | ✅ Passed                                                                |
| **Comment**          | Auto-generated from Postman Collection                                  |
| **Date**             | 2025-07-28                                                              |
| **Author**           | Andrei800                                                               |

### Example request (curl)

```bash
curl -X POST https://gorest.co.in/public/v2/users \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "name": "Test User",
  "email": "test_invalid_gender@example.com",
  "gender": "robot",
  "status": "active"
}'
```


---

## Test Case: POST with incorrect data types

| Field                | Value                                                                   |
|----------------------|-------------------------------------------------------------------------|
| **ID**               | `TC_API_POST_009`                                                       |
| **Title**            | POST `https://gorest.co.in/public/v2/users` — POST with incorrect data types |
| **Priority**         | Medium                                                                  |
| **Test Type**        | Negative / API / Input validation                                       |
| **Preconditions**    | <ul><li>User is authorized</li><li>Bearer token is present in headers</li></ul> |
| **Steps to Reproduce** | 1. Send a `POST` request to `https://gorest.co.in/public/v2/users` <br>2. Request body:  
```json
{
  "email": true,
  "gender": 0,
  "status": false
}
```  
3. Set header `Content-Type: application/json` |
| **Expected Result**  | - HTTP 422 Unprocessable Entity <br>- Response body contains validation error messages |
| **Actual Result**    | Response contains validation error message                              |
| **Status**           | ✅ Passed                                                                |
| **Comment**          | Auto-generated from Postman Collection                                  |
| **Date**             | 2025-07-28                                                              |
| **Author**           | Andrei800                                                               |

### Example request (curl)

```bash
curl -X POST https://gorest.co.in/public/v2/users \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "email": true,
  "gender": 0,
  "status": false
}'
```

---

## Test Case: Fields contain only spaces (" ")

| Field                | Value                                                                   |
|----------------------|-------------------------------------------------------------------------|
| **ID**               | `TC_API_POST_010`                                                       |
| **Title**            | POST `https://gorest.co.in/public/v2/users` — Fields contain only spaces |
| **Priority**         | Medium                                                                  |
| **Test Type**        | Negative / API / Input validation                                       |
| **Preconditions**    | <ul><li>User is authorized</li><li>Bearer token is present in headers</li></ul> |
| **Steps to Reproduce** | 1. Send a `POST` request to `https://gorest.co.in/public/v2/users` <br>2. Request body:  
```json
{
  "name": "   ",
  "email": "   ",
  "gender": "   ",
  "status": "   "
}
```  
3. Set header `Content-Type: application/json` |
| **Expected Result**  | - HTTP 422 Unprocessable Entity <br>- Response body contains validation error messages |
| **Actual Result**    | Response contains validation error message                              |
| **Status**           | ✅ Passed                                                                |
| **Comment**          | Auto-generated from Postman Collection                                  |
| **Date**             | 2025-07-28                                                              |
| **Author**           | Andrei800                                                               |

### Example request (curl)

```bash
curl -X POST https://gorest.co.in/public/v2/users \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{
  "name": "   ",
  "email": "   ",
  "gender": "   ",
  "status": "   "
}'
```
