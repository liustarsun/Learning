# 安装docker
> Host为Ubuntu 16.04LTS
------
##  1. 安装流程
### 1.1 删除以前的老版本
```
asb@HP8300:~$ sudo apt-get remove docker docker-engine docker.io
```

### 1.2 添加extra-virtual
```
asb@HP8300:~$ sudo apt-get install linux-image-extra-$(uname -r) linux-image-extra-virtual
```

### 1.3 安装其他软件
```
asb@HP8300:~$ sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
```

### 1.4 添加官方或aliyunPGP秘钥
```
// 官方PGP秘钥
asb@HP8300:~$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -

// 或者添加aliyun的PGP秘钥 
asb@HP8300:~$ curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add

// 验证
asb@HP8300:~$ sudo apt-key fingerprint 0EBFCD88
```

### 1.5 添加官方apt配置或aliyun配置
```
// 官方配置
asb@HP8300:~$ sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) > stable"

// aliyun配置
asb@HP8300:~$ sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"
```

### 1.6 更新软件源
```
asb@HP8300:~$ sudo apt-get update
```

### 1.7 安装docker-ce
```
asb@HP8300:~$ sudo apt-get install docker-ce
```

### 1.8 测试
```
asb@HP8300:~$ docker -v
Docker version 17.12.1-ce, build 7390fc6
```

------
## 2. 配置fabric环境所需
### 2.1 修改为当前用户权限
```
asb@HP8300:~$ sudo usermod -aG docker asb
// 需要重启
asb@HP8300:~$ sudo reboot
```

### 2.2 配置阿里云镜像加速器
```
asb@HP8300:~$ sudo mkdir -p /etc/docker
asb@HP8300:~$ sudo tee /etc/docker/daemon.json <<-'EOF'
{
  "registry-mirrors": ["https://obou6wyb.mirror.aliyuncs.com"]
}
EOF
asb@HP8300:~$ sudo systemctl daemon-reload
asb@HP8300:~$ sudo systemctl restart docker
```

### 2.3 安装Docker-Compose
- Docker-compose是支持通过模板脚本批量创建Docker容器的一个组件
```
asb@HP8300:~$ sudo curl -L https://github.com/docker/compose/releases/download/1.20.0-rc1/docker-compose-`uname -s`-`uname -m` -o /usr/local/bin/docker-compose

asb@HP8300:~$ sudo chmod +x /usr/local/bin/docker-compose
asb@HP8300:/$ docker-compose -v
docker-compose version 1.20.0-rc1, build 86428af
```


------
## 3 配置docker 代理
```
asb@docker:~$ vi /etc/default/docker 
DOCKER_OPTS="--dns 8.8.8.8 --dns 8.8.4.4"

export http_proxy="http://135.245.48.34:8000/"
export https_proxy="https://135.245.48.34:8000/"
```

### Centos中docker代理配置
```
[root@localhost /]# mkdir /etc/systemd/system/docker.service.d
[root@localhost /]# vi /etc/systemd/system/docker.service.d/http-proxy.conf
[Service] 
Environment="HTTP_PROXY=http://135.245.48.34:8000/"
Environment="HTTPS_PROXY=http://135.245.48.34:8000/"
[root@localhost /]# systemctl daemon-reload
[root@localhost /]# systemctl restart docker
[root@localhost /]# docker run hello-world 
Unable to find image 'hello-world:latest' locally
latest: Pulling from library/hello-world
```

