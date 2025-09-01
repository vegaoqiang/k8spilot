# 安装k8spilot

以下步骤演示将k8spilot下载安装到系统中, 如果使用k8spilot docker镜像请跳到[Docker方式使用k8spilot](#docker方式使用k8spilot)

## 下载k8spilot

```shell
tag=v1.0.4
wget https://github.com/vegaoqiang/k8spilot/archive/refs/tags/${tag}.tar.gz
tar -xf ${tag}.tar.gz
cd k8spilot-${tag##*v}
```

## 安装依赖
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

至此，k8spilot已经安装到本地，如何使用k8spilot安装和管理Kubernetes，参见：[使用k8spilot](getting-started.md)