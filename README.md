# k8spilot
k8spilot可以简单、快速的搭建一个生产级别，纯净的Kuebrnetes集群；能帮你完成搭建Kubernetes集群时所有复杂的操作，你要做的，只需要提供运行Kubernetes的主机或服务器。k8spilot安装Kubernetes集群的速度取决于你电脑和服务器的互联网下载速度。

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
在开始使用k8spilot前，需要先明白k8spilot中的两个名词：**控制端**和**被控端**  

**主控端**  
运行k8spilot的机器，可以是你的笔记本电脑，可以是一台独立服务器，也可以是被控端机器中的任意一台。主控端需要满足以下要求  
+ 主控端要求能连接互联网，能与所有被控端通过ssh连接(如果主控端不能连接互联网，请参见离线方案: k8spilot-offline)
+ 主控端必须是Linux/MacOS，不支持Windows（Windows使用docker或者wsl方案替代）
+ 主控端必须安装了Python 3.10及以上版本，否则，需要升级Python版本，参见：[Python安装方法](docs/getting_started/install-python.md)    

**被控端**  
用于安装Kubernetes集群的虚拟机或者服务器，被控端需要满足以下要求  
+ 被控端只能是Linux，且内核版本>=5.4,受支持的Linux发现版本见：[支持的Linux发行版本](#支持的Linux发行版本)
+ 被控端要求能连接互联网，并且所有被控端之间网络互通(如果被控端不能连接互联网，请参见离线方案: k8spilot-offline)


### 安装k8spilot
如果主控端安装有Docker服务，推荐使用k8spilot的Docker镜像，因为k8spilot和所需要的依赖都已经在镜像中准备就绪，你无需操心主控端的环境和依赖问题。  
没有Docker也不必担心，只需简单几步就能安装k8spilot，见

[Getting started](docs/getting_started/getting-started.md)


## 支持的Linux发行版本
以下Linux发行版支持作为被控端安装Kubernetes集群  

+ :penguin: **CentOS Stream** 9/10
+ :penguin: **Rocky Linux** 8/9/10
+ :penguin: **Oracle Linux** 8/9/10
+ :penguin: **Debian** Bullseye/Bookworm
+ :penguin: **Ubuntu** 22.04/24.04
+ :penguin: **Fedore** 39/40
+ :penguin: **openSUSE** 
+ :penguin: **openEuler** 2203/2403
+ :penguin: **Alibaba Cloud Linux** 3
+ :penguin: **Kylin Linux Advanced Server V10** Halberd

## 集群组件版本矩阵
|component name | version |
| - | - |
| **kubernetes** | v1.30.4+ |
| **etcd** | v3.6.2 |
| **containerd** | v2.1.3 |
| **runc** | v1.3.0 |
| **cni-plugins** | v1.7.1 |
| **pause** | v3.9 |
| **CoreDNS** | v1.12.2 |

## 工具
+ **helm** v3.17.4

## 存储插件
+ **csi-driver-nfs** v4.11.0

## 网络插件
+ **clilum** v1.16.12
+ **calico** v3.30.2

> 网络插件安装时默认开启BPF模式，kube-proxy将被忽略安装

## Ingress Plugins
+ **cilium ingress** 安装cilium网络时，默认开启cilium ingress功能作为默认ingress
+ **ingress-nginx** 可选安装ingress-nginx作为默认ingress