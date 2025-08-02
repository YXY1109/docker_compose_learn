# 构建镜像

## 进入容器

```
docker run -it --name sanic-temp python:3.11-slim /bin/bash
```

## 更新系统包（可选）

```
apt-get update && apt-get install -y --no-install-recommends gcc
执行上面更新很慢的话，可以使用国内源

cat > /etc/apt/sources.list <<EOF
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free
deb https://mirrors.tuna.tsinghua.edu.cn/debian-security/ bookworm-security main contrib non-free
EOF
```

## 安装依赖包

pip install sanic==25.3.0 -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

## 清理缓存（减小镜像体积）

pip cache purge && apt-get clean && rm -rf /var/lib/apt/lists/*

## 新开窗口，生成镜像

docker commit sanic-temp sanic_demo:v2.0

## 启动docker-compose

- cd /root/code/docker_compose_learn/build_image_2
- docker-compose -f docker-compose-sanic.yml up

## 缺少依赖包，再次进入容器安装依赖包

> 启动容器：
> docker run -d --name sanic-temp sanic_demo:v2.0 tail -f /dev/null
>
> 进入容器：
> docker exec -it sanic-temp /bin/bash
>
> 安装依赖包：
> pip install loguru==0.7.3 -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
>
> 再次生成镜像：
> docker commit sanic-temp sanic_demo:v2.1
>
> 修改docker-compose.yml文件，版本升级到v2.1
>
> 启动docker-compose：
> docker-compose -f docker-compose-sanic.yml up
>
> 访问：curl http://localhost:8012/api

