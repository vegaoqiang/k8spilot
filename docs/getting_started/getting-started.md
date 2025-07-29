# 开始

## 安装k8spilot
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
pip3 -r deps/requirments -i https://mirrors.tuna.tsinghua.edu.cn/pypi/web/simple
```

> :warning: 在你的环境中，如果主控端是通过SSH密码登录被控端，主控端需要额外安装sshpass
>```shell
># apt仓库（Debian/Ubuntu系）
>apt install -y sshpass
>
># rpm仓库（Fedore/CentOS系）
>dnf install -y sshpass
>```

## 开始安装Kubernetes
一切准备就绪后，只需执行一下操作，即可开始安装Kubernetes集群了
```shell
# 执行以下命令进入交互式配置安装
./pilot deploy
```



