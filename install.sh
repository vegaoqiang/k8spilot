#!/bin/bash

checkConnect(){
  local ADDR=$1
  local PORT=$2

  nc -z ${ADDR} ${PORT}
  if [ $? -ne 0 ]; then
    echo "${ADDR}:${PORT}端口不可连接，请确认"
    exit 1
  fi
}

readMaster(){
  # echo "[k8smaster]" >> $(dirname ${BASH_SOURCE[0]})/hosts
  while true; do
    read -p "输入K8S MASTER节点IP地址: " MASTER_ADDR
    if [ -z "${MASTER_ADDR}" ];then
      echo -e "\e[33mK8S MASTER地址不能为空\e[0m"
    else
      read -p "输入K8S MASTER节点SSH端口[默认22]: " MASTER_SSH_PORT
      if [ -z "${MASTER_SSH_PORT}" ]; then
        local MASTER_SSH_PORT=22
      fi
      while true; do
        read -p "输入K8S MASTER节点root SSH密码: " MASTER_SSH_PASSWD
        if [ -z "$MASTER_SSH_PASSWD" ]; then
          echo -e  "\e[33mK8S MASTER节点root SSH密码不能为空\e[0m"
        else
          break
        fi
      done
      # 在[k8smaster]后插入内容
      sed -i "/\[k8smaster\]/a k8s-master01  ansible_ssh_host=${MASTER_ADDR} ansible_port=${MASTER_SSH_PORT} ansible_password='${MASTER_SSH_PASSWD}'" $(dirname ${BASH_SOURCE[0]})/hosts
      # 在[k8snode]后插入内容
      sed -i "/\[k8snode\]/a k8s-master01  ansible_ssh_host=${MASTER_ADDR} ansible_port=${MASTER_SSH_PORT} ansible_password='${MASTER_SSH_PASSWD}'" $(dirname ${BASH_SOURCE[0]})/hosts
      sed -i "/\[schedulernode\]/a k8s-master01  ansible_ssh_host=${MASTER_ADDR} ansible_port=${MASTER_SSH_PORT} ansible_password='${MASTER_SSH_PASSWD}'" $(dirname ${BASH_SOURCE[0]})/hosts
      sed -i "/\[etcd\]/a k8s-master01  ansible_ssh_host=${MASTER_ADDR} ansible_port=${MASTER_SSH_PORT} ansible_password='${MASTER_SSH_PASSWD}'" $(dirname ${BASH_SOURCE[0]})/hosts
      break
    fi
  done
}

readNode(){
  #echo "[k8snode]" >> $(dirname ${BASH_SOURCE[0]})/hosts
  local count=1
  while true; do
    read -p "输入K8S NODE${count}节点的IP地址:" NODE_ADDR
    if [ -z "${NODE_ADDR}" ]; then
      echo -e  "\e[33mK8S NODE${count}地址不能为空\e[0m"
    else
      read -p "输入K8S NODE${count}节点SSH端口[默认22]: " NODE_SSH_PORT
      if [ -z "${NODE_SSH_PORT}" ]; then
        local NODE_SSH_PORT=22
      fi
      while true; do
        read -p "输入K8S NODE${count}节点root SSH密码: " NODE_SSH_PASSWD
        if [ -z "$NODE_SSH_PASSWD" ]; then
          echo -e  "\e[33mK8S NODE节点root SSH密码不能为空\e[0m"
        else
          break
        fi
      done

      # 在[schedulernode]前插入内容
      sed -i "/\[schedulernode\]/i k8s-node0${count}  ansible_ssh_host=${NODE_ADDR} ansible_port=${NODE_SSH_PORT} ansible_password='${NODE_SSH_PASSWD}'" $(dirname ${BASH_SOURCE[0]})/hosts
      # 在[etcd]前插入内容
      sed -i "/\[etcd\]/i k8s-node0${count}  ansible_ssh_host=${NODE_ADDR} ansible_port=${NODE_SSH_PORT} ansible_password='${NODE_SSH_PASSWD}'" $(dirname ${BASH_SOURCE[0]})/hosts
      # 增加两个node节点到etcd中用于部署etcd集群 
      if [ ${count} -le 2 ]; then
        sed -i "/\[etcd\]/a k8s-node0${count}  ansible_ssh_host=${NODE_ADDR} ansible_port=${NODE_SSH_PORT} ansible_password='${NODE_SSH_PASSWD}'" $(dirname ${BASH_SOURCE[0]})/hosts
      fi
      read -p "是否继续添加K8S NODE节点?默认否[Y/n]" ADD
      if [ "${ADD,,}" != "y" ]; then
        break
      fi
      count=$((count + 1))
    fi
  done
}

