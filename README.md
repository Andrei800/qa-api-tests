# 🧪 GoRest API Testing Project

This project demonstrates manual and automated API testing of the public [GoRest API](https://gorest.co.in/).  
It includes negative and positive test cases, bug reports, collection automation, and reporting.

---

## 📦 Tech Stack

- Postman — for API requests and test scripts
- Newman — for CLI execution
- JSON Schema validation (tv4)
- Git + GitHub — version control and documentation
- Markdown — structured test cases and bug reports

---

## 🚀 How to Run Tests

1. Install Node.js: https://nodejs.org/
2. Install Newman and HTML reporter:

```bash
npm install -g newman newman-reporter-html
```

3. Run the collection:

```bash
newman run collections/users-tests.postman_collection.json \
  -e environments/gorest.postman_environment.json \
  -r cli,html \
  --reporter-html-export reports/report.html
```

You can also use the script:

```bash
./scripts/run-tests.cmd
```

---

## 📂 Project Structure

```
qa-api-tests/
├── collections/              # Postman collections
├── environments/             # Postman environments
├── scripts/                  # Run scripts
├── reports/                  # HTML reports (generated)
├── docs/
│   ├── test-cases.md         # Manual test cases
│   └── bug-reports.md        # Reported bugs
├── README.md
└── .gitignore
```

---

## ✅ Test Coverage

- [x] `POST /users` — positive & negative scenarios
- [x] Field validation (email, name, gender, status)
- [x] Required field and type checks
- [x] Duplicate data checks
- [x] JSON Schema validation
- [x] Full request chain: `POST → PATCH → GET → DELETE`

---

## 🐞 Bug Reports

See [bug-reports.md](./docs/bug-reports.md) for known issues.  
Bug examples include: invalid validation, missing field handling, incorrect status codes, etc.

---

## 📊 Sample Report

View: [HTML Report](./reports/report.html)

---

## 👨‍💻 Author

**Andrei Vedernikov**  
Manual QA Engineer / Junior API Tester  
[GitHub: Andrei800](https://github.com/Andrei800)  
[LinkedIn: andrei-vedernikov](https://www.linkedin.com/in/andrei-vedernikov-a96128248/)