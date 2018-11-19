整理来自[FS4412-Android4.4 HDMI移植的步骤](http://fasight001.spaces.eepw.com.cn/articles/article/item/115955)

## **第一部分：理论扫盲**
### **1. HDMI基础**
HDMI(High-DefinitionMultimedia Interface)高清晰度多媒体接口，首个支持**单线缆上传输不经过压缩的全数字高清晰度、多声道音频和智能格式与控制命令数据的数字接口**    

### **2. 传输原理**
每一个标准的 HDMI 连接,都包含:  
**3个用于传输数据的TMDS传输通道**  
**1个独立的TMDS时钟通道,用来保证传输时所需的统一时序**  
> **术语：**   
1. HDMI把视频信号分为 R、G、B、H、V 五种信号用TMDS技术编码  
2. TMDS:这三个通道传输 R、G、B 三原色,HV 编码在B信号通道里面传输,R、G 的多余位置用来传输音频信号  
3. DDC :即显示数据通道,用来向视频接收装置发送配置信息和数据格式信息,接收装置读取这些 E-EDID(增强扩展显示识别数据)的信息  
4. CEC:即消费电子控制通道,通过这条通道可以控制视听设备的工作   


### **3. HDMI数据容量**


## **第二部分：实践**
### **1. 硬件原理图**
通过HDMI接口引脚定义得出：  
**a) TMDS_D0-、TMDS_D0+, TMDS_D1- 、TMDS_D1+, TMDS_D2- 、TMDS_D2+**三对数据线用来传输**视频**、**音频**、**控制**信号   
**b) TMDS_CLK+、TMDS_CLK-**为HDMI提供时钟源
**c) CE_REMOTE_IN/OUT**
**d) DDC_CLK_IN/OUT DDC_DAT_IN/OUT**Display Data Channel，用于HDMI设备之间的协议沟通
**e) HOTPLUG_DET_IN/OUT**

### **2. 数据手册**
HDMI的视频数据是通过MIXER输入到 HDMI CORE 核心，然后通过 PHY 发送出去，MIXER 是视频混合器，用于图层的混合，音频数据源有两路，一路是 SPDIF 总线输入，另外一路是 I2S 音频总线输入，我们的开发板采用的是 I2S 的音频源，故音频输入是通过 I2S 传输到HDMI CORE 的    

另外需要注意一下 HDMI PHY，Exynos4412 集成了 HDMI PHY，PHY 用于产生 pixel 时钟和TMDS 时钟，我们不再需要额外的 PHY 芯片，这样可以省去 PCB 布线，当然还有 cost，软件通过 CPU 内部的专用的 I2C 总线配置 Phy 寄存器，针对 Phy 进行控制，比如开启，关闭 PHY电源等等    


### **3. 内核代码**
HDMI驱动文件分为两个部分：一个是HDMI架构驱动；另一个是板级相关的驱动

#### **3.1 内核配置**

------
239的服务器上的：/home/asb/github/uboot

## patch修改文件
```
        modified:   arch/arm/cpu/armv7/mx6/Makefile  // 可以
        modified:   arch/arm/cpu/armv7/mx6/clock.c
        modified:   arch/arm/cpu/armv7/mx6/ipu.c
        modified:   arch/arm/include/asm/arch-mx6/clock.h
        modified:   arch/arm/include/asm/arch-mx6/crm_regs.h
        modified:   board/freescale/mx6qsensorgw/mx6qsensorgw.c
        modified:   drivers/misc/Makefile
        modified:   drivers/video/Makefile
        modified:   include/configs/mx6sabre_common.h
```


## HDMI uboot patch修改
1. arch/arm/cpu/armv7/mx6/Makefile
```
asb@IoT:uboot$ git diff arch/arm/cpu/armv7/mx6/Makefile
+obj-$(CONFIG_UBOOT_LOGO_ENABLE) += ipu.o
asb@IoT:uboot$ 
```

2. 
```
asb@IoT:uboot$ git diff arch/arm/include/asm/arch-mx6/crm_regs.h
diff --git a/arch/arm/include/asm/arch-mx6/crm_regs.h b/arch/arm/include/asm/arch-mx6/crm_regs.h
index 0531cac..d227aad 100644
--- a/arch/arm/include/asm/arch-mx6/crm_regs.h
+++ b/arch/arm/include/asm/arch-mx6/crm_regs.h
@@ -104,6 +104,12 @@ struct mxc_ccm_reg {
        u32 analog_pfd_528_clr;
        u32 analog_pfd_528_tog;
        /* PMU Memory Map/Register Definition */
+    u32        ana_misc2;      
+
+
+
+
+
        u32 pmu_reg_1p1;
        u32 pmu_reg_1p1_set;
        u32 pmu_reg_1p1_clr;

```


 export PATH=/home/asb/L4.1.15/bin:$PATH
  mkdir fsl-release-bsp
  cd fsl-release-bsp/

asb@IoT:fsl-release-bsp$ repo init -u http://git.freescale.com/git/cgit.cgi/imx/fsl-arm-yocto-bsp.git -b imx-4.1-krogoth -m imx-4.1.15-2.0.0.xml



liu:Downloads xingyanl$ git clone http://git.freescale.com/git/cgit.cgi/imx/uboot-imx.git -b imx_v2015.04_4.1.15_1.0.0_ga
Cloning into 'uboot-imx'...


http://git.freescale.com/git/cgit.cgi/imx/
