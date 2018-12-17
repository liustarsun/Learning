### **调试工具**

#### **1. JLINK, JTAG, OPENOCD**  
**JLINK**一款调试ARM CPU的调试设备，**JTAG**和**SWD**是该设备调试CPU的两种工作方式  
**JTAG**是ARM的一种**调试接口协议**；**JLINK**实现由集成开发环境中RDI接口到JTAG协议的转换(**由JLINK内部硬件电路完成**)，它针对ARM设计成**小型USB到JTAG转换盒**
**OpenOCD**是一个调试工具，配合JTAG调试协议，可以对硬件设备进行指令集级别和寄存器级别的调试

#### **2. JLINK简介**


#### **3. JTAG简介**



#### **4. OPENOCD简介**
**TAP的概念**：TAP是一个调试链，通常一个芯片就是一个TAP，但是一个芯片可能会包含多个IP核，因此通常这个chain会包含多个可调试对象；使用**scan_chain**命令显示的信息可以看出所有的可调试对象   


**scan_chain：查看有几个供调试的chain**

#### **5. eclipse调试arm流程**
[调试流程，国外](http://fatalfeel.blogspot.jp/2015/12/openocd-with-eclipse-debug-kernel-of.html)


#### **6. DDR3 stress tool使用**
[DDR3 stress tool使用链接](http://www.imx6rex.com/software/how-to-run-ddr3-calibration-on-imx6/)

下载：
```
============================================
        DDR Stress Test (2.6.0)
        Build: Aug  1 2017, 17:33:25
        NXP Semiconductors.
============================================

============================================
        Chip ID
CHIP ID = i.MX6 Dual/Quad (0x63)
Internal Revision = TO1.5
============================================

============================================
        Boot Configuration
SRC_SBMR1(0x020d8004) = 0x00003840
SRC_SBMR2(0x020d801c) = 0x0a000001
============================================

ARM Clock set to 1GHz

============================================
        DDR configuration
BOOT_CFG3[5-4]: 0x00, Single DDR channel.
DDR type is DDR3
Data width: 64, bank num: 8
Row size: 15, col size: 10
Chip select CSD0 is used
Density per chip select: 2048MB
============================================
```

Calibration：主要是更新这个几个属性，在/board/freescale/mx6sabresd/mx6q_4x_mt41j128.cfg文件中，找到对应的属性
```
保存在log\ is saved
Read DQS Gating calibration
 MPDGCTRL0 PHY0 (0x021b083c) = 0x43240334
 MPDGCTRL1 PHY0 (0x021b0840) = 0x0324031C
 MPDGCTRL0 PHY1 (0x021b483c) = 0x4328033C
 MPDGCTRL1 PHY1 (0x021b4840) = 0x0324026C

 Read calibration
 MPRDDLCTL PHY0 (0x021b0848) = 0x40303638
 MPRDDLCTL PHY1 (0x021b4848) = 0x38363244

 Write calibration
 MPWRDLCTL PHY0 (0x021b0850) = 0x36383C3C
 MPWRDLCTL PHY1 (0x021b4850) = 0x42344C40
```

迅为的板子区别在第6位，为1的话，则是EMMC，为0的话是USB OTG
#### **7. GDB调试流程**
##### **7.1 把u-boot load到内存**

##### **7.2 加载符号表**

##### **7.3 打断点**

##### **7.4 run命令，然后会停在断点处**







### 1. 安装驱动


### 2. 安装keil DS-MDK



Test Access Ports (TAPs) are the core of JTAG.
JTAG使用
https://forum.sparkfun.com/viewtopic.php?f=18&t=40680&p=180635&hilit=imx6+uboot#p180635
For loading u-boot using JTAG, follow the below steps--
1. Download DDR stress test tool v.2.52 from NXP website.
2. Boot your board into serial mode, by turning all boot switches off
3. Now connect USB cable from USB OTG port to desktop/Laptop on which you will be running DDR stress test tool.
4. For information on using DDR stress test tool refer to documentation.
5. Once board is detected in DDR stress test tool, use appropriate inc script in the tool and click on download. After successful downloading of script , DDR will be initialised.
6. Now connect JTAG cable , and load u-boot.bin image using load_image command from JTAG to appropriate address, for imx6q sabresd board it is 0x17800000.
7. Once image is downloaded successfully, you can resume from same address using resume command like
resume 0x178000000

For custom boards, you can use xls provided by NXP to generate inc file for custom board which can be used for loading into DDR stress test tool to initalise DDR.
I am using Arm olimex JTAG debugger for debugging.



---------
---------
[整理来自](http://fatalfeel.blogspot.jp/2015/12/openocd-with-eclipse-debug-kernel-of.html)

## **OpenOCD + Eclipse + Jtag debug on Uboot & Linux**
> openocd从官网下载，或者下载patch版本

### **1. 给官方openocd打补丁**
**编译安装带补丁的openocd**

### **2. 更新openocd中关于imx6的配置文件**
```
because add 2 events in our imx6d-1gb.cfg
$_TARGETNAME configure -event reset-assert
$_TARGETNAME configure -event reset-end

please compare mx6d1G_4x_mt41j128.cfg with imx6d-512mb-oocd-0.8.0.cfg
mx6d1G_4x_mt41j128.cfg at /root/project_board/free_imx/myandroid/bootable/bootloader/uboot-imx/board/freescale/imx/ddr
imx6d-512mb-oocd-0.8.0.cfg at http://www.voipac.com/downloads/imx/jtag

replace correct define on clock, ddr, cache, "set" address and "mww phys" write value in imx6d-512mb-oocd-0.8.0.cfg
save to /opt/openocd/share/openocd/scripts/target/imx6d-1gb.cfg

```


### **3. 给u-boot打patch**
```
// 修改uboot-imx/Kconfig 文件
// config CC_OPTIMIZE_FOR_SIZE
[default y] to  [default n]

// 修改uboot-imx/Makefile 文件
[KBUILD_CFLAGS    += -O2] to
[KBUILD_CFLAGS    += -O0 -g -fno-omit-frame-pointer -fno-optimize-sibling-calls]

// 避免无穷调用堆栈 修改uboot-imx/arch/arm/lib/crt0.S中的ENTRY(_main)
[sub    sp, sp, #GD_SIZE] to  [subs    sp, sp, #GD_SIZE]

// 修改uboot-imx/arch/arm/lib/cache-cp15.c
static void cache_disable(uint32_t cache_bit)
{
...
if (cache_bit == (CR_C | CR_M))
    {
        flush_dcache_all();
        /* issue begin */
//mark here
/*
        set_cr(reg & ~CR_C);
        flush_dcache_all();
*/
    }
...
}

// 修改成usb upload模式
Hardware Switch Boot Mode1 to Boot Mode0

```

### **4. 使用openocd调试**
```
// 执行openocd, cfg文件
openocd -f /opt/openocd/share/openocd/scripts/target/imx6d-1gb.cfg

// 登陆到交叉编译出来的toolchains
asb@ubuntu:~$ gnugdb
(gdb)target remote 127.0.0.1:3333
(gdb)monitor reset halt
(gdb)symbol-file /root/project_board/free_imx/out/matrix_io/uboot/u-boot  //must before load
(gdb)load /root/project_board/free_imx/out/matrix_io/uboot/u-boot
(gdb)break relocate_code
(gdb)continue
Breakpoint 1, relocate_code ()
    at /root/project_board/free_imx/myandroid/bootable/bootloader/uboot-imx/arch/arm/lib/relocate.S:25
        subs    r4, r0, r1        /* r0 <- relocation addr */

```

### **5. 重定位后调试u-boot**
```
// uboot命令行地址
=> bdinfo
.....
relocaddr   = 0x4FF49000   // this value for add-symbol-file of arm-eabi-gdb
.....

// 在uboot启动过程中，执行
~# openocd -f /opt/openocd/share/openocd/scripts/interface/ftdi/dp_busblaster.cfg -f /opt/openocd/share/openocd/scripts/target/imx6.cfg

// 执行gdb
~#gdb
(gdb)target remote localhost:3333
(gdb)add-symbol-file /root/project_board/free_imx/out/matrix_io/uboot/u-boot 0x4FF49000
(gdb)monitor reg
(gdb)cont (then press ctrl+c)
(gdb)bt
//////////////will show follows
#0  0x12000000 in ?? ()
#1  0x4ff704c8 in serial_getc ()
    at /root/project_board/free_imx/myandroid/bootable/bootloader/uboot-imx/drivers/serial/serial.c:413
#2  0x00000000 in ?? ()

// 重定位地址
4ff704c8 - 3DF49000(reloc off) = 120274C8
/*check  /root/project_board/free_imx/out/matrix_io/uboot/u-boot.map
            .text.serial_getc
                0x00000000120274b8       0x14 drivers/serial/built-in.o
                0x00000000120274b8                serial_getc

                .text.serial_tstc
                0x00000000120274cc       0x14 drivers/serial/built-in.o
                0x00000000120274cc                serial_tstc              

confirm 120274b8  < [120274C8] < 120274cc the address is correct
openocd uboot debug is ok~~*/

```

### **6. 调试内核**
1. //default config************************
gedit /root/project_board/free_imx/myandroid/kernel_imx/arch/arm/configs/mx6dq_matrix_android_defconfig
//enableCONFIG_DEBUG_INFO=y
CONFIG_FTRACE=y
CONFIG_FUNCTION_TRACER=y

note:
CONFIG_FTRACE & CONFIG_FUNCTION_TRACER will enable CONFIG_FRAME_POINTER
[config FRAME_POINTER] in ~/myandroid/kernel_imx/arch/arm/Kconfig.debug  


2. ************************
gedit /root/project_board/free_imx/myandroid/device/fsl/matrix_io/init.matrix_io.rc
on init
    #start watchdogd   -->mark here

#service watchdogd /sbin/watchdogd 10 20 5   -->mark here
#    class core
#    seclabel u:r:watchdogd:s0

3. //linux kernel************************
gedit /root/project_board/free_imx/myandroid/kernel_imx/Makefile
KBUILD_CFLAGS    += -O2
to
KBUILD_CFLAGS    += -O1 -g

if set -O0 or compile error, refer to
http://fatalfeel.blogspot.tw/2013/09/kgdb-eclipse-debug-kernel-on-imx6.html

4. ************************debug linux drivers. (select any directory which you want to debug)
gedit /root/project_board/free_imx/myandroid/kernel_imx/drivers/Makefile
//first line add
KBUILD_CFLAGS    += -O0 -g

//rebuild

5. ************************remove breakpoint and watchpoint reset action
gedit /root/project_board/free_imx/myandroid/kernel_imx/arch/arm/kernel/hw_breakpoint.c
//in functon reset_ctrl_regs(void *unused)
//mark this section
/*
for (i = 0; i < raw_num_brps; ++i) {
    write_wb_reg(ARM_BASE_BCR + i, 0UL);
    write_wb_reg(ARM_BASE_BVR + i, 0UL);
}
for (i = 0; i < core_num_wrps; ++i) {
    write_wb_reg(ARM_BASE_WCR + i, 0UL);
    write_wb_reg(ARM_BASE_WVR + i, 0UL);
}
*/

//in function static u8 get_max_wp_len(void)
//mark this section
/*
write_wb_reg(ARM_BASE_WVR, 0);
write_wb_reg(ARM_BASE_WCR, ctrl_reg);
*/

6. ************************remove low power clock
arm clock need always enable for jtag have 2 ways, select one.
(a.)way
gedit /root/project_board/free_imx/myandroid/kernel_imx/arch/arm/mach-imx/pm-imx6.c
val |= 0x1 << BP_CLPCR_LPM;
val |= BM_CLPCR_ARM_CLK_DIS_ON_LPM;
to
/*val |= 0x1 << BP_CLPCR_LPM;
val |= BM_CLPCR_ARM_CLK_DIS_ON_LPM;*/

(b.)way
gedit /root/project_board/free_imx/myandroid/kernel_imx/arch/arm/configs/mx6dq_android_defconfig
CONFIG_CPU_IDLE=y
to
#CONFIG_CPU_IDLE=y

I select way (a.)

7.  ************************
gedit /root/project_board/free_imx/myandroid/kernel_imx/arch/arm/kernel/entry-armv.S
//find .macro    svc_entry, stack_hole=0
sub        sp, sp, #(S_FRAME_SIZE + \stack_hole - 4)
//change to
subs    sp, sp, #(S_FRAME_SIZE + \stack_hole - 4)

8. ************************disable jtag alarm for Android 6.0
gedit /root/project_board/free_imx/myandroid/kernel_imx/drivers/crypto/caam/secvio.c
//find
static int snvs_secvio_probe(struct platform_device *pdev)

#if defined(CONFIG_JTAG_DEBUG)
    wr_reg32(&svpriv->svregs->hp.secvio_intcfg, HP_SECVIO_INTEN_SRC4 | HP_SECVIO_INTEN_SRC0);
#else
    wr_reg32(&svpriv->svregs->hp.secvio_intcfg, HP_SECVIO_INTEN_SRC4 | HP_SECVIO_INTEN_SRC2 | HP_SECVIO_INTEN_SRC1 | HP_SECVIO_INTEN_SRC0);
#endif

9. ************************fixed for some device node can not stop on breakpoint
gedit /mnt/projects/marsh_mnt/myandroid/kernel_imx/drivers/base/devtmpfs.c
int __init devtmpfs_init(void)
{
...
...
/*kthread_run on myandroid/kernel_imx/include/linux/kthread.h*/
#if defined(CONFIG_JTAG_DEBUG)
    thread = kthread_create(devtmpfsd, &err, "kdevtmpfs");

    if (!IS_ERR(thread))
    {
        thread->wake_cpu = 0;
        wake_up_process(thread);
    }
#else
    thread = kthread_run(devtmpfsd, &err, "kdevtmpfs");
#endif
...
...
    printk(KERN_INFO "devtmpfs: initialized\n");
    return 0;
}

10. ************************pass compile -O0 for Android 6.0
gedit /root/project_board/free_imx/myandroid/kernel_imx/kernel/seccomp.c
static inline void seccomp_sync_threads(void)
{
...
...
#if defined(CONFIG_JTAG_DEBUG)
        smp_mb(); //pass compiletime_assert_atomic_type on -O0
        ACCESS_ONCE(thread->seccomp.filter) =  caller->seccomp.filter;
#else
        smp_store_release(&thread->seccomp.filter, caller->seccomp.filter);
#endif
...
...
}

11. ************************Stop Android layer for speed up debugging(option item)
gedit /root/project_board/free_imx/myandroid/device/fsl/matrix/etc/init.rc
disable healthd zygote media surfaceflinger drm
service servicemanager /system/bin/servicemanager
    class core
    user system
    group system
    critical
    #onrestart restart healthd
    #onrestart restart zygote
    #onrestart restart media
    #onrestart restart surfaceflinger
    #onrestart restart drm
…
…
…
...
#service surfaceflinger /system/bin/surfaceflinger
#    class main
#    user system
#    group graphics drmrpc
#    onrestart restart zygote

#service zygote /system/bin/app_process -Xzygote /system/bin --zygote --start-system-server
#    class main
#    socket zygote stream 660 root system
#    onrestart write /sys/android_power/request_state wake
#    onrestart write /sys/power/state on
#    onrestart restart media
#    onrestart restart netd

#service drm /system/bin/drmserver
#    class main
#    user drm
#    group drm system inet drmrpc

#service media /system/bin/mediaserver
#    class main
#    user media
#    group audio camera inet net_bt net_bt_admin net_bw_acct drmrpc
#    ioprio rt 4

#service bootanim /system/bin/bootanimation
#    class main
#    user graphics
#    group graphics
#    disabled
#    oneshot
…
…
…
…
…
on  property:sys.boot_completed=1
start config_eth0
remove other services after “start config_eth0”

12. ************************kernel start operation at  [0.000000] Booting Linux on physical CPU 0x0
open new terminal type follows
~# /root/project_board/free_imx/myandroid/prebuilts/gcc/linux-x86/arm/arm-eabi-4.6/bin/arm-eabi-gdb
(gdb)target remote localhost:3333
(gdb)symbol-file /root/project_board/free_imx/out/matrix_io/kernel/vmlinux
(gdb)cont
(then press ctrl+c)

//show follows
Program received signal SIGINT, Interrupt.
0x8025c548 in kernel_map_pages (page=0x822bef44, numpages=1, enable=1)
    at /root/project_board/free_imx/myandroid/kernel_imx/mm/debug-pagealloc.c:99
            unpoison_pages(page, numpages);


### **7. eclipse图形化调试**
////////////Openocd eclipse GUI
////////////u-boot GUI debug
#### 1.install eclipse kepler
http://www.eclipse.org/downloads/packages/release/Kepler/SR2
Eclipse Standard 4.3.2 -> linux 64bits
install eclipse-standard-kepler-SR2-linux-gtk-x86_64.tar.gz
extract to /opt/eclipse
chmod 755 -R /opt/eclipse

gedit /opt/eclipse.ini
-XX:PermSize=64m
-XX:MaxPermSize=256m
-Xms128m
-Xmx4096m

Here is full install step:
http://fatalfeel.blogspot.tw/2013/09/eclipse-setting-for-ubuntu-imx6-android.html

#### 2.
Help -> install new software...
work with: http://gnuarmeclipse.sourceforge.net/updates
//check
GNU ARM C/C++ OpenOCD Debugging

#### 3.
right click project
Debug As -> Debug Configurations -> GDB Hardware Debugging
double click to create new name
c/c++ application: /root/project_board/free_imx/out/matrix_io/uboot/u-boot
click bottom line Select other... -> GDB(DSF) Hardware Debugging Launcher
check [disable auto build]

#### 4.
click Debugger tab
GDB Command: /root/project_board/free_imx/myandroid/prebuilts/gcc/linux-x86/arm/arm-eabi-4.6/bin/arm-eabi-gdb
check [Use Remote Target]
Jtag device: GUN ARM OPENOCD
Host name or ip address:localhost
port number:3333

#### 5.
click startup tab
uncheck the all items on startup page
add those lines under [Halt] Box
monitor reset halt
symbol-file /root/project_board/free_imx/out/matrix_io/uboot/u-boot //must before load
load /root/project_board/free_imx/out/matrix_io/uboot/u-boot

#### 6. //Load code and boot-up
because add 2 events in our imx6d-1gb.cfg
$_TARGETNAME configure -event reset-assert
$_TARGETNAME configure -event reset-end

please compare mx6d1G_4x_mt41j128.cfg with imx6d-512mb-oocd-0.8.0.cfg
mx6d1G_4x_mt41j128.cfg at /root/project_board/free_imx/myandroid/bootable/bootloader/uboot-imx/board/freescale/imx/ddr
imx6d-512mb-oocd-0.8.0.cfg at http://www.voipac.com/downloads/imx/jtag

replace correct define on clock, ddr, cache, "set" address and "mww phys" write value in imx6d-512mb-oocd-0.8.0.cfg
save to /opt/openocd/share/openocd/scripts/target/imx6d-1gb.cfg

#### 7. Change to usb upload
Hardware Switch Boot Mode1 to Boot Mode0

#### 8. open new terminal
openocd -f /opt/openocd/share/openocd/scripts/target/imx6d-1gb.cfg

#### 9.
click eclipse [Debug] button
//done

### ////////second debug, after u-boot relocate code address///////
#### 1.
click startup tab
uncheck all the items on startup page
add this line under [Halt] Box
add-symbol-file /root/project_board/free_imx/out/matrix_io/uboot/u-boot 0x4FF04000
rember 0x4FF04000 is from u-boot start operation and input [bdinfo] will show you

#### 2.
After u-boot relocate code address,  open new terminal type follows
~# openocd -f /opt/openocd/share/openocd/scripts/target/imx6d-1gb.cfg
or
~# openocd -f /opt/openocd/share/openocd/scripts/interface/ftdi/dp_busblaster.cfg -f /opt/openocd/share/openocd/scripts/target/imx6.cfg

#### 3.
after into u-boot start operation click eclipse [Debug] button
//done

### Kernel GUI debug/////////
#### 1.
right click project
Debug As -> Debug Configurations -> GDB Hardware Debugging
double click to create new name
C/C++ application: /root/project_board/free_imx/out/matrix_io/kernel/vmlinux
click bottom line Select other... -> GDB(DSF) Hardware Debugging Launcher
check [disable auto build]

#### 2.
click startup tab
uncheck all items on startup page
two ways choice, I use way (a.)

(a.)//target remote localhost:3333 first then load symbol-file
add this line under [Halt] checkbox
symbol-file /root/project_board/free_imx/out/matrix_io/kernel/vmlinux

(b.) //load symbol-file first then target remote localhost:3333
check [Load symbols], Use project binary:

#### 3.
After u-boot relocate code address, open new terminal type follows
~# openocd -f /opt/openocd/share/openocd/scripts/target/imx6d-1gb.cfg
or
~# openocd -f /opt/openocd/share/openocd/scripts/interface/ftdi/dp_busblaster.cfg -f /opt/openocd/share/openocd/scripts/target/imx6.cfg

#### 4.
click eclipse debug
click debug continue

#### 5.
in target console u-boot start operation
==> boot
then enter Starting kernel ...

#### 6.
when Starting kernel operation at [0.000000] Booting Linux on physical CPU 0x0
click eclipse suspend button quickly

#### 7.
set breakpoint
click continue
//done

### How debug module .ko
insmod /mytest/hellotest.ko
When cat /sys/module/hellotest/sections/.text = 0x00000000
Try one of these ways
#### 1.
(a.)
gedit /root/project_board/free_imx/myandroid/kernel_imx/kernel/module.c
//in function module_sect_show
return sprintf(buf, "0x%pK\n", (void *)sattr->address);
//change to
return sprintf(buf, "0x%p\n", (void *)sattr->address);

(b.)
geidt ~/myandroid/device/fsl/matrix/etc/init.rc
write /proc/sys/kernel/kptr_restrict 2
//change to
write /proc/sys/kernel/kptr_restrict 0

I select (b.)

#### 2.
root@matrix_io:/ # insmod /data/hellomod/hellotest.ko
[   76.104855] Hello, world
root@matrix_io:/ # cat /sys/module/hellotest/sections/.text
0x7f11c000  //-->get this addr

#### 3.
in eclipse right click your project
Debug As -> Debug Configurations -> GDB Hardware Debugging
click [Startup tab]
uncheck the all items on startup page
add those lines under [Halt] box but do not check [Halt]
add-symbol-file /root/project_board/free_imx/out/matrix_io/uboot/u-boot 0x7f11c000
then click [Apply]

### Hardware shared lib debugging
#### 1. Get target load address
cat /proc/*/maps | grep gralloc_viv.imx6.so
ad920000-ad924000 r-xp 00000000 103:02 722       /system/lib/hw/gralloc_viv.imx6.so

#### 2. Get shared lib .text address
/mnt/projects/lollipop_mnt/myandroid/prebuilts/gcc/linux-x86/arm/arm-eabi-4.6/bin/arm-eabi-readelf -S /mnt/projects/lollipop_mnt/out/matrix_io/android/target/product/matrix_io/system/lib/hw/gralloc_viv.imx6.so
Section Headers:
  [Nr] Name              Type            Addr     Off    Size   ES Flg Lk Inf Al
  [ 8] .text             PROGBITS        000013d8 0013d8 001988 00  AX  0   0  8

0xad920000 + 0x000013d8 = 0xad921d38

#### 3. Set to arm-eabi-gdb
click Startup tab
uncheck the all items on startup page
add those lines under [Halt] box but do not check [Halt]
add-symbol-file /mnt/projects/lollipop_mnt/out/matrix_io/android/target/product/matrix_io/system/lib/hw/gralloc_viv.imx6.so 0xad9213d8
apply to debug

#### 4. Set breakpoint in a function
/mnt/projects/lollipop_mnt/myandroid/prebuilts/gcc/linux-x86/arm/arm-eabi-4.6/bin/arm-eabi-readelf -s /mnt/projects/lollipop_mnt/out/matrix_io/android/target/product/matrix_io/system/lib/hw/gralloc_viv.imx6.so
28: 00001af1   456 FUNC    GLOBAL DEFAULT    8 _Z25gralloc_alloc_framebu

gralloc_alloc_frame = 0x00001af1 - 0x1 = 0x00001af0 (aligned 4 address in arm cortex)

set break point at target
0xad920000 + 0x00001af0 = 0xad921af0

### watchpoint patch
#### 1.
gedit /root/openocd-0.9.0/src/target/cortex_a.h
//berfore struct cortex_a_common
//add new
struct cortex_a_wrp
{
    int used;
    uint32_t value;
    uint32_t control;
    uint8_t WRPn;
};

//in struct cortex_a_common
//after struct cortex_a_brp *brp_list;
//add new
int wrp_num;
int wrp_num_available;
struct cortex_a_wrp* wrp_list;

#### 2.
gedit /root/openocd-0.9.0/src/target/cortex_a.c
//after function cortex_a_remove_breakpoint
//add functions
static int cortex_a_set_watchpoint(struct target *target, struct watchpoint *watchpoint)
{
    int retval;
    int wrp_i = 0;
    uint32_t    control;
    uint8_t        access_mode;
    uint8_t        byte_addr_select = 0x0F;
    struct cortex_a_common*    cortex_a    = target_to_cortex_a(target);
    struct armv7a_common*        armv7a    = &cortex_a->armv7a_common;
    struct cortex_a_wrp*            wrp_list    = cortex_a->wrp_list;

    if (watchpoint->set)
    {
        LOG_WARNING("breakpoint already set");
        return ERROR_OK;
    }

    while (wrp_list[wrp_i].used && (wrp_i < cortex_a->wrp_num))
        wrp_i++;

    if (wrp_i >= cortex_a->wrp_num)
    {
        LOG_ERROR("ERROR Can not find free Watchpoint Register Pair");
        return ERROR_TARGET_RESOURCE_NOT_AVAILABLE;
    }

    watchpoint->set = wrp_i + 1;

    if (watchpoint->length == 2)
        byte_addr_select = (3 << (watchpoint->address & 0x02));

    access_mode = watchpoint->rw+1;
    control = (byte_addr_select << 5) | (access_mode << 3) | (3 << 1) | 1;
    wrp_list[wrp_i].used = 1;
    wrp_list[wrp_i].value = (watchpoint->address & 0xFFFFFFFC);
    wrp_list[wrp_i].control = control;

    retval = cortex_a_dap_write_memap_register_u32(target,
                                                                                    armv7a->debug_base + CPUDBG_WVR_BASE + 4 * wrp_list[wrp_i].WRPn,
                                                                                    wrp_list[wrp_i].value);
    if (retval != ERROR_OK)
        return retval;

    retval = cortex_a_dap_write_memap_register_u32(target,
                                                                                    armv7a->debug_base + CPUDBG_WCR_BASE + 4 * wrp_list[wrp_i].WRPn,
                                                                                    wrp_list[wrp_i].control);

    if (retval != ERROR_OK)
        return retval;

    return ERROR_OK;
}

static int cortex_a_unset_watchpoint(struct target *target, struct watchpoint *watchpoint)
{
    int retval;
    int wrp_i;
    struct cortex_a_common *cortex_a = target_to_cortex_a(target);
    struct armv7a_common *armv7a = &cortex_a->armv7a_common;
    struct cortex_a_wrp *wrp_list = cortex_a->wrp_list;

    if (!watchpoint->set)
    {
        LOG_WARNING("watchpoint not set");
        return ERROR_OK;
    }

    wrp_i = watchpoint->set - 1;

    if ((wrp_i < 0) || (wrp_i >= cortex_a->wrp_num))
    {
        LOG_DEBUG("Invalid WRP number in watchpoint");
        return ERROR_OK;
    }

    LOG_DEBUG("rbp %i control 0x%0" PRIx32 " value 0x%0" PRIx32, wrp_i, wrp_list[wrp_i].control, wrp_list[wrp_i].value);

    wrp_list[wrp_i].used = 0;
    wrp_list[wrp_i].value = 0;
    wrp_list[wrp_i].control = 0;

    retval = cortex_a_dap_write_memap_register_u32(target,
                                                                                        armv7a->debug_base + CPUDBG_WCR_BASE + 4 * wrp_list[wrp_i].WRPn,
                                                                                        wrp_list[wrp_i].control);
    if (retval != ERROR_OK)
        return retval;

    retval = cortex_a_dap_write_memap_register_u32(target,
                                                                                        armv7a->debug_base + CPUDBG_WVR_BASE + 4 * wrp_list[wrp_i].WRPn,
                                                                                        wrp_list[wrp_i].value);
    if (retval != ERROR_OK)
        return retval;

    watchpoint->set = 0;

    return ERROR_OK;
}

static int cortex_a_add_watchpoint(struct target *target, struct watchpoint *watchpoint)
{
     struct cortex_a_common* cortex_a = target_to_cortex_a(target);

     if (cortex_a->wrp_num_available < 1)
     {
         LOG_INFO("no hardware breakpoint available");
         return ERROR_TARGET_RESOURCE_NOT_AVAILABLE;
     }

     //if (breakpoint->type == BKPT_HARD)
     cortex_a->wrp_num_available--;

     return cortex_a_set_watchpoint(target, watchpoint);
}

static int cortex_a_remove_watchpoint(struct target *target, struct watchpoint *watchpoint)
{
    struct cortex_a_common* cortex_a = target_to_cortex_a(target);

    if (watchpoint->set)
    {
        //if (breakpoint->type == BKPT_HARD)
        cortex_a_unset_watchpoint(target, watchpoint);

        cortex_a->wrp_num_available++;
    }

    return ERROR_OK;
}

#### 3.
gedit /root/openocd-0.9.0/src/target/cortex_a.c
//in cortex_a_examine_first(struct target *target)
//after LOG_DEBUG("Configured %i hw breakpoints", cortex_a->brp_num);
//add
cortex_a->wrp_num = ((didr >> 28) & 0x0F) + 1;
cortex_a->wrp_num_available = cortex_a->wrp_num;
free(cortex_a->wrp_list);
cortex_a->wrp_list = calloc(cortex_a->wrp_num, sizeof(struct cortex_a_wrp));

for (i = 0; i < cortex_a->wrp_num; i++)
{
    cortex_a->wrp_list[i].used = 0;
    cortex_a->wrp_list[i].value = 0;
    cortex_a->wrp_list[i].control = 0;
    cortex_a->wrp_list[i].WRPn = i;
}
LOG_DEBUG("Configured %i hw watchpoints", cortex_a->wrp_num);

#### 4.
gedit /root/openocd-0.9.0/src/target/cortex_a.c
//both struct target_type cortexa_target and struct target_type cortexr4_target
.add_watchpoint = NULL,
.remove_watchpoint=NULL,
//change to
.add_watchpoint = cortex_a_add_watchpoint,
.remove_watchpoint = cortex_a_remove_watchpoint,

#### 5.
gedit /root/openocd-0.9.0/src/target/arm_dpm.c
//in arm_dpm_setup(struct arm_dpm *dpm)
target->type->add_watchpoint = dpm_add_watchpoint;
target->type->remove_watchpoint = dpm_remove_watchpoint;
//change to
if (!target->type->add_watchpoint)
{
    target->type->add_watchpoint = dpm_add_watchpoint;
    target->type->remove_watchpoint = dpm_remove_watchpoint;
}

//patch done

#### 6. //how to use
in eclipse [Console] window select [GDB Hardware Debugging]  window
add watchpoint command:
monitor wp address sizeof(unit) r/w/a(read/write/access)
ex:
monitor wp 0x8144be4c 4 r

remove watchpoint command:
monitor rwp address
ex:
monitor rwp 0x8144be4c

or

open [Breakpoints] window
click [View Menu] -> [Add Watchpoint (C/C++)...]

Note:After trigger the watchpoint, you must remove it or debug can not continue.
https://picasaweb.google.com/106185541018774360364/IMx6#6245065388141165858

/////////////////////how to break on every driver's function////////////////////
//we want to trace every driver function , but some driver function can not stop
//because driver use gic soft interrupt will affect jtag breakpoint
//here is fix way

//in myandroid/kernel_imx/init/main.c
static void num_call(int fnum)
{
    int a=0, b=0;
    a = fnum;
    b = fnum;
}

static void __init do_initcall_level(int level)
{
    extern const struct kernel_param __start___param[], __stop___param[];
    int                 fnum;
    initcall_t*    fn;

    strcpy(initcall_command_line, saved_command_line);
    parse_args(initcall_level_names[level],
           initcall_command_line, __start___param,
           __stop___param - __start___param,
           level, level,
           &repair_env_string);

    fnum = 0;

    for (fn = initcall_levels[level]; fn < initcall_levels[level+1]; fn++)
    {
        //want to break at level 6, driver function number is 176        
        if( level >= 6 && fnum >= 175 )
*          num_call(fnum); ---> breakpoint stop at 175 first

        do_one_initcall(*fn);

        fnum++;
    }
}

in myandroid/kernel_imx/drivers/irqchip/irq-gic.c
static void gic_raise_softirq(const struct cpumask *mask, unsigned int irq)
{
    int cpu;
    unsigned long flags, map = 0;

    raw_spin_lock_irqsave(&irq_controller_lock, flags);

    for_each_cpu(cpu, mask)
        map |= gic_cpu_map[cpu];

    dmb(ishst);

    writel_relaxed(map << 16 | irq, gic_data_dist_base(&gic_data[0]) + GIC_DIST_SOFTINT);

    //after stop at 175, set breakpoint here and continue
    //then you can see the driver function number is 176
*   raw_spin_unlock_irqrestore(&irq_controller_lock, flags);
}


#### Ref Site:   
a. bus blaster and i.mx6 setting   
http://imx6dev.blogspot.tw/2014/07/inexpensive-jtag-on-imx6-solo-u-boot.html   
http://wiki.wandboard.org/index.php/JTAG-BusBlaster   
b. openocd console config   
http://www.denx-cs.de/doku/?q=m53evkopenocd   
http://www.edlangley.co.uk/blog/2014/06/rescuing-bricked-secure-mode-i.mx6   
http://wiki.voipac.com/xwiki/bin/view/imx6+rex/jtag_oocd   
http://www.imx6rex.com/software/how-to-run-ddr3-calibration-on-imx6    
c. openocd eclipse setting   
https://www.tincantools.com/wiki/BeagleBone_Black_Eclipse_and_GDB    
http://thehackerworkshop.com/?tag=eclipse   
d. arm clock enable    
https://community.freescale.com/thread/376786    

Demo:
1. https://www.youtube.com/watch?v=8K1qY3St06k    
2. https://www.youtube.com/watch?v=2L1vr_LA8Nc      
3. https://picasaweb.google.com/106185541018774360364/IMx6#6241487014458388690    
4. https://picasaweb.google.com/106185541018774360364/IMx6#6241103017491328690    
5. https://picasaweb.google.com/106185541018774360364/IMx6#6240074819468163938    
6. https://picasaweb.google.com/106185541018774360364/IMx6#6239524844608161106    

My OpenOcd full patch:
http://www.mediafire.com/file/ejzocu266juicrt/openocd-0.10.0_v12.tar.gz   
http://www.mediafire.com/file/wpys8ad1hgb9e44/openocd-0.10.0_v10.tar.gz    
http://www.mediafire.com/file/l4f4wgw439xdtzl/openocd-0.10.0_v9.tar.gz    
http://www.mediafire.com/file/l91ahpdqwy18bku/openocd-0.10.0_v8.tar.gz    
http://www.mediafire.com/file/p5ogkicf8nhg14i/openocd-0.9.0_v16.tar.gz    

Docx files:
http://www.mediafire.com/file/t4cv7b1d2z0b53g/openocdv17.docx     
http://www.mediafire.com/file/3b5tbabxjj5a0a6/openocdv16.docx    

My modified source code of uboot and kernel. Search keyword JTAG_DEBUG in files:    
http://www.mediafire.com/file/rddsei4hsdcw8ad/myandroid.tar.gz    

openocd plugin for Eclipse Kepler Service Release 2    
https://github.com/gnu-mcu-eclipse/eclipse-plugins/releases/download/v2.12.1-201604190915/ilg.gnuarmeclipse.repository-2.12.1-201604190915.zip      

Eclipse 64bits linux with ADT + CDT + Openocd packages:       
http://www.mediafire.com/file/7auvmwm2uw8avod/eclipse_adt_cdt_openocd.tar.gz      


### **8. **

-------------
--------------
# **OpenOCD学习**
> OpenOCD可以作为GDBServer，从而方便使用GDB进行调试

## 1. OpenOCD的编译, 安装
```
// 下载的内容
https://github.com/arduino/OpenOCD
http://blog.csdn.net/qingwufeiyang12346/article/details/45954595
http://blog.csdn.net/tugouxp/article/details/54799924
// OPENOCD+JLINK进行STM32开发
https://www.cnblogs.com/tfanalysis/p/3563797.html
```

```
// 下载openocd的zip包
// 安装libusb的开发包
asb@IoT:openocd-0.10.0$ sudo apt-get install libusb++

// 配置openocd
asb@IoT:openocd-0.10.0$ ./configure --enable-jlink  

// make和make install
asb@IoT:openocd-0.10.0$ make
asb@IoT:openocd-0.10.0$ sudo make install

// 执行命令，回去用2440试试，或者直接把环境安装起来
asb@IoT:openocd-0.10.0$ openocd -f interface/jlink.cfg -f target/imx6.cfg
Open On-Chip Debugger 0.10.0
Licensed under GNU GPL v2
For bug reports, read
        http://openocd.org/doc/doxygen/bugs.html
Info : auto-selecting first available session transport "jtag". To override use 'transport select <transport>'.
Warn : imx6.sdma: nonstandard IR value
adapter speed: 1000 kHz
Info : No device selected, using first device.
Error: No J-Link device found.

asb@IoT:openocd-0.10.0$

// 下载ARM官方的也试试

```

// 取消dpkg的错误
http://www.maybe520.net/blog/999/

// ubuntu修改为图形化界面？

// 虚拟机中添加一个USB设备
http://www.myir-tech.com/resource/493.asp
http://blog.csdn.net/tugouxp/article/details/54799924
http://blog.chinaunix.net/uid-11319766-id-3060018.html
http://www.eeworld.com.cn/mcu/article_2016072627853.html



#### ubuntu去掉图形化界面
```
vim /etc/default/grub
把 为text的那行注释掉，把console那行注释掉
/usr/local/share/openocd/scripts/target/s
```
javascript:Object.defineProperty(Object.getPrototypeOf(navigator),'platform',{get:function(){return 'sb_baidu';}})


https://pan.baidu.com/wap/home
// 报销
 discussion
 lsusb




// 解决百度网盘大文件下载限制
-  登录https://greasyfork.org/zh-CN网址, 下载"解决百度云大文件下载限制"
-  chrom安装Tampermonkey插件
-  直接下载即可
// 下载链接
https://d11.baidupcs.com/file/d0f74dea62d048150a3c2d2815ff408b?bkt=p3-000030e005a601a3564913a69f14193e465b&xcode=2db291321d721c7e254733ad015f4064daa06a2da25d7b540b2977702d3e6764&fid=3255651936-250528-468447093426324&time=1513162628&sign=FDTAXGERLQBHSK-DCb740ccc5511e5e8fedcff06b081203-luUjmRbximBQ4ZvzPJYnh5wsZXw%3D&to=d11&size=634123808&sta_dx=634123808&sta_cs=6454&sta_ft=EXE&sta_ct=7&sta_mt=6&fm2=MH,Yangquan,Anywhere,,shanghai,ct&vuk=3155631609&iv=0&newver=1&newfm=1&secfm=1&flow_ver=3&pkey=000030e005a601a3564913a69f14193e465b&sl=79364174&expires=8h&rt=sh&r=976884554&mlogid=8043031780566069793&vbdid=236712677&fin=MDK521a.EXE&fn=MDK521a.EXE&rtype=1&dp-logid=8043031780566069793&dp-callid=0.1.1&hps=1&tsl=100&csl=100&csign=%2BxaM75zqpNSnp6T4DSXogM3sl44%3D&so=0&ut=6&uter=4&serv=0&uc=656145816&ic=3305713692&ti=220620fd8d32b1152e4a04f0010012c4da82f743cbed5fb3&by=themis
-----
https://wiki.segger.com/J-Link_cannot_connect_to_the_CPU#Test_Connection

imx6qsabresd 是contexA9的芯片
// 遇到错误解决方法
Info : DAP transaction stalled (WAIT) – slowing down
Info : DAP transaction stalled (WAIT) – slowing down
Info : DAP transaction stalled (WAIT) – slowing down
Info : sd5115.cpu: hardware has 6 breakpoints, 4 watchpoints
https://blog.csersoft.net/?p=147
https://wiki.segger.com/J-Link_Commander
https://blog.csersoft.net/?p=147
刷新固件
http://blog.csdn.net/perfect1t/article/details/76854260
```
J-Link> connect
Deivce> MCIMX6Q7
其他的默认就可以了
```
直接选择MCIMX6Q7


http://bbs.eeworld.com.cn/thread-427349-1-1.html


45.76.207.182 9900
chacha20
Qwe*90op
