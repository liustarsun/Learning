### 1. 安装USB转串口的驱动
USB转串口线定义：
红色---5V
黑色---GND
白色---RXD
绿色---TXD

### 2.1 备份源设备树文件
```
// source环境
xingyanl@yocto-DL580:build_1207$ source setup-environment build_1207/
// /tmp/work/sensorgw_imx6q-poky-linux-gnueabi/u-boot-imx/2017.03-r0/git：uboot目录
xingyanl@yocto-DL580:git$ cd board/freescale/mx6sabresd/
// arch/arm/dts:dts目录，备份dts文件
xingyanl@yocto-DL580:dts$ ls -lrt imx6q-sabresd.dts
-rw-r--r-- 1 xingyanl xingyanl 915 Dec  7 15:27 imx6q-sabresd.dts
```

#### 2.2 制作设备树patch文件
```
// 制作patch文件
xingyanl@yocto-DL580:dts$ cp imx6q-sabresd.dts.xingyanl imx6q-sabresd.dts
xingyanl@yocto-DL580:dts$ git diff imx6q-sabresd.dts > imx6q-sabresddts.patch
xingyanl@yocto-DL580:dts$ vi imx6q-sabresddts.patch
mx6qsabresd_defconfig_fpga.patch
+CONFIG_FPGA_ALTERA=y
+CONFIG_FPGA_CYCLON2=y
```

#### 2.3 打patch文件
```
xingyanl@yocto-DL580:build_1207$ bitbake u-boot
```
#### 2.4 反汇编dtb文件
```
asb@IoT:dts$ dtc -I dtb -O dts imx6q-sabresd.dtb > temp.dts  
asb@IoT:dts$ vi temp.dts
asb@IoT:dts$
```

### 3. 网卡相关
已经修改了

### 4. 启动模式管脚配置，以及FPGA相关的配置文件
需要根据原理图把每个模式都测试出来
```
BOOT_MODE0
BOOT_MODE1
启动模式：
BOOT_MODE[1:0]：
00 boot from fuses
01 serial downloader
10 internal boot
```


```
// BOOT_CFG4
BOOT_CFG4[2:0]: 000-ECSPI-1; 001-ECSPI-2; 010-ECSPI-3; 011-ECSPI-4; 100-ECSPI-5; 110-I2C-1; 110-I2C-2; 111-I2C-3
BOOT_CFG4[3]: 0-2B(16bit) 1=3B(24bit)
BOOT_CFG4[5:4]: 00-ECSPIX_SS0; 01-ECSPIX_SS1; 10-ECSPIX_SS2; 11-ECSPIX_SS3;
BOOT_CFG4[6]: 0-Disable EEPROM RECOVERY; 1- ENABLE EEPROM RECOVERY
// BOOT_CFG1
BOOT_CFG1[7:4]: 0011-I2C/SPI BOOT

// BOOT_CFG2
BOOT_CFG2[4:3]: 01-SD2 BOOT; 10-SD3 BOOT; 11-SD4 BOOT
BOOT_CFG2[7:5]: 000-1BIT; 001-4BIT; 010-8BIT; 101-4BIT DDR MMC; 110-8BIT DDR MMC
BOOT_CFG1[0]: 0-Through the SD pad; 1-Direct
BOOT_CFG1[1]:
 MMC: 0-emmc reset disalbed; 1-emmc reset enabled via the sd rst pad(on USDHC3 and USDHC4 only)
SD: 0-No power cycle; 1-Power cycle enabled via the SD RST pad(on USDHC3 and USDHC4 only)
BOOT_CFG1[3:2]
MMC: 0-high-speed mode; 1-Normal-speed mode
SD: 00-Normal(SDR12); 01-High(SDR25); 10-SDR50; 11-SDR104
BOOT_CFG1[4]: 0-Normal boot; 1-Fast boot为例
BOOT_CFG1[5]: 0-SD/ESD/SDXC; 1-MMC/EMMC
BOOT_CFG1[7:6]: 01-Boot from the USDHC interface
```



