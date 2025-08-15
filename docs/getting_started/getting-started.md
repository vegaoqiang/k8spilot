# 开始

## 安装k8spilot
以下步骤演示将k8spilot下载安装到系统中, 如果使用k8spilot docker镜像请跳到[Docker方式使用k8spilot](#docker方式使用k8spilot)

### 下载k8spilot

```shell
tag=v1.0.3
wget https://github.com/vegaoqiang/k8spilot/archive/refs/tags/${tag}$.tar.gz
tar xf ${tag}.tar.gz
cd ${tag}
```

### 安装依赖
推荐使用Python虚拟环境

```shell
# 创建虚拟环境
python3 -m venv .venv
# 激活虚拟环境
source .venv/bin/active
# 安装依赖
pip3 -r requirments -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

> :warning: 在你的环境中，如果主控端是通过SSH密码登录被控端，主控端需要额外安装`sshpass`  
>apt仓库（Debian/Ubuntu系）
>```shell
>apt install -y sshpass
>```
>
>rpm仓库（Fedore/REHL系）
>```shell
>dnf install -y sshpass
>```


## 开始安装Kubernetes

### 创建集群环境
k8spilot支持安装和管理多套k8s集群，在开始安装Kubernetes集群之前，首先需要创建集群环境

**创建一个名为`mycluster`的集群**
```shell
./pilot create mycluster
```

集群创建成功后，可以根据需求修改 `./inventories/mycluster/group_vars/all.yml` 文件自定义Kubernetes集群安装的配置，如组件、网络插件版本等

### 安装集群
创建好 `mycluster` 集群环境后，如果你已经准备好了用于安装`mycluster`环境Kubernetes集群的虚拟机，只需执行以下操作，即可开始安装环境为 `mycluster` 的Kubernetes集群了。
```shell
./pilot deploy mycluster
```

`pilot deploy mycluster`将开始交互式录入被控端（用于安装集群的主机）信息，包含IP地址、ssh端口、ssh密码，录入完成后安装 `Ctrl + C` 结束录入，并开始安装Kubernetes
![example](/docs/images/getting-started.gif)

如果被控端（用于安装集群的主机）实例数量庞大，交互式手动输入容易出错且效率低下，此时可以手动构建被控端清单，见: [被控端清单](inventory.md)

##  Docker方式使用k8spilot

**创建`mycluster`集群环境**
```shell
sudo docker run --rm -it \
 -v $(pwd):/k8spilot/inventories \
 quay.io/k8spilot/k8spilot:v1.0.3 bash ./pilot create mycluster
```
此时如果需要编辑`mycluster`集群安装配置，可使用编辑器打开 `$(pwd)/mycluster/group_vars/all.yml` 文件进行编辑

**开始安装`mycluster`集群**
```shell
sudo docker run --rm -it \
 -v $(pwd):/k8spilot/inventories \
 -v "${HOME}"/.ssh/id_rsa:/root/.ssh/id_rsa \
 -v /tmp/.ansible_temp:/k8spilot/.ansible_temp \
 quay.io/k8spilot/k8spilot:v1.0.3 bash ./pilot deploy mycluster
```

