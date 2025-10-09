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

### 安装ingress-nginx

```
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.13.3/deploy/static/provider/cloud/deploy.yaml
```

```
验证ingress是否创建成功：
kubectl get ingress sanic-app-ingress

查看ingress-nginx控制器的外部IP：
kubectl get svc -n ingress-nginx

找到ingress-nginx-controller服务，查看其EXTERNAL-IP列的值，这应该就是您可以用来访问服务的IP地址。

访问服务： 由于您没有配置域名，可以直接使用ingress-nginx控制器的外部IP地址在浏览器中访问您的服务。
这样配置后，您就可以通过主节点的公网IP访问部署在Kubernetes集群中的sanic应用了。
```
