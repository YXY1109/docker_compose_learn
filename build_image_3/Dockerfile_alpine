# 优化的多阶段构建 Dockerfile
FROM python:3.11-alpine as builder

# 设置构建环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# 安装构建依赖 - 合并为一个 RUN 指令优化层缓存
RUN apk add --no-cache --update \
    build-base \
    python3-dev \
    musl-dev \
    linux-headers \
    cmake \
    make \
    pkgconfig \
    libpng-dev \
    libjpeg-turbo-dev \
    libffi-dev \
    libwebp-dev \
    tiff-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tk-dev \
    libimagequant-dev \
    wget \
    unzip \
    && rm -rf /var/cache/apk/*

# 升级 pip 和安装构建工具
RUN python -m ensurepip --upgrade && \
    pip install --upgrade pip setuptools wheel --no-cache-dir -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 创建虚拟环境以避免权限问题
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 批量安装 Python 包 - 优化缓存和下载速度
RUN pip install --no-cache-dir \
    fastapi==0.120.4 \
    uvicorn==0.38.0 \
    Pillow==10.4.0 \
    safetensors==0.6.2 \
    pypdf==6.1.3 \
    numpy==2.3.4 \
    -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 单独安装 paddlepaddle 和 paddleocr (使用官方源)
RUN pip install --no-cache-dir \
    paddlepaddle==3.2.0 \
    -i https://www.paddlepaddle.org.cn/packages/stable/cpu/ && \
    pip install --no-cache-dir \
    paddleocr[doc-parser]==3.2.0 \
    -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# 生产阶段 - 最小化镜像
FROM python:3.11-alpine as runtime

# 设置运行时环境变量
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

# 只安装运行时依赖
RUN apk add --no-cache \
    libpng \
    libjpeg-turbo \
    libffi \
    libwebp \
    tiff \
    freetype \
    lcms2 \
    openjpeg \
    tk \
    libstdc++ \
    libgcc \
    && rm -rf /var/cache/apk/*

# 创建非 root 用户
RUN addgroup -g 1000 appgroup && \
    adduser -D -s /bin/sh -u 1000 -G appgroup -h /app appuser

# 设置工作目录
WORKDIR /app

# 从构建阶段复制 Python 环境
COPY --from=builder /opt/venv /opt/venv

# 复制应用代码 (使用 chown 减少权限问题)
COPY --chown=1000:1000 requirements.txt ./
COPY --chown=1000:1000 . .

# 创建必要的目录
RUN mkdir -p /app/storage /app/logs && \
    chown -R 1000:1000 /app

# 切换到非 root 用户
USER 1000:1000

# 暴露端口
EXPOSE 5000

# 健康检查
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# 启动应用
CMD ["python", "start.py"]