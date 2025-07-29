@echo off
echo Запуск тестов с HTML-отчётом...

newman run collections\users-tests.postman_collection.json ^
  -e environments\gorest.postman_environment.json ^
  -r cli,html ^
  --reporter-html-export reports\report.html

echo ---------------------------
echo ✅ Готово! Отчёт в: reports\report.html
pause