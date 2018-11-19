# 安装ubuntu14.04
> F10键进入BIOS模式，把UEFI模式禁止掉, 开启CPU虚拟化支持; 安装系统，删除多余应用程序
> U盘启动是F9

------
## 1. 配置IP地址，重启电脑或者网卡

```
asb@IoT:~$  sudo vi /etc/network/interfaces
# interfaces(5) file used by ifup(8) and ifdown(8)
auto lo
iface lo inet loopback

auto eth0
iface eth0 inet static
address 135.252.5.239
netmask 255.255.255.0
gateway 135.252.5.1

dns-nameservers 135.252.5.1
(dns-nameservers 8.8.4.4)
(dns-nameservers 8.8.8.8)
asb@IoT:~$

// 修改dns文件
asb@IoT:~$ sudo vi /etc/resolvconf/resolv.conf.d/base

```

------
## 2. 安装代理和相关软件

### 2.1 安装proxychains4，添加文件proxychains.conf
```
strict_chain
proxy_dns
remote_dns_subnet 224
tcp_read_time_out 15000
tcp_connect_time_out 8000
[ProxyList]
socks5  135.251.123.122 9900
```

### 2.2 安装openssh-server
```
asb@HP8300:~$ proxyc apt-get install openssh-server
```

### 2.3 安装vim
```
asb@HP8300:~$ proxyc apt-get install vim
```

### 2.4 安装gcc/g++ 32位库
```
root@d9ffaad30ba7:~/c++# apt-get install gcc-multilib g++-multilib

```

#### 2.4.1 配置vim
```
// vim的配置文件
root@36637a20099f:~/C# cat ~/.vimrc 
set nocompatible
set encoding=utf-8
set fileencodings=utf-8,chinese
set tabstop=4
set cindent shiftwidth=4
set backspace=indent,eol,start
autocmd Filetype c set omnifunc=ccomplete#Complete
autocmd Filetype cpp set omnifunc=cppcomplete#Complete
set incsearch
set number
set display=lastline
set ignorecase
syntax on
set nobackup
set ruler
set showcmd
set smartindent
set hlsearch
set cmdheight=1
set laststatus=2
set shortmess=atI
set formatoptions=tcrqn
set autoindent
``` 

### 2.5 安装配置VNC
```
asb@HP8300:~$ sudo apt-get install x11vnc
asb@HP8300:~$ x11vnc -storepasswd
// 启动VNCserver
asb@HP8300:~$ x11vnc -forever -shared -rfbauth ~/.vnc/passwd

// 配置随系统启动在后台启动
asb@HP8300:~$ sudo cp ~/.vnc/passwd /etc/x11vnc.pass
asb@HP8300:~$ sudo vi /etc/init/x11vnc.conf
start on login-session-start
script
    x11vnc -display :0 -auth /var/run/lightdm/root/:0 -forever -bg -o /var/log/x11vnc.log -rfbauth /etc/x11vnc.pass -rfbport 5900
end script

// 让capslock键起作用添加一个参数

```

### 2.6 安装pip3
```
xingyanl@xy:~$ sudo apt install python3-pip
```

### 2.7 安装配置shadowsocks
```
xingyanl@xy:~$ sudo pip3 install shadowsocks
Downloading/unpacking shadowsocks
  Downloading shadowsocks-2.8.2.tar.gz
  Running setup.py (path:/tmp/pip_build_root/shadowsocks/setup.py) egg_info for package shadowsocks

Installing collected packages: shadowsocks
  Running setup.py install for shadowsocks

    Installing sslocal script to /usr/local/bin
    Installing ssserver script to /usr/local/bin
Successfully installed shadowsocks
Cleaning up...
xingyanl@xy:~$ vi shadowsocks.json
{
"server": "45.76.207.182",
"server_port": 9900,
"local_port": 1080,
"password": "Qwe*90op",
"timeout": 600,
"method": "chacha20"
}

// 启动shadowsocks
xingyanl@xy:~$ sudo sslocal -c ~/shadowsocks.json -d start
INFO: loading config from /home/xingyanl/shadowsocks.json
2017-12-29 07:47:00 INFO     loading libsodium from libsodium.so.23
started
xingyanl@xy:~$
```

