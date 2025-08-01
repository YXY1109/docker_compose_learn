# 构建镜像

```
docker build -t sanic_demo:v1.0 .

docker-compose -f docker-compose-sanic.yml up

curl http://localhost:8011/api

```