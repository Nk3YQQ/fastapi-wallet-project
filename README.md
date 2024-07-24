# Структура проекта
```
fastapi-wallet-project/
    |—— coverage/ # Результаты тестрования
    |—— nginx/ # Настройки для Nginx
    |—— tests/ # Тесты для приложений
        |—— conftest.py
        |—— test_wallet.py
        |—— test_users.py
    |—— users/ # Приложение пользователей
        |—— migartions/
        |—— __init__.py
        |—— database.py
        |—— models.py
        |—— schemas.py
        |—— services.py
        |—— routers.py
    |—— wallet/ # Приложение кошелька
        |—— migrations/
        |—— __init__.py
        |—— database.py
        |—— models.py
        |—— schemas.py
        |—— services.py
        |—— routers.py
    |—— .dockerignore
    |—— .env.sample
    |—— .flake8
    |—— .gitignore
    |—— docker-compose.yml
    |—— Dockerfile
    |—— LICENSE
    |—— Makefile
    |—— manage.py
    |—— poetry.lock
    |—— pyproject.toml
    |—— README.md
    |—— requirements.txt
```