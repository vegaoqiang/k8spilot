# 开始

## 安装k8spilot
以下步骤演示将k8spilot下载安装到系统中, 如果使用k8spilot docker镜像请跳过

### 下载k8spilot

```shell
version=v1.0
wget https://github.com/vegaoqiang/k8spilot/releases/${version}.tar.gz
tar xf ${version}.tar.gz
cd ${version}
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
>```shell
># apt仓库（Debian/Ubuntu系）
>apt install -y sshpass
>
># rpm仓库（Fedore/REHL系）
>dnf install -y sshpass
>```

## 使用k8spilot Docker镜像
:todo:

## 开始安装Kubernetes
如果你已经准备好了用于安装Kubernetes的虚拟机，只需执行以下操作，即可开始安装Kubernetes集群了
```shell
# 执行以下命令进入交互式配置安装
./pilot deploy
```


