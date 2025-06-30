# k8splaybook
使用ansible playbook快速部署k8s集群

## 快速开始

### Requirements

+ 用于安装k8s集群的虚拟机应该>=3台
+ 确保inventor中的分组名称是：[k8smaster]，[k8snode]，[schedulernode]，[etcd]，这将决定相关服务安装在分组下指定的虚拟机中（主机名可自行修改）
+ [schedulernode]中的节点应该是[k8snode]中排除master后的所有节点
+ etcd必须要>=3个节点，如果资源不充足，etcd可以选择安装在K8snode虚拟机上，如果用于安装k8s集群的虚拟机只有三台，那么etcd其中一个节点需要安装在k8smaster虚拟机上, 如果资源充足，推荐将etcd安装在单独的三台虚拟机中

### 创建ansible inventor
执行脚本将交互式在k8splaybook目录下创建hosts文件
```shell
cd k8splaybook
./install prepare
```

### 安装环境准备

```shell
ansible-playbook --tags common common.yml --ssh-extra-args='-o StrictHostKeyChecking=no' -i ./hosts
```

### 安装etcd集群

```shell
ansible-playbook --tags etcd --skip-tags common,master,node common.yml --ssh-extra-args='-o StrictHostKeyChecking=no' -i ./hosts 
```
安装脚本会自动打印出集群状态，如果没有，需要手动执行以下操作来验证etcd集群是否健康
```shell
export ENDPOINT='--endpoints=10.10.41.138:2379,10.10.41.139:2379,10.10.41.140:2379'
export ETCD_ARGS='--cacert=/usr/local/etcd/ssl/ca.pem --cert=/usr/local/etcd/ssl/etcd.pem --key=/usr/local/etcd/ssl/etcd-key.pem --write-out=table'
etcdctl $ETCD_ARGS member list
etcdctl $ETCD_ARGS endpoint status
etcdctl $ETCD_ARGS endpoint health
etcdctl $ENDPOINT $ETCD_ARGS endpoint status
```


### 安装k8s master

```shell
ansible-playbook --tags master --skip-tags common,node,etcd common.yml --ssh-extra-args='-o StrictHostKeyChecking=no' -i ./hosts
```

### 安装k8s node

```shell
ansible-playbook --tags node --skip-tags common,master,etcd common.yml --ssh-extra-args='-o StrictHostKeyChecking=no' -i ./hosts
```

> node节点安装启动之后需要在master上批发证书
playbook在安装完node节点后会自动执行批准证书操作，如果执行失败，请用如下命令手动执行证书批准操作

```shell
kubectl get csr
kubectl certificate approve [csrName]
```

### 安装中间件和服务

在开始安装中间件和服务前，需要先执行
```shell
./install init_service_version
```
脚本会更新roles/service/templates目录下所有服务的template文件的images为roles/service/files目录下的版本，目的是让k8s安装的服务版本和已经拷贝过去的服务镜像版本保持一致。

然后执行以下脚本开始安装
```shell
ansible-playbook service.yml --skip-tags service_update --ssh-extra-args='-o StrictHostKeyChecking=no' -i ./hosts
```

### 安装Cilium（可选）

在上一步安装中间件和服务器已经包含了安装cilium，如果需要重新安装cilium，可执行

```shell
ansible-playbook --tags cilium cilium.yml --ssh-extra-args='-o StrictHostKeyChecking=no' -i ./hosts
```

### 仅安装中间件（可选）
```shell
ansible-playbook service.yml --tags middware --skip-tags service_update --ssh-extra-args='-o StrictHostKeyChecking=no' -i ./hosts
```

### 仅安装服务（可选）
```shell
ansible-playbook service.yml --tags service --skip-tags service_update --ssh-extra-args='-o StrictHostKeyChecking=no' -i ./hosts
```

### 更新服务
```shell
./install service_update /xxxx/xxxx/服务镜像包路径
```
脚本中会调用ansible-playbook执行更新操作，具体的ansible-playbook指令是：
```shell
ansible-playbook service.yml --tags update_service --skip-tags service --ssh-extra-args='-o StrictHostKeyChecking=no' -i ./hosts
```