### 2.8 安装proxychains
```
xingyanl@xy:~$ sudo apt install proxychains
// 修改配置文件
xingyanl@xy:~$ sudo vi /etc/proxychains.conf
socks5  127.0.0.1 1080

```

#### 2.8.1 测试安装结果
```
// 成功
xingyanl@xy:~$ sudo proxychains curl www.google.com
ProxyChains-3.1 (http://proxychains.sf.net)
|DNS-request| www.google.com
|S-chain|-<>-127.0.0.1:1080-<><>-4.2.2.2:53-<><>-OK
|DNS-response| www.google.com is 64.233.189.99
|S-chain|-<>-127.0.0.1:1080-<><>-64.233.189.99:80-<><>-OK
<HTML><HEAD><meta http-equiv="content-type" content="text/html;charset=utf-8">
<TITLE>302 Moved</TITLE></HEAD><BODY>
<H1>302 Moved</H1>
The document has moved
<A HREF="http://www.google.co.jp/?gfe_rd=cr&amp;dcr=0&amp;ei=eoNFWuTGOJOF2QSKg6QY">here</A>.
</BODY></HTML>
xingyanl@xy:~$
```

### 2.9 python版本更换
> 前提是/usr/bin要在PATH的最前面
```
// 查看版本
asb@IoT:fsl-release-bsp$ update-alternatives --list python 
/home/asb/anaconda3/bin/python
/usr/bin/python2.7
/usr/bin/python3.4
asb@IoT:fsl-release-bsp$ 

// 添加1：python2.7
asb@IoT:fsl-release-bsp$ sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7  1

// 添加2：python3.4
asb@IoT:fsl-release-bsp$ sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.4 2 

// 添加3: anaconda3 python
asb@IoT:~$ sudo update-alternatives --install /usr/bin/python python /home/asb/anaconda3/bin/python 3

// 更换为2.7
asb@IoT:fsl-release-bsp$ sudo update-alternatives --config python
There are 3 choices for the alternative python (providing /usr/bin/python).

  Selection    Path                            Priority   Status
------------------------------------------------------------
* 0            /home/asb/anaconda3/bin/python   3         auto mode
  1            /home/asb/anaconda3/bin/python   3         manual mode
  2            /usr/bin/python2.7               1         manual mode
  3            /usr/bin/python3.4               2         manual mode

Press enter to keep the current choice[*], or type selection number: 2
update-alternatives: using /usr/bin/python2.7 to provide /usr/bin/python (python) in manual mode
asb@IoT:fsl-release-bsp$ 

// 删除某个版本
asb@IoT:fsl-release-bsp$ sudo update-alternatives --remove python /usr/bin/python2.7 
update-alternatives: removing manually selected alternative - switching python to auto mode
update-alternatives: using /home/asb/anaconda3/bin/python to provide /usr/bin/python (python) in auto mode
asb@IoT:fsl-release-bsp$ 

asb@IoT:fsl-release-bsp$ sudo update-alternatives --remove python /usr/bin/python3.4
update-alternatives: removing manually selected alternative - switching python to auto mode
update-alternatives: using /home/asb/anaconda3/bin/python to provide /usr/bin/python (python) in auto mode

asb@IoT:fsl-release-bsp$ sudo update-alternatives --remove python /home/asb/anaconda3/bin/python

```

