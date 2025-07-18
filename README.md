# 一键部署Kubernetes集群

## 快速开始
以下两种方式都可以使用k8spilot部署Kubernetes集群

### Ansible
#### 使用方法
见：

### Docker
todo

## 支持的Linux发行版本
+ :penguin: **CentOS Stream** 9/10
+ :penguin: **Debian** Bullseye/Bookworm
+ :penguin: **Ubuntu** 22.04/24.04
+ :penguin: **Fedore** 39/40
+ :penguin: **openSUSE** 
+ :penguin: **Oracle Linux** 8/9
+ :penguin: **Rocky Linux** 8/9
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