prepare_hosts(){
  HOSTS=$(dirname ${BASH_SOURCE[0]})/hosts
  > ${HOSTS}
  echo "[k8smaster]" >> ${HOSTS}
  echo "[k8snode]" >> ${HOSTS}
  echo "[schedulernode]" >> ${HOSTS}
  echo "[etcd]" >> ${HOSTS}
  readMaster
  readNode
  echo "节点配置完成，即将进入安装阶段"
}

install_platform(){
  echo -e "\e[32m=====Start prepare install k8s cluster======\e[0m"
  ansible-playbook --tags common $(dirname ${BASH_SOURCE[0]})/common.yml --ssh-extra-args='-o StrictHostKeyChecking=no' -i $(dirname ${BASH_SOURCE[0]})/hosts
  echo -e "\e[32m=====Start install etcd cluster======\e[0m"
  ansible-playbook --tags etcd --skip-tags common,master,node $(dirname ${BASH_SOURCE[0]})/common.yml --ssh-extra-args='-o StrictHostKeyChecking=no' -i $(dirname ${BASH_SOURCE[0]})/hosts
  echo -e "\e[32m=====Start install k8s master======\e[0m"
  ansible-playbook --tags master --skip-tags common,node,etcd $(dirname ${BASH_SOURCE[0]})/common.yml --ssh-extra-args='-o StrictHostKeyChecking=no' -i $(dirname ${BASH_SOURCE[0]})/hosts
  echo -e "\e[32m=====Start install k8s node======\e[0m"
  ansible-playbook --tags node --skip-tags common,master,etcd $(dirname ${BASH_SOURCE[0]})/common.yml --ssh-extra-args='-o StrictHostKeyChecking=no' -i $(dirname ${BASH_SOURCE[0]})/hosts
  echo -e "\e[32m=====Start install services======\e[0m"
  ansible-playbook $(dirname ${BASH_SOURCE[0]})/service.yml --ssh-extra-args='-o StrictHostKeyChecking=no' -i $(dirname ${BASH_SOURCE[0]})/hosts
}

help(){
  echo "Usage:"
  echo -e "  bash install.sh [OPTION]\n"
  echo -e "OPTIONS:\n"
  echo -e "  install:"
  echo -e "  一键执行所有操作，包含配置用于安装K8S集群的主机信息，安装K8S集群，中间件服务，业务服务\n"
  echo -e "  prepare:"
  echo -e "  仅配置用于安装K8S集群的主机信息\n"
  echo -e "  service_update:"
  echo -e "  更新服务，必须指定更新的服务镜像目录或镜像文件：./install.sh service_update xx/xx/镜像目录or文件"
  echo -e "  init_service_version:"
  echo -e "  初始化服务的版本，修改roles/service/vars/main.yaml文件中的对应服务的镜像版本，使之同roles/service/files/{arch}下的镜像保持一致"
  echo -e "  platform:"
  echo -e "  仅装K8S集群，中间件服务，业务服务\n"
}

