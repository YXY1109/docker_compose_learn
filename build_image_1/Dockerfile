# 使用官方Python基础镜像，选择3.11版本的slim版（体积较小）
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件到工作目录
COPY requirements.txt .

# 安装依赖包
RUN pip install --no-cache-dir -r requirements.txt

# 复制应用代码到工作目录
COPY sanic_demo.py .

# 暴露Sanic默认端口
# EXPOSE 8000

# 启动命令
# CMD ["python", "app.py"]
