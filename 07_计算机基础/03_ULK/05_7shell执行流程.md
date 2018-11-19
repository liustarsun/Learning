# 基础
------
## 1. init进程
/sbin/init：linux系统默认启动的第一个程序，负责进行Linux系统的一些初始化工作

## 2. getty进程
/bin/getty：getty程序用execve系统调用执行了/bin/login程序
> getty程序在自己的主进程里面执行执行了/bin/login，这样/bin/login**将把getty的进程空间替换掉**      

## 3. login进程
/bin/login：检查/etc/passwd文件       

### 登陆流程    
```
// passwd文件包含了用户名、密码和该用户的登陆shell
// 密码和用户名匹配用户的登陆，登陆shell则作为用户登陆后的命令行程序
root@36637a20099f:/# cat /etc/passwd | grep root
root:x:0:0:root:/root:/bin/bash   // x说明密码被保存在另外一个文件里头/etc/shadow

// 密码是被加密的
root@36637a20099f:/# cat /etc/shadow | grep root
root:*:17554:0:99999:7:::

// 追踪流程， 安装strace工具
root@36637a20099f:/# apt-get install strace

// 追踪内核
root@36637a20099f:~# strace -f -o strace.out /bin/login  ===> 追踪内核启动的流程

注释：/bin/login程序用execve调用了/bin/bash命令，/bin/login在子进程里面用execve调用了/bin/bash，因为在启动/bin/bash后，可以看到/bin/login并没有退出

// trace打印
3882 4829  execve("/bin/bash", ["-bash"], [/* 18 vars */]) = 0
```

## 4. bash进程
/bin/bash：执行当前用户所有设置的shell环境             
```
// 打印当前shell
root@36637a20099f:/# echo $SHELL
/bin/bash

// $$是个特殊的环境变量，它存放了当前进程ID
root@36637a20099f:/# echo $$ 
161

root@36637a20099f:/# ps -C bash
  PID TTY          TIME CMD
  161 pts/2    00:00:00 bash
```