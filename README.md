# Домашние задания от 1 до 6 (Flask API)

Проект расширяет практику SQLAlchemy: добавлены модели `Category` и `Question`, связь по внешнему ключу, Pydantic-схемы и REST API категорий/вопросов.

## 1. Установка (Windows / PyCharm)

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Миграция базы данных

В терминале из папки проекта:

```bash
flask --app app db init
flask --app app db migrate -m "add categories and questions"
flask --app app db upgrade
```

Если папка `migrations` уже существует, пропустите `db init`. После изменения моделей повторите `db migrate` и `db upgrade`.

## 3. Запуск

```bash
python app.py
```

Откройте `http://127.0.0.1:5000/`. API использует SQLite `instance/practicum3.db`.

## 4. Эндпоинты

| Метод | URL | Назначение |
|---|---|---|
| POST | `/categories` | Создать категорию: `{"name":"Python"}` |
| GET | `/categories` | Список категорий |
| PUT | `/categories/1` | Изменить имя категории |
| DELETE | `/categories/1` | Удалить категорию |
| GET | `/questions` | Список вопросов с информацией о категории |
| POST | `/questions` | Создать вопрос, можно передать `category_id` |

Пример тела для вопроса:
```json
{"title":"Что такое Flask?","text":"Python web framework","category_id":1}
```

При удалении категории вопросы сохраняются, а `category_id` становится `null`.
Ошибки валидации возвращаются с HTTP 400, отсутствующие записи — с 404, повтор имени категории — с 409.

## 5. Быстрая проверка через curl

```bash
curl -X POST http://127.0.0.1:5000/categories -H "Content-Type: application/json" -d "{\"name\":\"Python\"}"
curl http://127.0.0.1:5000/categories
curl -X POST http://127.0.0.1:5000/questions -H "Content-Type: application/json" -d "{\"title\":\"Что такое API?\",\"text\":\"Интерфейс взаимодействия\",\"category_id\":1}"
curl http://127.0.0.1:5000/questions
```

## Структура

- `app.py` — Flask-приложение и маршруты
- `models.py` — SQLAlchemy-модели и связь
- `schemas/question.py` — Pydantic-схемы
- `requirements.txt` — зависимости
- `migrations/` — создаётся Flask-Migrate командами выше
