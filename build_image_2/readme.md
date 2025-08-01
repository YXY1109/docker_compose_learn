# 构建镜像

```
docker run -it --name sanic-temp python:3.11-slim /bin/bash
```

```
# 更新系统包（可选）
apt-get update && apt-get install -y --no-install-recommends gcc

# 安装Sanic
pip install sanic==25.3.0

# 清理缓存（减小镜像体积）
pip cache purge && apt-get clean && rm -rf /var/lib/apt/lists/*


#新开窗口
docker commit sanic-temp sanic_demo:v2
```