import sys
import subprocess

REQUIRE_ANSIBLE_VERSION=10.5
REQUIRE_ANSIBLE_CORE_VERSION=2.17

py_major=sys.version_info.major
py_minor=sys.version_info.minor

if py_major != 3:
    print("Currnet Python Version Less Than 3.10 \n")
    sys.exit(1)
if  py_major == 3 and py_minor < 10:
    print("Must Be Install Python Version >=3.10")
    sys.exit(1)


try:
    import ansible
except ModuleNotFoundError as e:
    print(e)
    print("Please use `pip install ansible>=10.5.0`")
    sys.exit(1)

try:
    import yaml
except ModuleNotFoundError as e:
    print(e)
    print("PyYAML module not install, please install it use `pip install PyYAML`")
    sys.exit(1)

try:
    import pip
except ModuleNotFoundError as e:
    print(e)
    print('Use `python3 -m ensurepip` enable it.')
    sys.exit(1)

ansible_core_version = float(ansible.__version__.rsplit('.', 1)[0])
if ansible_core_version < REQUIRE_ANSIBLE_CORE_VERSION:
    print("Current installed ansible-core version is %s less than 2.17.0") % ansible.__version__
    sys.exit(1)

ansible_verison_info = subprocess.run(["pip3", "show", "ansible"], capture_output=True, text=True)
if ansible_verison_info.returncode != 0:
    print('Unknow pip3 command')
    sys.exit(1)

ansible_version_text = ansible_verison_info.stdout.splitlines()[1]
ansible_version = ansible_version_text.split(':')[-1]
if float(ansible_version.rsplit('.', 1)[0]) < REQUIRE_ANSIBLE_VERSION:
    print('Current installed ansible version is %s less than 10.5.0' %ansible_version)
    print("Please install ansible>=10.5.0, use `pip3 install ansible>=10.5.0`")
    sys.exit(1)
