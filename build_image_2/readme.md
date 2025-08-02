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

pip install sanic==25.3.0 -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple some-package

##清理缓存（减小镜像体积）

pip cache purge && apt-get clean && rm -rf /var/lib/apt/lists/*

## 新开窗口，生成镜像

docker commit sanic-temp sanic_demo:v2.0

