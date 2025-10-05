# K8S学习笔记

## 一，购买服务器

对比了腾讯云，阿里云，百度云。腾讯云价格更便宜，选择了腾讯云
![服务器订单](images/服务器订单.png)

## 二，安装K8S集群

[参考文章1](https://developer.aliyun.com/article/1445670)
[参考文章2](https://blog.csdn.net/m0_53928179/article/details/139068769)

- sudo su
- 关闭防火墙：
    - systemctl disable --now ufw
- 设置主机名称
    - 10.6.0.9机器：hostnamectl set-hostname k8s-master
    - 10.6.0.14机器：hostnamectl set-hostname k8s-worker1
    - 10.6.0.8机器：hostnamectl set-hostname k8s-worker2
    - 查看主机名：hostnamectl
- 配置hosts配置文件
    - vi /etc/hosts
    - 添加如下内容，内网ip
        - #k8s
        - 10.6.0.9 k8s-master
        - 10.6.0.14 k8s-worker1
        - 10.6.0.8 k8s-worker2
- 转发 IPv4 并让 iptables 看到桥接流量

```
# 1. 写入 modules-load 配置文件
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf
overlay
br_netfilter
EOF

# 2. 立即加载内核模块
sudo modprobe overlay
sudo modprobe br_netfilter

# 3. 写入 sysctl 配置文件
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf
net.bridge.bridge-nf-call-iptables  = 1
net.bridge.bridge-nf-call-ip6tables = 1
net.ipv4.ip_forward                 = 1
EOF

# 4. 立即应用 sysctl 配置
sudo sysctl --system
```

- 安装containerd

```
下载：curl -LO https://github.com/containerd/containerd/releases/download/v2.1.4/containerd-2.1.4-linux-amd64.tar.gz
解压：sudo tar -zxvf containerd-2.1.4-linux-amd64.tar.gz -C /usr/local
查看版本：containerd -v
配置：sudo mkdir /etc/containerd
创建配置文件：sudo containerd config default | sudo tee /etc/containerd/config.toml
```
