# 构建镜像

## 制作镜像

```
#切换目录
cd /root/code/docker_compose_learn/build_image_1

#构建镜像
docker build -t sanic_demo:v1.0 .

#启动镜像
docker-compose -f docker-compose-sanic.yml up
docker-compose -f docker-compose-sanic.yml logs -f -n 10

#访问
curl http://localhost:8011/api

```