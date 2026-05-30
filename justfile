up:
    docker compose -f docker-compose.dev.yml up --build -d

down:
    docker compose -f docker-compose.dev.yml down

shell:
    docker exec -it familytreedb psql -U user -d familytree_db