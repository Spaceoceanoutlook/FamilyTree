# FamilyTree

docker compose down -v

docker compose up --build -d

docker compose exec api alembic revision --autogenerate -m "init"
docker compose exec api alembic upgrade head