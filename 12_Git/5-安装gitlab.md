

### 查看hostname
```
asb@docker:~$ cat /etc/hostname 
docker
```

### 安装gitlab
```
asb@docker:~$ docker search gitlab
// 下载
asb@docker:~$ docker pull gitlab/gitlab-ce

// 启动
asb@docker:~$ sudo docker run --detach \
    --hostname gitlab \
    --publish 443:443 --publish 80:80 --publish 13456:22 \
    --name 'gitlab001' \
    --restart always \
    --volume /opt/gitlab/config:/etc/gitlab \
    --volume /opt/gitlab/logs:/var/log/gitlab \
    --volume /opt/gitlab/data:/var/opt/gitlab \
    gitlab/gitlab-ce:latest

sudo docker run --detach \
--hostname gitlab.example.com \
--publish 443:443 --publish 80:80 --publish 22:22 \
--name gitlab \
--restart always \
--volume /srv/gitlab/config:/etc/gitlab \
--volume /srv/gitlab/logs:/var/log/gitlab \
--volume /srv/gitlab/data:/var/opt/gitlab \
gitlab/gitlab-ce:latest



asb@docker:~$ sudo docker ps

asb@docker:~$ docker exec -it 8d0dd95de15f /bin/bash
root@docker:~$ vi /etc/gitlab/gitlab.rb
// 修改如下内容，外面可以访问的IP地址
external_url 'http://10.66.7.24'

root@docker:~$ gitlab-ctl reconfigure

// 默认的用户名是root 密码是：asb#1234
```


### 项目地址
```
[root@cnkp vicia]# git remote 命令

http://135.252.5.237/CNKP/VICIA
http://135.252.5.237/CNKP/tahoe_16t16r
http://135.252.5.237/CNKP/gen364tr

```


### 查看当前shell
```
asb@docker:~$ cat /etc/shells 
# /etc/shells: valid login shells
/bin/sh
/bin/dash
/bin/bash
/bin/rbash

// 添加用户
[root@cnkp /]# adduser xingyanl
[root@cnkp /]# passwd xingyanl
Changing password for user xingyanl.
New password: 
BAD PASSWORD: The password fails the dictionary check - it is too simplistic/systematic
Retype new password: 
passwd: all authentication tokens updated successfully.
[root@cnkp /]# 

```