FPGA设置开关已经打开，然后下载需要明天试试
### 5. linux patch文件制作
已经完成

### 6. 使用yocto项目进行编译
已经结束

#### 6.1 编译环境
+ **DL580 Server账号：**

```
ServerIP: 135.251.123.102
Account: xingyanl
PWD: asb#1234
```

#### 6.2 编译方式
#### 6.2.1 拷贝/home/hsun006/yocot_proj下的downloads，nsb-setupenv.sh ，setup-environment，sources到自己的目录下


```
// 生成build目录和相关文件
xingyanl@yocto-DL580:build$ source nsb-setupenv.sh -b build
```

#### 6.2.2 编译生成的image在build/tmp/deploy/image下

```
xingyanl@yocto-DL580:build$ bitbake meta-toolchain        
xingyanl@yocto-DL580:build$ bitbake sensorgw-image-minimal
```

#### 6.2.3 修改代码：以u-boot为例
```
// 源文件目录
xingyanl@yocto-DL580:yocto_proj$ cd build_1207/tmp/work/sensorgw_imx6q-poky-linux-gnueabi/u-boot-imx/2017.03-r0/git
// 修改文件
xingyanl@yocto-DL580:kernel$ vi common.h
// 生成patch
xingyanl@yocto-DL580:kernel$ git diff common.h > common.patch
```

#### 6.2.4 打patch
```
// 把patch放到如下目录
xingyanl@yocto-DL580:linux-imx$ cd /home/xingyanl/yocto_proj/sources/meta-nsb/recipes-bsp/u-boot/u-boot-imx

// 修改bbappend文件
xingyanl@yocto-DL580:linux$ cd  /home/xingyanl/yocto_proj/sources/meta-nsb/recipes-bsp/u-boot
xingyanl@yocto-DL580:u-boot$ ls
u-boot-imx  u-boot-imx_2017.03.bbappend

// 更新
xingyanl@yocto-DL580:u-boot$ cat u-boot-imx_2017.03.bbappend
....
FILESEXTRAPATHS_prepend := "${THISDIR}/${PN}:"
SRC_URI += "file://mx6_common_h.patch \
           file://mx6sabresd.patch \
           file://mx6sabre_common_h.patch \
           file://fec_mxc.patch \
           file://phy.patch \
           file://mx6qsabresd_defconfig.patch  \
           file://common.patch\  // 添加
"
```

> 如果要修改kernel编译选项， 可以直接自己在linux-imx下新建一个.cfg文件， 里边定义好需要的def选项， 并在SRC_URI里加上这个文件， 可参照usb_serial.cfg





------
## 5. watchdog的操作
```
// watchdog的功能, dts管脚

// CPU_WD_EN
MX6QDL_PAD_EIM_D20__GPIO3_IO20	0x1b0b0
IOMUXC_SW_MUX_CTL_PAD_EIM_DATA20  20E_00A0h

===============================================

// CPU_WDI
MX6QDL_PAD_EIM_D23__GPIO3_IO23	0x1b0b0

// 1. 读功能
IOMUXC_SW_MUX_CTL_PAD_EIM_DATA23 20E_00ACh
值为0x00000005

// 2. 读方向
GPIO direction register (GPIOx_GDIR)  20A_4004
值为0x00480000 因为23位是0，所以是input

// 3. 做成output
关掉狗
#define pwTCON 0x7E004000       @WTCON寄存器
disable_watchdog: 
        ldr r0, =pwTCON         @把地址装载到R0
        mov r1, #0x0            @置0,关闭看门狗
        str r1,[r0]     
        mov pc,lr

```
## 6. 移植过程中PMIC电源管理模块的注释
[去掉PMIC电源管理模块](http://blog.csdn.net/haly321/article/details/70244527)