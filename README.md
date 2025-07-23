# k8spilot
k8spilot可以简单、快速的搭建一个生产级别的Kuebrnetes集群；k8spilot能帮你完成搭建Kubernetes集群时所有复杂的操作，你要做的，只需要提供运行Kubernetes的主机或服务器。k8spilot安装Kubernetes集群的速度取决于你电脑和服务器的互联网下载速度。

## 功能概述
+ Kubernetes安装版本可自定义，可选参考: [版本列表](https://dl.k8spilot.icu/kubernetes/kube-versions)
+ Kubernetes所有组件裸运行在系统中，而不是容器化部署，更稳定和易维护
+ 无docker，采用更现代的containerd作为容器运行时
+ 高性能网络插件cilium，默认开启BPF模式（网络插件可选calico）
+ 支持x86_64和aarch64架构服务器，自适应部署对应架构Kubernetes
+ 安装CoreDNS为集群DNS
+ 安装helm工具，helm安装在master节点上
+ 可选安装csi-driver-nfs作为集群默认StorageClass
+ 可选ingress-nginx作为集群默认IngressClass

## 快速开始
以下两种方式都可以使用k8spilot部署Kubernetes集群, 在开始使用k8spilot前，需要先明白k8spilot中的两个名词：**控制端**和**被控端**  
**主控端**  
运行k8spilot的机器，可以是你的笔记本电脑，可以是一台独立服务器，也可以是被控端机器中的任意一台。主控端需要满足以下要求  
+ 主控端要求能连接互联网，能与所有被控端通过ssh连接
+ 主控端必须是Linux/MacOS，不支持Windows（windows使用docker或者wsl方案替代）
+ 主控端必须安装了Python 3.10及以上版本
**被控端**
+ 被控端要求能连接互联网，并且所有被控端之间网络互通
### Ansible
#### 使用方法
见：

### Docker
todo

## 支持的Linux发行版本
+ :penguin: **CentOS Stream** 9/10
+ :penguin: **Rocky Linux** 8/9/10
+ :penguin: **Oracle Linux** 8/9/10
+ :penguin: **Debian** Bullseye/Bookworm
+ :penguin: **Ubuntu** 22.04/24.04
+ :penguin: **Fedore** 39/40
+ :penguin: **openSUSE** 
+ :penguin: **openEuler** 2203/2403
+ :penguin: **Alibaba Cloud Linux**
+ :penguin: **Kylin Linux Advanced Server V10** Halberd

## 集群组件
+ **kubernetes**
+ **etcd**
+ **containerd**
+ **runc**
+ **cni-plugins**
+ **pause**
+ **CoreDNS**

## 工具
+ **helm**

## 存储插件
+ **csi-driver-nfs**

## 网络插件
+ **clilum** v16.3
+ **calico** v3.30.2

> 网络插件安装时默认开启BPF模式，kube-proxy将被忽略安装

## Ingress Plugins
+ **cilium ingress** 安装cilium网络时，默认开启cilium ingress功能作为默认ingress
+ **ingress-nginx** 可选安装ingress-nginx作为默认ingress