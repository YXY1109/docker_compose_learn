# 使用官方 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY k8s_sanic/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt