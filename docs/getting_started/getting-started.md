# 开始

## Requirements
运行k8spilot的系统需要满足以下条件 
+ Linux操作系统，Windows不支持（可用wsl）
+ k8spilot的网络与需要被安装kubernetes集群的服务器保持互通
+ Ansible >= 10.5.0 (ansible-core >= 2.17.0)
+ Python >= 3.10
+ sshpass （可选的）如果k8spilot和需要安装kubernetes集群的服务器是通过ssh密码登录，则需要sshpass

安装kubernetes集群的服务器需要满足以下条件  
+ Linux操作系统，内核>=5.4
+ 服务器可使用root用户进行ssh登录
+ 安装kubernetes集群最少需要3台服务器,且各服务器之间网络互通


## 安装Python
`k8spilot`要求`Python`最低版本为`3.10`，如果你的`Python`刚好大于等于`3.10`可跳过该步骤。否则，你需要升级Python版本，参见：[Python安装方法](install-python.md)  

查看Python版本.
```shell
python --version
```

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




