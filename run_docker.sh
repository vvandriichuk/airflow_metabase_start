echo killing old docker processes
docker-compose -f airflow/docker-compose.yml rm -fs
docker-compose -f postgres_collect_data/docker-compose.yml rm -fs
docker-compose -f metabase/docker-compose.yml rm -fs

echo building docker containers
docker-compose -f airflow/docker-compose.yml up -d --build
docker-compose -f postgres_collect_data/docker-compose.yml up -d --buil
docker-compose -f metabase/docker-compose.yml up -d --build


