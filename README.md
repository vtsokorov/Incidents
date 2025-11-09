# Incidents

# При разработке использовался Python 3.14.

## Для запуска необходимо выполнить:
- Клонировать репозиторий
- Создать виртуальное окружение в каталоге проекта (python -m venv venv)
- pip install -r requirements.txt
- flask db upgrade
- flask --app app run

# Документация API:
http://localhost:5000/swagger/

# Состояние API:
http://localhost:5000/health

Методы API:
[POST] /api/v1/incident - Создать новый инцидент
Пример: curl -X POST "http://localhost:5000/api/v1/incident" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"description\":\"Новая проблема\", \"source\":\"operator\"}"

[GET] /api/v1/incident/{incident_id} - Получить инцидент по ID
Пример: curl -X GET "http://localhost:5000/api/v1/incident/1" -H  "accept: application/json"

[PATCH] /api/v1/incident/{incident_id} - Обновить статус инцидента
Пример: curl -X PATCH "http://localhost:5000/api/v1/incident/1" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"status\":\"closed\"}"

[GET] /api/v1/incidents - Получить список инцидентов
Пример: curl -X GET "http://localhost:5000/api/v1/incidents?page=1&length=10&status=reported" -H  "accept: application/json"