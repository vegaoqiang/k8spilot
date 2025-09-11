# ingress
k8spilot 默认使用cilium网络插件提供的ingress作为默认ingress-controller，如果集群安装的网络插件非cilium，需要自行安装额外的ingress-controller，k8spilot提供安装ingress-nginx作为额外的ingress-controller。

## cilium ingress
当使用cilium ingress为集群默认ingress时，cilium会创建名为cilium-ingress的services，对应的端口如下
+ http:  30080(nodeport) -> 80
+ https: 30443(nodeport) -> 443

可以通过集群任意节点+端口将请求转发到cilium-ingress

## 安装ingress-nginx
通过修改k8spilot配置文件,如：`./inventories/mycluster/group_vars/all.yml`,修改以下内容，让k8spilot安装ingress-nginx作为集群ingress-controller，并设置为默认IngressClass
```yml
# 是否开启ingress
enable_ingress: true
# 选择ingress类型，默认使用cilium, 可选ingress-nginx
# 使用cilium时，cni_plugin必须同时为cilium，否则k8spilot不会安装ingress
ingress_controller: ingress-nginx
# ingress-nginx版本，当ingress_controller为ingress-nginx时生效
ingress_nginx_version: v1.13.0
# ingress入口，将在所有节点上通过nodeport暴露ingress入口
ingress_nodeport_http: 30080
ingress_nodeport_https: 30443
```

## 安装其它ingress controller
k8spilot暂未提供其它ingress controller内置安装，如需要请自行安装