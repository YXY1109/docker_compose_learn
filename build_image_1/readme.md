# 构建镜像


## 制作镜像

```
cd /root/code/docker_compose_learn/build_image_1

docker build -t sanic_demo:v1.0 .

docker-compose -f docker-compose-sanic.yml up

curl http://localhost:8011/api

```