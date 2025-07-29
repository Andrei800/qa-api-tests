@echo off
REM Auto-run Postman collection and open HTML report

REM Ensure reports folder exists
if not exist reports (
    mkdir reports
)

echo Running Newman collection...
npx newman run collections/qa-api-tests-full-collection.json --reporters cli,html --reporter-html-export reports\report.html

REM Check if report.html was created
if exist reports\report.html (
    echo Opening report...
    start reports\report.html
) else (
    echo Failed to generate HTML report.
)

pause
