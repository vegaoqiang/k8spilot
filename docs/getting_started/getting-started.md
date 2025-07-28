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

## 开始安装
一切准备就绪后，可以开始安装Kubernetes集群了
```shell
# 执行以下命令进入交互式配置安装
./pilot deploy
```




