# create network

docker network create Gisnet

# build container

docker-compose up -d

# shut down and delete container

docker-compose down

# Web

localhost:8080

# Swagger

localhost:5000/apidocs

## Port Gisapp 8080
## Port Gisback 5000
## Port Gisdata 80, localhost

## SQL
You should use 'foldername'-postgres-1 in GisBack/__init__.py, because sql link is based on docker container name.