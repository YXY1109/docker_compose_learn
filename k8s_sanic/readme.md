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
kubectl delete -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.13.3/deploy/static/provider/cloud/deploy.yaml
以上文件镜像地址是带digest，不走hosts.toml重定向规则。所以需要修改文件，一定要删除 @sha256
先下载文件，将三处image:替换国内的镜像源

一处：
image: registry.k8s.io/ingress-nginx/controller:v1.13.3@sha256:1b044f6dcac3afbb59e05d98463f1dec6f3d3fb99940bc12ca5d80270358e3bd
改为：
image: ccr.ccs.tencentyun.com/tkeimages/ingress-nginx-controller:v1.13.3

两处：
image: registry.k8s.io/ingress-nginx/kube-webhook-certgen:v1.6.3@sha256:3d671cf20a35cd94efc5dcd484970779eb21e7938c98fbc3673693b8a117cf39
改为：
image: ccr.ccs.tencentyun.com/tkeimages/ingress-nginx-kube-webhook-certgen:v1.6.3

将deploy.yaml改名为：ingress-nginx-deploy.yaml
kubectl delete -f ingress-nginx-deploy.yaml   # 如果之前部署过
kubectl apply -f ingress-nginx-deploy.yaml

kubectl get ns ingress-nginx


强制删除：
kubectl get ns ingress-nginx -o json > ingress-nginx.json
vi ingress-nginx.json
将："spec": {
  "finalizers": [
    "kubernetes"
  ]
}
改为："spec": {}
kubectl replace --raw "/api/v1/namespaces/ingress-nginx/finalize" -f ./ingress-nginx.json

kubectl -n ingress-nginx get all
kubectl -n ingress-nginx delete pods --all
kubectl -n ingress-nginx delete svc --all
kubectl -n ingress-nginx delete deploy --all
kubectl -n ingress-nginx delete daemonset --all


查看ingress-nginx控制器的pod：
kubectl -n ingress-nginx get pods
kubectl describe pod ingress-nginx-admission-create-blfhf -n ingress-nginx

```

```
验证ingress是否创建成功：
kubectl get ingress sanic-app-ingress

查看ingress-nginx控制器的外部IP：
kubectl get svc -n ingress-nginx

找到ingress-nginx-controller服务，查看其EXTERNAL-IP列的值，这应该就是您可以用来访问服务的IP地址。

访问服务： 由于您没有配置域名，可以直接使用ingress-nginx控制器的外部IP地址在浏览器中访问您的服务。
这样配置后，您就可以通过主节点的公网IP访问部署在Kubernetes集群中的sanic应用了。

删除po：
kubectl delete pod ingress-nginx-admission-create-ndpwb -n ingress-nginx
kubectl delete pod ingress-nginx-admission-patch-q2nh7 -n ingress-nginx
kubectl delete pod ingress-nginx-controller-69f6c6b89d-h5wmc -n ingress-nginx

查看po：
kubectl get po -n=ingress-nginx

查看po日志：
kubectl describe pod ingress-nginx-admission-create-dlmrj -n ingress-nginx

```
