# 建立镜像

docker-compose build

postgis不需要镜像，直接建立容器就行

# 建立网络

docker network create Gisnet

# 建立容器

docker-compose up -d

-d 是放在后台

# 删除容器

docker-compose down

# Swagger

localhost:5000/apidocs

# Port
Gisapp 8080
Gisback 5000
Gisdata 80, localhost