# 安装Python

## 包管理器安装
以下在各个Linux发行版中使用包管理器安装python3.11，你也可以自由的更换版本为python3.12或者python3.13

🐧 Ubuntu / Debian 系列 (apt)
```shell
sudo apt update
sudo apt install -y python3.11
```

🐧 RHEL / CentOS / AlmaLinux / Rocky Linux（dnf / yum）
```shell
sudo dnf install -y python3.11
```

🐧 openSUSE / SUSE Linux Enterprise（zypper）
```shell
sudo zypper install python3.11
```
## 编译安装
如果你的操作系统版本比较老旧，使用包管理器无法安装>=3.10的python，可下载Python源码进行编译安装。[点击进入Python官网下载](https://www.python.org/downloads/)


开始编译前需要安装必要的依赖：
```shell
sudo dnf install -y \
  gcc \
  gcc-c++ \
  make \
  zlib-devel \
  bzip2-devel \
  openssl-devel \
  ncurses-devel \
  sqlite-devel \
  readline-devel \
  tk-devel \
  libuuid-devel \
  libffi-devel \
  xz-devel \
  wget \
  git \
  gdbm-devel \
  lzma-sdk-devel \
  libnsl2-devel
```

依赖作用说明：  
| 依赖 | 用途 |
| - | - |
|gcc, make | 基础编译工具
|zlib-devel, bzip2-devel, xz-devel |支持 .zip, .bz2, .xz 解压模块
|openssl-devel | 支持 ssl、https
|readline-devel, ncurses-devel | 支持交互式 shell 和编辑功能
|sqlite-devel | 支持 sqlite3 模块
|tk-devel | 支持 tkinter 图形界面
|libuuid-devel | 支持 uuid 模块
|libffi-devel | 支持 ctypes 模块



**开始编译：**
```shell
# 下载源码包
wget https://www.python.org/ftp/python/3.11.13/Python-3.11.13.tar.xz
tar -xf Python-3.11.13.tar.xz
cd Python-3.11.13

# 编译并安装
./configure --enable-optimizations
make -j$(nproc)
make install

# 验证安装
python3 --version
```