# Docker Compose 学习项目 🐳

一个全面的学习项目，涵盖 Docker 容器化、Docker Compose 编排和 Kubernetes 部署。本项目演示了使用 Sanic 框架部署 Python Web 服务的各种方法，从基础 Docker 镜像到生产级 Kubernetes 集群。

## 🚀 快速开始

```bash
# 克隆仓库
git clone <repository-url>
cd docker_compose_learn

# 设置 Python 环境（使用 uv 进行依赖管理）
pip install uv
uv sync

# 探索不同项目
ls bge_web/ build_image_1/ build_image_2/ docker-compose/ k8s_learn/ k8s_sanic/
```

## 📁 项目结构

### 🤖 [bge_web/](./bge_web/)
BGE（BAAI General Embedding）模型使用 Sanic 部署为 Web 服务
- **目标**：生产环境 BGE 嵌入模型的 GPU 支持部署
- **核心文件**：
  - `1_download_bge_model.py` - 模型下载脚本
  - `2_sanic_bge.py` - BGE 推理的 Sanic Web 服务
  - `Dockerfile` - GPU 支持的容器配置
- **特性**：GPU 加速的高性能嵌入服务

### 🏗️ [build_image_1/](./build_image_1/)
使用 Sanic 的基础 Docker 镜像构建示例
- **目标**：学习基础 Docker 镜像构建技术
- **核心文件**：
  - `Dockerfile` - 多阶段构建配置
  - `sanic_demo.py` - 简单的 Sanic 应用
  - `docker-compose-sanic.yml` - 服务编排
- **学习重点**：Dockerfile 最佳实践和容器优化

### 🔧 [build_image_2/](./build_image_2/)
使用 `docker run` 安装依赖的替代方案
- **目标**：演示交互式容器开发工作流
- **核心文件**：
  - `sanic_demo.py` - 增强的 Sanic 应用
  - `docker-compose-sanic.yml` - 生产就绪配置
- **学习重点**：容器开发和从运行容器创建镜像

### ⚡ [docker-compose/](./docker-compose/)
使用 Docker Compose 的 GPU 服务
- **服务**：
  - **BGE 服务** (`bge.yml`)：端口 8011 的 BGE 嵌入模型
  - **Qwen3-30B 服务** (`qwen3-30b.yml`)：端口 8010 的大语言模型
- **特性**：NVIDIA GPU 支持、共享内存优化、集中日志
- **要求**：NVIDIA Docker 运行时、充足的 GPU 内存

### ☸️ [k8s_learn/](./k8s_learn/)
Ubuntu 22.04 上的 Kubernetes 集群部署（3台腾讯云服务器）
- **目标**：从零开始完整 K8s 集群搭建
- **组件**：
  - Calico 网络（Tigera operator）
  - MetalLB 裸金属集群负载均衡器
  - 自定义资源配置
- **学习重点**：生产集群架构和网络

### 🚀 [k8s_sanic/](./k8s_sanic/)
Kubernetes 上的 Sanic 应用，配备 GitHub Actions CI/CD
- **架构**：
  - **Deployment**：滚动更新的 Pod 管理
  - **Service**：集群内部通信
  - **Ingress**：通过 nginx ingress controller 的外部访问
  - **MetalLB**：裸金属环境负载均衡
- **CI/CD**：主分支推送的自动构建和部署
- **监控**：自动滚动重启和健康检查

## 🛠️ 开发工作流

### 1. 本地开发
```bash
# 设置环境
uv sync

# 本地运行
python bge_web/2_sanic_bge.py
python build_image_1/sanic_demo.py
```

### 2. Docker 测试
```bash
# 构建镜像
docker build -t bge-service:latest bge_web/
docker build -t sanic-demo:latest build_image_1/

# 使用 compose 测试
docker-compose -f docker-compose/bge.yml up -d
docker-compose -f docker-compose/qwen3-30b.yml up -d
```

### 3. Kubernetes 部署
```bash
# 手动部署
kubectl apply -f k8s_sanic/k8s/deployment.yaml
kubectl apply -f k8s_sanic/k8s/service.yaml
kubectl apply -f k8s_sanic/k8s/ingress.yaml

# 检查状态
kubectl get pods,svc,ingress

# 重启部署
kubectl rollout restart deployment/sanic-app-deployment
```

## 🔧 环境设置

### Python 环境（使用 uv）
```bash
# 新项目（无 pyproject.toml）
uv init
uv venv .venv --python 3.11
uv add sanic

# 现有项目
pip install uv
uv sync
```

### GPU 要求
- **NVIDIA Docker 运行时**：所有 GPU 服务必需
- **CUDA 支持**：确保与模型的 CUDA 兼容性
- **内存分配**：BGE 最少 16GB GPU 内存，Qwen3-30B 需要 80GB+

### 模型路径
GPU 服务期望模型位于以下主机路径：
- `/home/models/bge_m3` → `/models/bge_m3`（容器）
- `/home/models/bge-reranker-v2-m3` → `/models/bge-reranker-v2-m3`（容器）
- `/home/models/qwen3_30b_a3b` → `/models/qwen3_30b_a3b`（容器）

## 📊 服务架构

### 端口映射
| 服务 | 主机端口 | 容器端口 | 用途 |
|---------|-----------|----------------|---------|
| BGE 服务 | 8011 | 8011 | 嵌入 API |
| Qwen3-30B | 8010 | 8000 | LLM 推理 |
| Sanic 演示 | 8011 | 8011 | 开发测试 |
| K8s Sanic | N/A | 8000 | 生产服务 |

### 通用配置
```yaml
# 标准环境变量
TZ: Asia/Shanghai
ENVIRONMENT: production
PYTHONUNBUFFERED: 1
PYTHONDONTWRITEBYTECODE: 1

# GPU 配置
runtime: nvidia
deploy:
  resources:
    reservations:
      devices:
        - driver: nvidia
          device_ids: ['0']
          capabilities: [gpu]

# 性能调优
shm_size: '50g'    # 大模型使用 '100g'
logging:
  driver: "json-file"
  options:
    max-size: "500m"
    max-file: "5"
```

## 🔄 CI/CD 流水线

### GitHub Actions 工作流
- **触发器**：影响 `k8s_sanic/` 目录的主分支推送
- **步骤**：
  1. 构建多平台 Docker 镜像
  2. 推送到 DockerHub 并添加时间戳标签
  3. 部署到 Kubernetes 集群
  4. 重启部署以实现无缝更新

### 必需的密钥
- `DOCKERHUB_USERNAME`：Docker Hub 注册表凭据
- `DOCKERHUB_TOKEN`：Docker Hub 访问令牌
- `KUBE_CONFIG`：Kubernetes 集群配置

## 📚 学习路径

### 初学者
1. 从 `build_image_1/` 开始学习 Docker 基础
2. 探索 `build_image_2/` 了解容器开发工作流
3. 使用本地 Sanic 应用进行练习

### 中级者
1. 学习 `bge_web/` 的生产就绪服务
2. 使用 `docker-compose/` 部署 GPU 服务
3. 学习服务编排和扩展

### 高级者
1. 使用 `k8s_learn/` 构建自己的 K8s 集群
2. 使用 `k8s_sanic/` 实现 CI/CD
3. 优化生产工作负载

## 🤝 贡献

这是一个学习仓库。欢迎：
- 探索不同的部署策略
- 试验配置
- 从真实示例中学习
- 通过问题提出改进建议

## 📄 许可证

本项目用于教育目的。请参考各个组件的具体许可证。

---

**用 ❤️ 构建，专注于学习 Docker、Kubernetes 和云原生开发**