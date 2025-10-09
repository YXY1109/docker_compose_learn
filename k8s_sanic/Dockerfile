# 使用官方 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY k8s_sanic/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码
COPY k8s_sanic/ .

# 暴露端口
EXPOSE 8000

# 启动应用
CMD ["python", "app.py"]