up:
    docker compose up --build -d

down:
    docker compose down

shell:
    docker exec -it familytreedb psql -U user -d familytree_db