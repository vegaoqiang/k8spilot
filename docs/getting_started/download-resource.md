# 下载离线资源
当使用离线方案部署Kubernetes集群时，需要首先下载离线资源，k8spilot提供了离线资源下载脚本，本文档主要介绍使用k8spilot下载离线资源，也可以手动下载需要的离线资源，存放在指定的目录结构即可，见 [k8spilot离线资源目录结构](#离线资源目录结构)


## 使用pilot下载离线资源

**下载所有离线文件**
```shell
./pilot dl
```
执行以上命令开始下载所有离线资源，所有离线资源的版本为k8spilot预设的默认版本

**指定kubernetes版本**
```shell
./pilot dl --kube v1.33.3
```
执行以上命令开始下载Kubernetes v1.33.3版本离线资源及所有其他默认的离线组件和镜像

**仅下载kubernetes离线资源**
```shell
./pilot dl --kube v1.33.3 --only
```
指定`--only`参数，让pilot仅下载kubernetes离线资源，跳过组件以及镜像资源的下载
> `--only`参数仅搭配`--kube`生效

**指定平台架构**
```shell
./pilot dl --kube v1.33.3 --arch arm64 --only
```
指定以上命令将下载ARM平台的Kubernetes v1.33.3版本离线资源

**指定集群环境**
```shell
./pilot dl --env mycluster
```
执行以上命令将下载`mycluster`环境对应的离线资源，可搭配`--kube v1.33.3`,`--arch arm64`等参数指定自定义版本

>当pilot部署多个环境的Kubernetes集群时，不同环境对应组件版本可能不一样，使用`--env`指定环境可下载对应版本的离线资源

## 离线资源目录结构

+ **kubernetes** 目录用于存放各版本kubenetes二进制文件
+ **components** 目录用于存放所有集群组件二进制包和文件
+ **images**  目录用于存放组件对应的离线镜像
+ **charts**  目录用于存放组件的helm chart离线文件

```
resources
├── charts
│   ├── cilium-1.17.6.tgz
│   ├── csi-driver-nfs-4.11.0.tgz
│   ├── ingress-nginx-v1.13.0.yaml
│   └── tigera-operator-v3.30.2.tgz
├── components
│   ├── cfssl_1.6.5_linux_amd64
│   ├── cfssl_1.6.5_linux_arm64
│   ├── cfssljson_1.6.5_linux_amd64
│   ├── cfssljson_1.6.5_linux_arm64
│   ├── cilium-1.17.6.tgz
│   ├── cni-plugins-linux-amd64-v1.7.1.tgz
│   ├── containerd-1.7.28-linux-amd64.tar.gz
│   ├── containerd-1.7.28-linux-arm64.tar.gz
│   ├── csi-driver-nfs-4.11.0.tgz
│   ├── etcd-v3.6.2-linux-amd64.tar.gz
│   ├── etcd-v3.6.2-linux-arm64.tar.gz
│   ├── go-containerregistry_Darwin_arm64.tar.gz
│   ├── helm-v3.17.4-linux-amd64.tar.gz
│   ├── ingress-nginx-v1.13.0.yaml
│   ├── runc.amd64
│   └── tigera-operator-v3.30.2.tgz
├── images
│   ├── calico
│   │   └── v3.30.2
│   │       ├── amd64
│   │       │   ├── cni.tar
│   │       │   ├── kube-controllers.tar
│   │       │   ├── node.tar
│   │       │   ├── operator.tar
│   │       │   ├── pilot-job.tar
│   │       │   ├── pod2daemon-flexvol.tar
│   │       │   └── typha.tar
│   │       └── arm64
│   │           ├── kube-controllers.tar
│   │           ├── node.tar
│   │           ├── operator.tar
│   │           └── pod2daemon-flexvol.tar
│   ├── cilium
│   │   └── v1.17.6
│   │       └── amd64
│   │           ├── cilium-envoy.tar
│   │           ├── cilium.tar
│   │           └── operator-generic.tar
│   ├── coredns
│   │   └── v1.12.2
│   │       └── amd64
│   │           └── coredns.tar
│   ├── csi-nfs
│   │   └── v4.11.0
│   │       └── amd64
│   │           ├── csi-node-driver-registrar.tar
│   │           ├── csi-provisioner.tar
│   │           ├── csi-resizer.tar
│   │           ├── csi-snapshotter.tar
│   │           ├── livenessprobe.tar
│   │           ├── nfs-server-alpine.tar
│   │           ├── nfsplugin.tar
│   │           └── snapshot-controller.tar
│   ├── ingress-nginx
│   │   └── v1.13.0
│   │       └── amd64
│   │           ├── controller.tar
│   │           └── kube-webhook-certgen.tar
│   └── pause
│       └── 3.9
│           └── amd64
│               └── pause.tar
└── kubernetes
    ├── v1.31.11
    │   ├── amd64
    │   │   ├── kube-apiserver
    │   │   ├── kube-controller-manager
    │   │   ├── kube-scheduler
    │   │   ├── kubectl
    │   │   └── kubelet
    │   └── arm64
    └── v1.33.3
        ├── amd64
        │   ├── kube-apiserver
        │   ├── kube-controller-manager
        │   ├── kube-scheduler
        │   ├── kubectl
        │   └── kubelet
        └── arm64
            ├── kube-apiserver
            ├── kube-controller-manager
            ├── kube-scheduler
            ├── kubectl
            └── kubelet

30 directories, 61 files
```