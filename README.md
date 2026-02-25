# Family Tree

Сервис для составления генеалогического древа

### Запуск проекта

Клонирование репозитория

```bash
git clone https://github.com/Spaceoceanoutlook/FamilyTree.git
```
Открыть проект в редакторе, в корне проекта создать файл `.env` и добавить следующие переменные:
```
POSTGRES_USER=user
POSTGRES_PASSWORD=
POSTGRES_DB=familytree_db
POSTGRES_HOST=db
POSTGRES_PORT=5432

JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```
Генерируем хэш пароля и JWT secret key. Полученные значения добавить в .env
```bash 
docker compose run --rm api python familytree/generate_secrets.py
```
Запустить приложение
```bash 
docker compose up --build -d
```
Применить миграцию:
```bash 
docker compose exec api alembic upgrade head
```
Запускать приложение
```bash 
docker compose up -d
```
