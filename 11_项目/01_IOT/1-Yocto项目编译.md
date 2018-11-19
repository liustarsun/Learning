#  编译项目
------
## 1. 命令 
### 1.1 首次创建build目录，括号内容sensorgw项目没有用，不用指定
```
xingyanl@yocto:yocto_proj$ DISTRO=fsl-imx-x11 MACHINE=sensorgw-imx6q source fsl-setup-release.sh -b build_X11
```

### 1.2 在不新增目录的情况下登录
```
xingyanl@yocto:yocto_proj$ source setup-environment build_X11/
```

### 1.3 toolchains目录
```
build_dir/tmp/deploy/sdk/MACHINE/
```
### 1.4 内核镜像目录
```
build_dir/tmp/deploy/images/imx6qsabresd
```

### 1.5 内核源码软链接目录
```
xingyanl@yocto:build_1207$  bitbake -e linux-imx  | grep ^S=
S="/home/xingyanl/yocto_proj/build_1207/tmp/work/sensorgw_imx6q-poky-linux-gnueabi/linux-imx/4.9.11-r0/git"
```

### 1.6 包的下载目录
```
xingyanl@yocto-DL580:build_1207$ bitbake -e linux-imx | grep ^SRC_URI=
SRC_URI="git://source.codeaurora.org/external/imx/linux-imx.git;protocol=https;branch=imx_4.9.11_1.0.0_ga file://mach-imx6q.patch             file://defconfig             file://sensorgw.cfg   
```

### 1.7 编译内核--注意为大写-C
```
xingyanl@yocto-DL580:build$ bitbake linux-imx -C compile
....
Initialising tasks: 100% |####################################################################| Time: 0:00:01
NOTE: Executing SetScene Tasks
NOTE: Executing RunQueue Tasks
NOTE: Tasks Summary: Attempted 442 tasks of which 427 didn't need to be rerun and all succeeded.
```

### 1.8 查找包名
```
xingyanl@yocto:build_1207$ bitbake -s | grep linux
linux-imx                                          :4.9.11-r0
.......
```

### 1.9 查看一个包常用命令
```
xingyanl@yocto:build_1207$ bitbake linux-imx -c listtasks
Initialising tasks: 100% |####################################################################| Time: 0:00:00
NOTE: Executing RunQueue Tasks
linux-imx-4.9.11-r0 do_listtasks: do_build                       Default task for a recipe - depends on all other normal tasks required to 'build' a recipe
linux-imx-4.9.11-r0 do_listtasks: do_clean                       Removes all output files for a target
linux-imx-4.9.11-r0 do_listtasks: do_cleanall                    Removes all output files, shared state cache, and downloaded source files for a target
linux-imx-4.9.11-r0 do_listtasks: do_compile                     Compiles the source in the compilation directory
linux-imx-4.9.11-r0 do_listtasks: do_deploy                      Writes deployable output files to the deploy directory
....
NOTE: Tasks Summary: Attempted 1 tasks of which 0 didn't need to be rerun and all succeeded.
```

### 1.10 开启多通道下载
```
xingyanl@yocto:build_1207$ vi conf/local.conf
// 添加如下内容
BB_NUMBER_THREADS = '16'
PARALLEL_MAKE = '-j 16'
```

### 1.11 只下载包，不编译
```
xingyanl@yocto:build_1207$ bitbake fsl-image-qt5//core-image-base/core-image-minimal -c fetchall
```

### 1.12 编译sensor_gw大包
```
xingyanl@yocto-DL580:build_sensorgw$ bitbake sensorgw-image-minimal
```

### 1.13 dd 安装系统到SD卡
```
xingyanl@yocto-DL580: sudo dd if=sensorgw.sdcard of=/dev/sdb1 bs=1M && sync
```

### 1.14 带GUI的包
```
asb@IoT:build$  bitbake fsl-image-validation-imx
```

------
## 2 自定义配置
> 参考[自定义配置](http://www.thelins.se/johan/blog/2014/06/yocto-part-iii-a-custom-meta-layer/)      

- 通过**添加yocto Layer来自定义镜像配置，添加去除组件，修改系统设置等**      
> 以添加一个自定义Layer**test**为例    

### 2.1 自定义layer镜像
- 切换到**sources**目录下，添加**meta-test** layer
```
xingyanl@yocto-DL580:yocto_proj$ cd /home/xingyanl/sensorgw/yocto_proj/sources
xingyanl@yocto-DL580:sources$ yocto-layer create test
Please enter the layer priority you'd like to use for the layer: [default: 6] <------都是直接回车
Would you like to have an example recipe created? (y/n) [default: n] 
Would you like to have an example bbappend file created? (y/n) [default: n] 

New layer created in meta-test.

Don't forget to add it to your BBLAYERS (for details see meta-test/README).

xingyanl@yocto-DL580:sources$ cd meta-test/

xingyanl@yocto-DL580:meta-test$ mkdir -p recipes-test/images

// 以core-image-minimal.bb为模板，给test layer添加一个镜像目标
xingyanl@yocto-DL580:images$ vi test-image.bb 
require recipes-core/images/core-image-minimal.bb
```   
### 2.2 编译test的镜像
- 切换到 build 编译目录下，并修改**conf/bblayers.conf** 文件，按照已有的格式，将**meta-test** layer添加到**BBLAYERS**变量中。
```
xingyanl@yocto-DL580:build$ vi conf/bblayers.conf
BBLAYERS += " ${BSPDIR}/sources/meta-test "
```

// 和命令相关的配置文件
xingyanl@yocto-DL580:sources$ grep "fsl-image-validation-imx" * -nR
meta-fsl-bsp-release/imx/meta-sdk/recipes-fsl/images/fsl-image-qt5-validation-imx.bb:4:require recipes-fsl/images/fsl-image-validation-imx.bb
meta-fsl-bsp-release/imx/meta-sdk/recipes-fsl/images/fsl-image-gui.bb:4:require recipes-fsl/images/fsl-image-validation-imx.bb
meta-fsl-bsp-release/imx/README:74:   fsl-image-validation-imx provides a gui image without QT.


```
// 交叉编译工具
Each time you wish to use the SDK in a new shell session, you need to source the environment setup script e.g.
 $ . /opt/fsl-imx-x11/4.9.11-1.0.0/environment-setup-cortexa9hf-neon-poky-linux-gnueabi

```