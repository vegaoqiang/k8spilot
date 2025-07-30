# 被控端清单
inventory记录了用于安装Kubernetes的主机信息，k8spilot inventory文件位于: [./inventory/inventory.ini](../../inventory/inventory.ini)，k8spilot可交互式配置inventory，如果你的被控端数量很多，交互式配置inventory显得很笨拙，可自行编辑inventory文件，使用任意文本编辑器参考[inventory样例](#inventory样例)进行修改。

## 编辑inventory

编辑inventory需要注意以下事项

**分组**
inventory文件中必须包含 `**control**` `**worker**` `**etcd**`三个分组，分组名称包含在`[]`中

**[control]**: 用于安装Kubernetes Control-Plane的主机放入该分组下，k8spilot现阶段只支持安装单个Control-Plane节点的Kubernetes，所以`[control]`分组下只能有一台主机信息。
**[worker]**: 用于安装Kubernetes Worker节点的主机信息放入该分组下，注意worker节点中应包含安装用于安装Control-Plane的主机信息
**[etcd]** 用于安装etcd集群的主机信息，etcd集群最少需要三个节点

**主机信息**

inventory文件中的每一条主机信息，都包含以下结构

| control01 | ansible_ssh_host=x.x.x.x | ansible_port=22 | ansible_password='xxxx' |
| - | - | - | - |
| 主机名称，并作为Kubernetes节点名称，可自定义 | `ansible_ssh_host `是固定key，x.x.x.x是主机的IP地址 | `ansible_port`是固定key，22是主机的ssh端口，根据实际情况修改 | `ansible_password`是固定key，xxxx是主机的root用户密码，根据实际情况修改，如果主控端通过公私钥方式登录主机，密码可省略。 |

## inventory样例

以下为k8spilot inventory样例

```ini
[control]
control01 ansible_ssh_host=x.x.x.x ansible_port=22 ansible_password='xxxx'
[worker]
control01 ansible_ssh_host=x.x.x.x ansible_port=22 ansible_password='xxxx'
worker01 ansible_ssh_host=x.x.x.x ansible_port=22 ansible_password='xxxx'
worker02 ansible_ssh_host=x.x.x.x ansible_port=22 ansible_password='xxxx'
[etcd]
control01 ansible_ssh_host=x.x.x.x ansible_port=22 ansible_password='xxxx'
worker01 ansible_ssh_host=x.x.x.x ansible_port=22 ansible_password='xxxx'
worker02 ansible_ssh_host=x.x.x.x ansible_port=22 ansible_password='xxxx'
```
