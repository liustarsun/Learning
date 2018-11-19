### **Git常用指令**

#### **1. 代理相关**
```
// 查看配置  
xingyanl@yocto-DL580:~$ git config -l
user.name=xingyanl
user.email=xingyang.liu@nokia-sbell.com
xingyanl@yocto-DL580:~$

// 配置全局代理
xingyanl@yocto-DL580:~$ git config --global http.proxy 'socks5://135.251.123.122:9900'
xingyanl@yocto-DL580:~$ git config --global https.proxy 'socks5://135.251.123.122:9900'

xingyanl@yocto-DL580:~$ git config --global http.proxy 'http://135.245.48.34:8000/'
xingyanl@yocto-DL580:~$ git config --global https.proxy 'http://135.245.48.34:8000/'

// 取消全局代理配置
xingyanl@yocto-DL580:~$ git config --global --unset http.proxy
xingyanl@yocto-DL580:~$ git config --global --unset https.proxy

// 配置用户名和邮箱
xingyanl@yocto-DL580:~$ git config --global user.email "xingyang.liu@nokia-sbell.com"
xingyanl@yocto-DL580:~$ git config --global user.name "xingyanl"

// 在vscode配置记住密码
xingyanl@yocto-DL580:~$ git config --global credential.helper store 

// 修改git默认编辑器为vim
xingyanl@yocto-DL580:IG_Project$ git config --global core.editor vim 


// 配置git下载通过https代替git，解决SSH协议不能下载的问题
asb@HP8300:build$ git config --global url."https://github.com".insteadOf git://github.com
asb@HP8300:build$ git config --global url."http://git.freescale.com/git/cgit.cgi/imx".insteadOf git://git.freescale.com/imx
asb@HP8300:build$ git config --global url."http://git.freescale.com/git/cgit.cgi/imx/imx-firmware.git".insteadOf git://git.freescale.com/proprietary/imx-firmware.git
asb@HP8300:build$ git config -l
url.https://github.com.insteadof=git://github.com  // 使用https:代替git:


```
#### **2. 创建repository相关**
```
// 查看repository
xingyanl@yocto-DL580:IG_Project$ git remote -v
origin  http://135.251.123.102/xingyanl/IG_Project.git (fetch)
origin  http://135.251.123.102/xingyanl/IG_Project.git (push)

xingyanl@yocto-DL580:gitlab$ git clone http://135.251.123.102/IGP/IG_Project.git
// 本地目录和远程仓库关联
xingyanl@yocto-DL580:gitlab$ git init
xingyanl@yocto-DL580:gitlab$ git remote add origin http://135.251.123.102/IGP/IG_Project.git

// 添加、提交
xingyanl@yocto-DL580:gitlab$ git add .
xingyanl@yocto-DL580:gitlab$ git commit -m ""
xingyanl@yocto-DL580:gitlab$ git push -u origin master(dev...)
```
----
#### **3. 分支相关**
```
// 查看分支, 前面带*号
xingyanl@yocto-DL580:IG_Project$ git branch
* master

// 创建分支，并切换到新的分支
xingyanl@yocto-DL580:IG_Project$ git checkout -b dev
Switched to a new branch 'dev'

// 删除分支
xingyanl@yocto-DL580:IG_Project$ git branch
  dev
* master
xingyanl@yocto-DL580:IG_Project$ git branch -d dev
Deleted branch dev (was 25a6a02).
xingyanl@yocto-DL580:IG_Project$ git branch
* master
xingyanl@yocto-DL580:IG_Project$

// 提交到dev分支
xingyanl@yocto-DL580:IG_Project$ git push -u origin dev
.....
To http://135.251.123.102/xingyanl/IG_Project.git
 * [new branch]      dev -> dev
Branch dev set up to track remote branch dev from origin.

// 切换到主流分支
xingyanl@yocto-DL580:IG_Project$ git checkout master
Switched to branch 'master'
Your branch is up-to-date with 'origin/master'.
xingyanl@yocto-DL580:IG_Project$ git branch
  dev
* master
xingyanl@yocto-DL580:IG_Project$

// 把dev分支merge到master分支上
xingyanl@yocto-DL580:IG_Project$ git merge dev
Updating 51d53f8..25a6a02
Fast-forward
 dev.md | 1 +
 1 file changed, 1 insertion(+)
 create mode 100644 dev.md

// 添加新的origin
xingyanl@yocto-DL580:IG_Project$ git remote add origin http://135.251.123.102/xingyanl/IG_Project.git


```
----
#### **4. 回退**
```
// 回退
xingyanl@yocto-DL580:IG_Project$ git log -p -2
commit 90a8c1c1ba47aaec0c8e5204bd063222c06c1e82
.....
// 回退版本号
commit 25a6a028f33e554051473ffaff94135bc376ae00
.....
xingyanl@yocto-DL580:IG_Project$ git reset --hard 25a6a028f33e554051473ffaff94135bc376ae00

// 查看修改内容
xingyanl@yocto-DL580:IG_Project$ git diff dev.md

// 添加所有更改内容
xingyanl@yocto-DL580:IG_Project$ git add -A

// 取消修改内容(提交前)
xingyanl@yocto-DL580:IG_Project$ git checkout -- dev.md

// 添加git忽略文件.gitignore
xingyanl@yocto-DL580:IG_Project$ vi .gitignore
.gitignore

```
------
### 5. gitbook制作
[gitbook制作](https://www.jianshu.com/p/4824d216ad10)


### 6. 解决git status不认识中文
```
liu:02_Ucore xingyanl$ git config --global core.quotepath false
```
