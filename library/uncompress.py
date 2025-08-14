# Author: vegaoqiang

from ansible.module_utils.basic import AnsibleModule
import os
import tarfile
import pwd
import grp


def main():
    # 定义模块参数
    module_args = dict(
      src=dict(type='str', required=True),
      dest=dict(type='str', required=True),
      strip_components=dict(type='int', default=0),
      owner=dict(type='str', default=None),
      group=dict(type='str', default=None),
      mode=dict(type='str', default=None),
      include=dict(type='list', elements='str', default=None)
    )

    # 初始化 Ansible 模块
    module = AnsibleModule(
      argument_spec=module_args,
      supports_check_mode=True
    )

    # 获取参数
    src = module.params['src']
    dest = module.params['dest']
    strip_components = module.params['strip_components']
    owner = module.params['owner']
    group = module.params['group']
    mode = module.params['mode']
    include = module.params['include']

    result = dict(
      changed=False,
      files=[],
      msg=""
    )

    # 检查源文件是否存在
    if not os.path.exists(src):
      module.fail_json(msg=f"Source file {src} does not exist")

    # 检查目标目录是否存在，不存在则创建
    if not os.path.exists(dest):
      if not module.check_mode:
        try:
          os.makedirs(dest)
        except Exception as e:
          module.fail_json(msg=f"Failed to create destination directory {dest}: {str(e)}")
      result['changed'] = True

    # 检查是否为 tar.gz 文件
    if not tarfile.is_tarfile(src):
      module.fail_json(msg=f"Source file {src} is not a valid tar.gz file")

    try:
      with tarfile.open(src, 'r:gz') as tar:
        # 获取所有成员
        members = tar.getmembers()
        if include:
          # 如果指定了 include，则过滤成员
          members = [m for m in members if os.path.basename(m.name) in include]

        # 过滤需要解压的成员
        if strip_components > 0:
          def filter_members(member):
            # 分割路径并去掉指定层级
            parts = member.name.split('/')
            if len(parts) <= strip_components:
              return None
            member.name = '/'.join(parts[strip_components:])
            return member
          members = [m for m in members if filter_members(m) is not None]

        # 检查是否需要解压（幂等性）
        files_to_extract = []
        for member in members:
          dest_path = os.path.join(dest, member.name)
          if not os.path.exists(dest_path):
            files_to_extract.append(member)
          else:
            # 简单检查文件是否需要更新（大小或修改时间）
            dest_stat = os.stat(dest_path)
            if dest_stat.st_size != member.size or dest_stat.st_mtime < member.mtime:
              files_to_extract.append(member)

        if files_to_extract:
          result['changed'] = True
          if not module.check_mode:
            tar.extractall(path=dest, members=files_to_extract)
            result['files'] = [m.name for m in files_to_extract]

        # 设置文件权限和所有者
        if (owner or group) and files_to_extract and not module.check_mode:
          for member in files_to_extract:
            dest_path = os.path.join(dest, member.name)
            try:
              if owner:
                uid = pwd.getpwnam(owner).pw_uid
                os.chown(dest_path, uid, -1)
              if group:
                gid = grp.getgrnam(group).gr_gid
                os.chown(dest_path, -1, gid)
              # 设置文件权限
              if mode:
                os.chmod(dest_path, int(mode, 8))
              else:
                # 如果没有指定 mode，则使用成员的原始模式
                os.chmod(dest_path, member.mode)
            except Exception as e:
              module.fail_json(msg=f"Failed to set permissions for {dest_path}: {str(e)}")

    except Exception as e:
      module.fail_json(msg=f"Failed to unarchive {src}: {str(e)}")

    module.exit_json(**result)

if __name__ == '__main__':
  main()