# 服务部署

### deploy中Secrets 设置

配置位置：仓库 Settings > Secrets and variables > Actions

### dockerhub

1. 登录：https://app.docker.com
2. 点击右上角头像 → Account Settings。
3. 左侧选择 Personal access tokens → Generate new token。
4. 创建令牌后，复制它并粘贴到 GitHub 的 DOCKERHUB_TOKEN 中。

### 配置kubeconfig密钥

1. 主节点执行，获取秘钥：kubectl config view --raw
2. 复制整个秘钥，粘贴到github的KUBE_CONFIG中
3. 需要将内网IP地址替换成公网IP
