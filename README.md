# 学习记录

docker构建镜像，docker-compose运行服务，k8s集群部署

### bge_web

将bge模型，使用sanic部署为web服务

### build_image_1

使用dockerfile构建镜像

### build_image_2

使用docker run进入容器，安装依赖包，生成镜像，docker-compose启动服务

### docker-compose

使用docker-compose启动带有gpu的服务

### k8s_learn

使用3台腾讯云服务器，系统ubuntu22.04部署k8s集群

### k8s_sanic

将sanic服务器运行在k8s集群中，代码保存到github，通过actions 自动部署到k8s集群

### 使用UV

- 没有pyproject.toml文件
    - uv init
    - uv venv .venv --python 3.11
    - uv add sanic(如果未切换虚拟环境，会自动创建虚拟环境.venv，所以创建的时候最好一致)
- 已有pyproject.toml文件
    - pip install uv
    - uv sync