IMAGE_INFO=()
image_info(){
  local MANIFEST=$(tar -axf $1 manifest.json -O)
  local CONFIG=$(echo ${MANIFEST}|sed -n 's/.*"Config":"\([^"]*\)".*/\1/p')
  local REPOTAGS=$(echo ${MANIFEST}|sed -n 's/.*"RepoTags":\["\([^"]*\)".*/\1/p')
  local PROJECT_NAME=$(echo ${REPOTAGS##*/}|awk -F: '{print $1}')
  local CONFIG_DETAILS=$(tar -axf $1 ${CONFIG} -O)
  local IMAGE_ARCH=$(echo ${CONFIG_DETAILS}|sed -n 's/.*"architecture":"\([^"]*\)".*/\1/p')
  IMAGE_INFO[0]="${PROJECT_NAME}"
  IMAGE_INFO[1]="${REPOTAGS}"
  IMAGE_INFO[2]="${IMAGE_ARCH}"
  #echo "${PROJECT_NAME} ${REPOTAGS} ${IMAGE_ARCH}"
}

service_update(){
  if [ -z $1 ];then
    echo "必须指定镜像或者镜像目录，并且使用绝对路径"
    exit 1
  fi
  if [ ! -e $1 ];then
    echo "${1}不存在"
    exit 1
  fi
  local IMAGE_LIST=()
  local COUNT=1
  local IMAGE_TYPE="$1" # $类型，如果是文件，则直接传递给ansible，如果是目录，则需要在末尾加上/
  if [ ! -d $1 ];then
    image_info $1
    echo -e "\e[32m${COUNT}. 服务名称：${IMAGE_INFO[0]}, 仓库地址：${IMAGE_INFO[1]}, 镜像架构：${IMAGE_INFO[2]}\e[0m"
    IMAGE_LIST+=(${IMAGE_INFO[1]})
  else
    for image in `ls $1/*.tar`;do
      image_info $image
      echo -e "\e[32m${COUNT}. 服务名称：${IMAGE_INFO[0]}, 仓库地址：${IMAGE_INFO[1]}, 镜像架构：${IMAGE_INFO[2]}\e[0m"
      IMAGE_LIST+=(${IMAGE_INFO[1]})
      ((COUNT+=1))
    done
    if [[ "$1" != *"/" ]];then
      IMAGE_TYPE="$1/"
    fi
  fi
  read -p "是否确认更新以上服务?[Y/N]: " CONFIRM
  if [ "${CONFIRM,,}" != "y" ];then
    exit 0
  fi
  local IMAGE_YML=()
  for repo in ${IMAGE_LIST[@]};do
    local PROJECT_NAME=$(echo ${repo##*/}|awk -F: '{print $1}')
    local VAR_NAME="${PROJECT_NAME//-/_}"
    IMAGE_YML+=("${PROJECT_NAME}.yaml")
    # 替换ansible role中的变量
    sed -i "s#${VAR_NAME}:.*#${VAR_NAME}: ${repo}#" roles/service/vars/main.yml
  done
  local var_service_yaml=$(printf '%s' "$(IFS=','; echo "${IMAGE_YML[*]}")")

  # 将镜像传递给ansible-playbook
  ansible-playbook service.yml --tags service_update --skip-tags service --ssh-extra-args='-o StrictHostKeyChecking=no' -e "var_image=${IMAGE_TYPE}" -e "var_service_yaml=${var_service_yaml}" -i hosts
}

# 通过读取镜像信息，更新service role var中的服务镜像变量
init_service_version(){
  local COUNT=1
  for image in `ls roles/service/files/$(arch)/*.tar`;do
    image_info $image
    echo -e "\e[32m${COUNT}. 服务名称：${IMAGE_INFO[0]}, 仓库地址：${IMAGE_INFO[1]}, 镜像架构：${IMAGE_INFO[2]}\e[0m"
    local PROJECT_NAME="${IMAGE_INFO[0]}"
    local VAR_NAME="${PROJECT_NAME//-/_}"
    sed -i "s#${VAR_NAME}:.*#${VAR_NAME}: ${IMAGE_INFO[1]}#" roles/service/vars/main.yml
    ((COUNT+=1))
  done
}

case $1 in
  install)
  prepare_hosts
  install_platform
  ;;
  prepare)
  prepare_hosts
  ;;
  platform)
  install_platform
  ;;
  service_update)
  service_update "$2"
  ;;
  init_service_version)
  init_service_version
  ;;
  -h)
  # 帮助
  help
  ;;
  *)
  # 帮助
  help
  ;;
esac