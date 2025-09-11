# cni provider
k8spilot默认安装cilium作为集群的网络插件，同时开启cilium-ingress并设置为集群默认ingressclass。作为替代，可选择calico作为集群的网络插件

## 设置网络插件
通过修改k8spilot配置文件,如：`./inventories/mycluster/group_vars/all.yml`,修改以下内容，让k8spilot安装calico作为集群网络插件

```yml
# calico版本
calico_version: v3.30.2
# 网络插件类型，推荐使用cilium, 可选calico
cni_provider: calico
```

选择cilium为网络插件（已默认）

```yml
# cilium版本
cilium_version: v1.17.6
# 网络插件类型，推荐使用cilium, 可选calico
cni_provider: cilium
```

> cilium和calico网络插件在安装时默认开启eBPF模式，kube-proxy将被忽略安装