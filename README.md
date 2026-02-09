# Family Tree

Сервис для составления генеалогического древа

## Запуск проекта

### 1. Клонирование репозитория

```bash
git clone https://github.com/Spaceoceanoutlook/FamilyTree.git
```
Открыть проект в редакторе, в корне проекта создать файл `.env` и добавить следующие переменные:
```
POSTGRES_USER=user
POSTGRES_PASSWORD=1234
POSTGRES_DB=familytree_db
POSTGRES_HOST=db
POSTGRES_PORT=5432
```
В системе должен быть установлен poetry

Установка библиотек:
```bash 
poetry install
```

Для корректной работы приложения, версия python должны быть < 3.14

Если глобальная версия python >= 3.14, то установить 3.13.0 через pyenv, после чего выполнить
```bash 
poetry env use ~/.pyenv/versions/3.13.0/bin/python
```

Активировать виртуальное окружение:
```bash 
poetry env activate
```
Запустить приложение
```bash 
docker compose up --build -d
```
Создать и применить миграцию:
```bash 
docker compose exec api alembic revision --autogenerate -m "init"
docker compose exec api alembic upgrade head
```
