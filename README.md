# Структура проекта
```
fastapi-wallet-project/
    |—— config/ # Настройки проекта
        |—— __init__.py
        |—— database.py
        |—— settings.py
    |—— migartions/ # Миграции проекта
    |—— nginx/ # Настройки для Nginx
    |—— tests/ # Тесты для приложений
        |—— conftest.py
    |—— users/ # Приложение пользователей
        |—— __init__.py
        |—— models.py
        |—— routers.py
        |—— schemas.py
        |—— services.py
    |—— wallet/ # Приложение кошелька
        |—— __init__.py
        |—— crud.py
        |—— models.py
        |—— routers.py
        |—— schemas.py
    |—— .dockerignore
    |—— .env.sample
    |—— .flake8
    |—— .gitignore
    |—— docker-compose.yml
    |—— Dockerfile
    |—— LICENSE
    |—— Makefile
    |—— main.py
    |—— poetry.lock
    |—— pyproject.toml
    |—— README.md
    |—— requirements.txt
```

# Как пользоваться проектом

## 1) Скопируйте проект на Ваш компьютер
```
git clone git@github.com:Nk3YQQ/fastapi-wallet-project.git
```

## 2) Добавьте файл .env для переменных окружения
Чтобы запустить проект, понадобятся переменные окружения, которые необходимо добавить в созданный Вами .env файл.

Пример переменных окружения необходимо взять из файла .env.sample

## 3) Запустите проект

Запуск проекта
```
make run
```

Остановка проекта
```
make stop
```