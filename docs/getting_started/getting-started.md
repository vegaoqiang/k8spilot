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

如果你已经准备好了用于安装Kubernetes的虚拟机，只需执行以下操作，即可开始安装Kubernetes集群了
```shell
./pilot deploy
```

`pilot deploy`将开始交互式录入被控端信息，包含IP地址、ssh端口、ssh密码，录入完成后安装 `Ctrl + C` 结束录入，并开始安装Kubernetes
![example](/docs/images/getting-started.gif)

如果被控端实例数量庞大，交互式手动输入容易出错且效率低下，此时可以手动构建被控端清单，见: [被控端清单](inventory.md)

##  Docker方式使用k8spilot
```shell
touch $(pwd)/inventory.ini
sudo docker run --rm -it -v $(pwd)/inventory.ini:/k8spilot/inventory/inventory.ini -v "${HOME}"/.ssh/id_rsa:/root/.ssh/id_rsa -v /tmp/.ansible_temp:/k8spilot/.ansible_temp quay.io/k8spilot/k8spilot:v1.0.3 bash ./pilot deploy
```
