# Dev environment
up:
    docker compose -f docker-compose.dev.yml up --build -d

down:
    docker compose -f docker-compose.dev.yml down

logs:
    docker compose -f docker-compose.dev.yml logs -f

# Database
db-shell:
    docker exec -it familytreedb psql -U user -d familytree_db