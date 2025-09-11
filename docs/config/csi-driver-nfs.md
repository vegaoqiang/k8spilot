# csi driver nfs
k8spilot默认不会安装csi-driver-nfs,如果你有需求，可通过以下方法开启安装并设置为集群默认的storageclass

通过修改k8spilot配置文件,如：`./inventories/mycluster/group_vars/all.yml`,修改以下内容，让k8spilot安装csi-driver-nfs作为集群存储插件
```yml
# 是否安装nfs网络存储
enable_csi_nfs: false
csi_nfs_version: v4.11.0
# 指定nfs服务端的地址, 指定的nfs服务端必须支持NFSv4
custom_nfs_server_address: 
# 如果没有指定自定义nfs-server地址，将在集群中自动安装nfs-server
# 安装nfs-server服务时，指定nfs-server在主机上的存储位置，请指定大容量磁盘目录，默认nfs数据存放在/var/lib/nfs-data
nfs_host_path: /var/lib/nfs-data
# 指定nfs-server容器运行在哪个节点上，默认调度到主节点上, 推荐在主节点上将nfs_host_path目录单独挂载磁盘
nfs_server_host: control
```