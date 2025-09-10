# 下载离线资源
当使用离线方案部署Kubernetes集群时，需要首先下载离线资源，k8spilot提供了离线资源下载脚本，本文档主要介绍使用k8spilot下载离线资源，也可以手动下载需要的离线资源，存放在指定的目录结构即可，见 [k8spilot离线资源目录结构](#离线资源目录结构)


## 使用pilot下载离线资源
pilot会将所有离线资源下载k8spilot项目中的`resources`目录下，pilot从资源的官方github仓库和官方镜像仓库中获取对应资源文件，确保你的网络可以访问这些地址，否则可考虑使用[终端http代理](#设置终端代理) 或 [替换资源下载地址](#自定义资源下载地址)


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

>当pilot部署多个环境的Kubernetes集群时，不同环境对应组件版本可能不一样，使用`--env`指定环境可下载该环境对应版本的离线资源

## 设置终端代理
pilot支持终端代理，在开始执行下载命令前，在终端执行以下设置代理的命令，pilot将自动应用代理
```shell
# 在终端执行
export http_proxy="http://xxxx:port"
export https_proxy="http://xxxx:port"
```

## 自定义资源下载地址
当你无法访问资源下载地址或需要修改资源下载地址，如：修改指定镜像仓库为私有仓库，让离线镜像从私有仓库下载  
可通过修改`k8spilot/download-config.yml`文件修改指定资源的下载地址，`k8spilot/download-config.yml`文件记录了所有离线资源的下载地址。

:chestnut: **举个例子**  
CoreDNS官方镜像地址是`docker.io/coredns/coredns:1.12.2`,在国内大部分情况下无法访问该镜像，可通过在`k8spilot/download-config.yml`中修改CoreDNS镜像地址为`m.daocloud.io/docker.io/coredns/coredns:1.12.2`,让pilot从这个镜像地址去下载CoreDNS镜像

:frog: **注意事项**   
如果修改了镜像的地址，需要告诉k8spilot修改后的地址，否则k8spilot还是会使用原来的地址部署CoreDNS Deployment，从而导致Kubernetes无法拉取CoreDNS镜像。修改`k8spilot`安装配置文件中`registry_mirror`参数让k8spilot知道对应仓库被替换.  
示例：  
修改mycluster环境的安装配置文件 `./inventories/mycluster/group_vars/all.yml` 如下
```yml
registry_mirror:
  registry.k8s.io: "m.daocloud.io/registry.k8s.io"
  docker.io: "m.daocloud.io/docker.io"
```
以上配置告诉k8spilot:  
`registry.k8s.io`镜像仓库替换成了 `m.daocloud.io/registry.k8s.io`  
`docker.io`镜像仓库替换成了 `m.daocloud.io/docker.io`  
k8spilot在部署相关资源时即会修改其image地址为替换后的地址

## 自定义资源版本
如你修改了`mycluster`环境集群组件版本，如CoreDNS版本改为v1.12.4，现需要下载CoreDNS v1.12.4的离线镜像，可修改`k8spilot/download-config.yml`文件，在其中增加对应版本和镜像地址
```yml
coredns:
  v1.12.2:
    coredns: m.daocloud.io/docker.io/coredns/coredns:1.12.2
  v1.12.4:
    coredns: m.daocloud.io/docker.io/coredns/coredns:1.12.4
```
然后再执行: `./pilot dl --env mycluster` 可下载`coredns:1.12.4`离线镜像. 
>当然你也可以手动下载`coredns:1.12.4`离线镜像，将下载好的镜像放在`./resources/images/coredns/v1.12.4/amd64/`目录下即可


## 离线资源目录结构
`resources`为k8spilot离线资源目录，该目录需要放在k8spilot项目下，同时`resources`目录下分为四个子目录，分别存放不同类型的离线文件

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

