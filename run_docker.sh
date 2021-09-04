echo killing old docker processes
docker-compose rm -fs

echo building docker containers
docker-compose -f airflow/docker-compose.yml up --build

echo building docker containers
docker-compose -f metabase/docker-compose.yml up --build

echo building docker containers
docker-compose -f postgres_collect_data/docker-compose.yml up --build
