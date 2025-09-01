# 开始

## 安装k8spilot
以下步骤演示将k8spilot下载安装到系统中, 如果使用k8spilot docker镜像请跳到[Docker方式使用k8spilot](#docker方式使用k8spilot)

### 下载k8spilot

```shell
tag=v1.0.4
wget https://github.com/vegaoqiang/k8spilot/archive/refs/tags/${tag}.tar.gz
tar -xf ${tag}.tar.gz
cd k8spilot-${tag##*v}
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

## 创建集群环境
k8spilot支持安装和管理多套k8s集群，在开始安装Kubernetes集群之前，首先需要创建集群环境，以下是创建集群环境的几个步骤

执行以下命令开始创建`mycluster`环境：
```shell
./pilot create mycluster
```
系统会进入交互式引导，步骤如下：

### 1. 选择安装方式

系统提示：
```shell
请选择 mycluster 环境 Kubernetes 安装方式 [默认: 1]:
  1) 在线安装
  2) 离线安装
请输入选项 [1/2]:
```
此处输入 1 表示在线安装（如果直接回车，则默认选择 1）。

### 2. 选择Kubernetes版本
系统会自动获取可安装的版本，例如：
```shell
正在获取 kubernetes 版本信息
v1.30.4
v1.30.14
v1.31.11
v1.32.6
v1.33.2
请从以上版本列表选择并输入 mycluster 环境安装的 kubernetes 版本 [默认:v1.33.2]:
```
在这里输入 v1.31.11
```
已选择安装 kubernetes v1.31.11
```

### 3. 是否初始化主机清单
接下来系统会提示是否立即初始化主机清单：
```
是否初始化 mycluster 环境集群主机清单？
主机清单也可以在稍后开始安装集群后初始化，
还可以在开始安装集群之前手动编辑主机清单文件。
是否立即初始化 mycluster 环境集群主机清单？ [Y/n]:
```
如果此时选择 n
```
已跳过初始化主机清单
```
>如果被控端（用于安装集群的主机）实例数量庞大，交互式手动输入容易出错且效率低下，此时可以输入：n 跳过初始化，稍后手动构建被控端清单，见: [被控端清单](inventory.md)

### 4. 创建完成
最终提示：
```shell
mycluster 集群环境已经创建成功，可编辑 ./inventories/mycluster/group_vars/all.yml 文件，
自定义 kubernetes 集群安装参数。
使用 ./pilot deploy mycluster 命令开始部署 mycluster kubernetes 集群。
```
至此`mycluster`集群环境已经创建好了，集群环境创建成功后，可以根据需求修改 `./inventories/mycluster/group_vars/all.yml` 文件自定义Kubernetes集群安装的配置，如组件、网络插件版本等。

完整的交互信息如下图

![example](/docs/images/online_create.png)


## 安装集群
创建好集群环境后，如果你已经准备好了用于安装Kubernetes集群的虚拟机，只需执行以下操作，即可开始安装Kubernetes集群了。

执行以下命令开始安装`mycluster`环境Kubernetes：
```shell
./pilot deploy mycluster
```

如果前面创建`mycluster`集群环境时跳过了初始化主机清单，此时将开始进入交互式引导创建主机清单

### 创建主机清单
系统提示：
```info
inventory file has no section [control]
开始初始化 mycluster 集群的inventory
根据提示录入用于安装集群的主机信息，录入完成后请按: Ctrl + C 退出录入
```

#### 开始录入
系统提示：
```shell
请输入control01的IP地址:
```
请输入用于安装Kubernetes Control-Plane节点的主机IP地址，如:`1.1.1.1`,输入完成后按`enter`键进入下一步

接下来系统提示
```shell
请输入1.1.1.1的ssh端口 [默认: 22]:
```
此时输入`1.1.1.1`主机的ssh端口，如果没有输入将默认ssh端口为`22`,输入完按`enter`键进入下一项

系统提示
```shell
请输入1.1.1.1的root登录密码 [免密登录请回车跳过]:
```
输入`1.1.1.1`主机root用户的密码，如果没有输入直接按回车键跳过将使用ssh公私钥匙认证登录`1.1.1.1`，输入完成后按`enter`键进入下一项

系统提示
```shell
请输入worker01的IP地址:
```
请输入用于安装Kubernetes `Worker`节点的主机IP地址，如:`2.2.2.2`,输入完成后按`enter`键进入下一步

此时又到了输入主机ssh端口，输入完成后下一步输入主机root用户密码，按照提示输入直到完成所有`Worker`节点的录入

完成所有`Worker`节点的录入后，退出录入按：`Ctrl + C` 组合键结束录入，此时系统提示
```shell
录入终止
inventory初始化完成
```
>如果被控端（用于安装集群的主机）实例数量庞大，交互式手动输入容易出错且效率低下，可以手动构建被控端清单，见: [被控端清单](inventory.md)

#### 确认安装
完成主机清单录入后，系统将提示是否开始安装集群，提示信息入下
```shell
开始为mycluster环境安装Kubernetes v1.31.11 集群, 是否确认安装[Y/n]:
```
此时输入`y`后按`enter`键按或直接按`enter`键开始集群安装

完整的交互信息如下图

![example](/docs/images/online_deploy.png)

>如果在创建`mycluster`集群环境时已经初始化了主机清单，执行`./pilot deploy mycluster`命令安装集群时将无需在录入主机清单，直接进入[确认安装](#确认安装)提示

##  Docker方式使用k8spilot

**创建`mycluster`集群环境**
```shell
sudo docker run --rm -it \
 -v $(pwd):/k8spilot/inventories \
 quay.io/k8spilot/k8spilot:v1.0.4 bash ./pilot create mycluster
```
此时如果需要编辑`mycluster`集群安装配置，可使用编辑器打开 `$(pwd)/mycluster/group_vars/all.yml` 文件进行编辑

**开始安装`mycluster`集群**
```shell
sudo docker run --rm -it \
 -v $(pwd):/k8spilot/inventories \
 -v "${HOME}"/.ssh/id_rsa:/root/.ssh/id_rsa \
 -v /tmp/.ansible_temp:/k8spilot/.ansible_temp \
 quay.io/k8spilot/k8spilot:v1.0.4 bash ./pilot deploy mycluster
```

