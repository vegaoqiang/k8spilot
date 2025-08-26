# Author: vegaoqiang
# Date: 20250715 

import os
import sys
import configparser
import yaml


def validation_inventory(config_path) -> None:
  if not os.path.isfile(config_path):
    print("033[33inventory file: %s not exist!\033[0m" %config_path)
    sys.exit(1)
  parser = configparser.ConfigParser()
  parser.read(config_path)
  if not parser.has_section('control'): 
    print("\033[33minventory file has no section [control]\033[0m")
    sys.exit(1)
  if not parser.has_section('worker'):
    print("\033[33minventory file has no section [worker]\033[0m")
    sys.exit(1)
  if not parser.has_section('etcd'):
    print("\033[33minventory file has no section [etcd]\033[0m")
    sys.exit(1)
  if len(parser['control']) != 1:
    print("\033[33m[control] section must be configured 1 hosts to install the cluster control\033[0m")
    sys.exit(1)
  if len(parser['worker']) < 3:
    print("\033[33m[worker] section must be configured with more than 3 hosts to install the cluster\033[0m")
    sys.exit(1)
  if len(parser['etcd']) < 3:
    print("\033[33m[etcd] section must be configured with more than 3 hosts to install the cluster\033[0m")
    sys.exit(1)


def get_hostname_prefix() -> tuple:
  yaml_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'inventories', env, 'group_vars', 'all.yml')
  with open(yaml_path, 'r', encoding='utf-8') as f:
    data = yaml.safe_load(f)
  return data.get('control_hostname_prefix', 'control'), data.get('worker_hostname_prefix', 'worker')
  

def get_host_profile(hostname_prefix: str, hostname_suffix: int) -> str:
  suffix = hostname_suffix
  if hostname_suffix < 10:
    suffix = '0' + str(hostname_suffix)
  ipaddress = input("\033[36m请输入{hostname_prefix}{suffix}的IP地址:\033[0m".format(hostname_prefix=hostname_prefix, suffix=suffix))
  if not ipaddress:
    return ''
  sshport = input("\033[36m请输入{0}的ssh端口 [默认: 22]:\033[0m".format(ipaddress)) or '22'
  sshpass = input("\033[36m请输入{0}的root登录密码 [免密登录请回车跳过]:\033[0m".format(ipaddress))
  return '{hostname_prefix}{suffix} ansible_ssh_host={ipaddress} ansible_port={sshport} ansible_password=\'{sshpass}\''.format(
    hostname_prefix=hostname_prefix,
    suffix=suffix,
    ipaddress=ipaddress,
    sshport=sshport,
    sshpass=sshpass
  )

def profile_inventory() -> tuple:
  control_hostname_prefix, worker_hostname_prefix = get_hostname_prefix()
  print("\033[32m请根据提示录入用于安装集群的主机信息，录入完成后请按: Ctrl + C 退出录入\033[0m")
  try:
    control_profile = get_host_profile(hostname_prefix=control_hostname_prefix, hostname_suffix=1)
  except KeyboardInterrupt:
    print("\033[32m录入终止\033[0m")
    sys.exit(1)
  if not control_profile:
    print("\033[31m必须配置控制节点[master]信息才能正常安装集群\033[0m")
    sys.exit(1)
  worker_suffix = 1
  worker_profile_bucket = []
  while True:
    try:
      worker_profile = get_host_profile(hostname_prefix=worker_hostname_prefix, hostname_suffix=worker_suffix)
      if worker_profile:
        worker_profile_bucket.append(worker_profile)
        worker_suffix += 1
    except KeyboardInterrupt:
      if len(worker_profile_bucket) < 2:
        print("\033[31mworker[node]节点数量必须大于等于2才能正常安装集群\033[0m")
        sys.exit(1)
      print("\033[32m录入终止\033[0m")
      break
  return control_profile, worker_profile_bucket


def generate_inventory(control_profile: str, worker_profile: list):
  with open(inventory_path, 'w', encoding='utf-8') as f:
    f.write('[control]\n')
    f.write(control_profile + '\n')
    f.write('[worker]\n')
    f.write(control_profile + '\n')
    f.write('\n'.join(worker_profile) + '\n')
    f.write('[etcd]\n')
    f.write(control_profile + '\n')
    f.write('\n'.join(worker_profile[:2]) + '\n')



if __name__ == '__main__':
  if len(sys.argv) != 3:
    print("Usage: python inventory_checker.py [validation|generate] mycluster_name")
    sys.exit(1)
  if sys.argv[1] not in ['validation', 'generate']:
    print("Invalid command: %s, must be one of [validation|generate]" % sys.argv[1])
    sys.exit(1)
  inventory_name = 'hosts'
  env = sys.argv[2]
  inventory_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir, 'inventories', env, inventory_name)

  if sys.argv[1] == 'validation':
    validation_inventory(config_path=inventory_path)
  if sys.argv[1] == 'generate':
    control_profile, worker_profile = profile_inventory()
    generate_inventory(control_profile=control_profile, worker_profile=worker_profile)