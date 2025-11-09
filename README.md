# Incidents

### Для запуска необходимо выполнить:
- Клонировать репозиторий
- Создать виртуальное окружение (python -m venv venv)
- pip install -r requirements.txt
- flask db upgrade
- flask --app app run

### Документация API:
http://localhost:5000/swagger/

### Состояние API:
http://localhost:5000/health

### Методы API:
[POST] /api/v1/incident - Создать новый инцидент <br>
<details>
<summary>Пример:</summary>
curl -X POST "http://localhost:5000/api/v1/incident" -H  "accept: */*" -H  "Content-Type: application/json" -d "{\"description\":\"Новая проблема\", \"source\":\"operator\"}"
</details>

[GET] /api/v1/incident/{incident_id} - Получить инцидент по ID <br>
<details>
<summary>Пример:</summary>
curl -X GET "http://localhost:5000/api/v1/incident/1" -H  "accept: application/json"
</details>

[PATCH] /api/v1/incident/{incident_id} - Обновить статус инцидента <br>
<details>
<summary>Пример:</summary>
curl -X PATCH "http://localhost:5000/api/v1/incident/1" -H  "accept: application/json" -H  "Content-Type: application/json" -d "{\"status\":\"closed\"}"
</details>

[GET] /api/v1/incidents - Получить список инцидентов <br>
<details>
<summary>Пример:</summary>
curl -X GET "http://localhost:5000/api/v1/incidents?page=1&length=10&status=reported" -H  "accept: application/json"
</details>

Использовался Python 3.14