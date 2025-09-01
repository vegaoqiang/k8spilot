# 使用k8spilot离线安装和管理Kubernetes
本文档将介绍和演示使用k8spilot的离线安装方式安装一个Kubernetes集群，还可以使用在线方式安装Kubernetes集群，参见: [在线方式安装Kubernetes](getting-started-online.md)

## Requirements
继续阅读该文档前，请查看您的环境是否已经满足离线安装Kubernetes的要求。

+ 控制端不支持Windows，Windows用户可使用docker或者wsl方案替代：[Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install), [k8spilot docker](getting-started-docker.md)
+ 被控端（用于安装`Kubernetes`的服务器）数量应该>=3
+ 所有被控端之间网络互通（通过内网）
+ 控制端能使用`root`账号登录所有被控端
+ 所有被控端均为`Linux`，且内核版本`>=5.4`

## 下载离线资源
请访问[]()，更具自己需要安装的Kubernetes版本，下载对应的离线资源，离线资源下载完成后，请解压离线资源到得到resource目录，将resource目录启动到k8spilot目录下