### 2.10 安装virtualbox
```
asb@docker:~$ sudo vi /etc/apt/sources.list
# add the virtualbox source 
deb http://download.virtualbox.org/virtualbox/debian vivid contrib

// 添加oracle public key for apt-secure
asb@docker:~$ wget -q https://www.virtualbox.org/download/oracle_vbox.asc -O- | sudo apt-key add -
OK

// install virtualbox
asb@docker:~$ sudo apt-get update
asb@docker:~$ sudo apt-get install virtualbox-5.0
``` 
------
## 3. 更新源文件
```
asb@HP8300:~$ sudo vi /etc/apt/sources.list

deb http://mirrors.aliyun.com/ubuntu/ trusty main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-security main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-updates main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ trusty-backports main restricted universe multiverse

asb@HP8300:~$ sudo proxychains4 apt-get update
asb@HP8300:~$ sudo proxychains4 apt-get upgrade
```

------
### 3.1 配置网卡
```
asb@HP8300:~$ sudo /etc/init.d/networking restart
asb@HP8300:~$ sudo ifconfig eth1 down
asb@HP8300:~$ sudo ifconfig eth1 up
asb@HP8300:~$ sudo ifdown eth0
asb@HP8300:~$ sudo ifup eth0
```

### 3.2 添加别名
```
xingyanl@xy:~$ vi .bashrc
alias proxyc='sudo proxychains'
alias gcc='gcc -Wall'
xingyanl@xy:~$ source .bashrc
```

### 3.3 关闭networkmanager
```
// 1. 停止服务
asb@docker:network$ sudo /etc/init.d/network-manager stop
Stopping network-manager (via systemctl): network-manager.service.
asb@docker:network$ 

// 2. 删除.state文件(我是修改文件，把true改成了false)
asb@docker:NetworkManager$ vi /var/lib/NetworkManager/NetworkManager.state
[main]
NetworkingEnabled=false
WirelessEnabled=false
WWANEnabled=false

// 3. false改成true
asb@docker:NetworkManager$ sudo vi /etc/NetworkManager/NetworkManager.conf
[ifupdown]
managed=true
```
### 3.4 ubuntu16.04的aliyun的源:
```
deb http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse  
deb http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse  
deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse  
deb http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse  

deb http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse  

deb-src http://mirrors.aliyun.com/ubuntu/ xenial main restricted universe multiverse  
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main restricted universe multiverse  
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main restricted universe multiverse  
deb-src http://mirrors.aliyun.com/ubuntu/ xenial-backports main restricted universe multiverse  

deb-src http://mirrors.aliyun.com/ubuntu/ xenial-proposed main restricted universe multiverse  

deb http://archive.canonical.com/ubuntu/ xenial partner  

```

### 3.5 ubuntu16.04的官方源
```
deb http://archive.ubuntu.com/ubuntu/ xenial main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ xenial-security main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ xenial-updates main restricted universe multiverse
deb http://archive.ubuntu.com/ubuntu/ xenial-backports main restricted universe multiverse

deb http://archive.ubuntu.com/ubuntu/ xenial-proposed main restricted universe multiverse

deb-src http://archive.ubuntu.com/ubuntu/ xenial main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ xenial-security main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ xenial-updates main restricted universe multiverse
deb-src http://archive.ubuntu.com/ubuntu/ xenial-backports main restricted universe multiverse

deb-src http://archive.ubuntu.com/ubuntu/ xenial-proposed main restricted universe multiverse


deb http://archive.canonical.com/ubuntu/ xenial partner
deb http://extras.ubuntu.com/ubuntu/ xenial main

```

### 3.6 升级ubuntu14.04到16.04(不推荐升级，可能会出很多问题)
```
asb@HP8300:apt$ sudo proxychains4 apt-get update
asb@HP8300:apt$ sudo proxychains4 apt-get dist-upgrade
asb@HP8300:apt$ sudo proxychains4 update-manager -d

```

### 3.7 安装ifconfig和IP命令
```
root@66f06921c2e0:~# apt-get install net-tools
root@66f06921c2e0:~# apt-get install iputils-ping
root@66f06921c2e0:~# apt-get install iproute2
```
### 3.8 配置代理
```
http_proxy=http://135.245.48.34:8000/
https_proxy=http://135.245.48.34:8000/
ftp_proxy=http://135.245.48.34:8000/
export http_proxy
export https_proxy
export ftp_proxy
```