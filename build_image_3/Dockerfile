# Multi-stage build to handle opencv compilation timeout
FROM python:3.11-alpine as opencv-builder

# Set build environment for opencv
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install opencv build dependencies
RUN apk add --no-cache \
    zlib \
    sqlite-libs \
    musl-dev \
    linux-headers \
    gcc \
    g++ \
    python3-dev \
    cmake \
    make \
    wget \
    unzip \
    pkgconfig \
    libpng-dev \
    libjpeg-turbo-dev \
    libffi-dev \
    gcompat \
    libstdc++ \
    libgcc \
    libwebp-dev \
    tiff-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tk-dev \
    libimagequant-dev

# Upgrade pip and install wheel for faster compilation
RUN python -m ensurepip --upgrade && \
    pip install --upgrade pip setuptools wheel

# Install opencv-contrib-python (this is the slow step, isolated in its own stage)
# RUN pip install --prefer-binary --compile opencv-contrib-python==4.10.0.84
# 测试流程
RUN pip install pytest isort -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# Final stage - copy opencv from builder stage
FROM python:3.11-alpine

# Set build environment
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install runtime dependencies only (no build tools needed for final image)
RUN apk add --no-cache \
    zlib \
    sqlite-libs \
    musl-dev \
    linux-headers \
    gcc \
    g++ \
    python3-dev \
    cmake \
    make \
    wget \
    unzip \
    pkgconfig \
    libpng-dev \
    libjpeg-turbo-dev \
    libffi-dev \
    gcompat \
    libstdc++ \
    libgcc \
    libwebp-dev \
    tiff-dev \
    freetype-dev \
    lcms2-dev \
    openjpeg-dev \
    tk-dev \
    libimagequant-dev

# Create non-root user early to leverage layer caching
RUN addgroup -g 1000 appgroup && \
    adduser -D -s /bin/sh -u 1000 -G appgroup -h /app appuser

# Set work directory
WORKDIR /app

# Copy opencv from builder stage (Alpine Python packages are in /usr/lib/python3.11/site-packages/)
COPY --from=opencv-builder /usr/local/lib/ /usr/local/lib/

# 测试流程
RUN pip show pytest isort

# Upgrade pip and install basic packages
RUN python -m ensurepip --upgrade && \
    pip install --upgrade pip setuptools wheel -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# Install specific versions in batches to maximize caching
RUN pip install safetensors==0.6.2 -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# Install pypdf last to override any conflicting versions
RUN pip install pypdf==6.1.3 -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# setting cl100k_base
# ENV TIKTOKEN_CACHE_DIR=/app/data/cache/tiktoken_cache \
#     NLTK_DATA=/app/data/cache/nltk_data
# Copy requirements first for better layer caching
COPY requirements.txt ./

# Copy cache and application code in order of change frequency
# COPY --chown=1000:1000 ai_core/cache /app/data/cache

# Install Pillow first with all its build dependencies available
RUN pip install Pillow==10.4.0 -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# Install dependencies in optimal order (less frequently changing first)
RUN pip install -r requirements.txt -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

RUN pip install numpy==2.3.4 -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
RUN pip install paddlepaddle==3.2.0 -i https://www.paddlepaddle.org.cn/packages/stable/cpu/

RUN pip install paddleocr[doc-parser]==3.2.0 -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple

# Copy application code
COPY --chown=1000:1000 . .

# Create necessary directories for the application
RUN mkdir -p /app/storage /app/logs && \
    chown -R 1000:1000 /app

# Switch to non-root user using numeric UID (K8s compatible)
USER 1000:1000

# Expose port
EXPOSE 5000

# Start application with production settings
CMD ["python", "start.py"]