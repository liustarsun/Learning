# 1. 烧写
[参考文档](http://www.cnblogs.com/helloworldtoyou/archive/2016/12.html)
```
    <!-- 将u-boot.bin写到/dev/mtd0，每次读写的大小是512-->
    <CMD state="Updater" type="push" body="$ dd if=$FILE of=/dev/mtd0 bs=512">write U-Boot to SPI-NOR</CMD>
    <CMD state="Updater" type="push" body="send" file="mksdcard-android.sh.tar">Sending partition shell</CMD>
    <CMD state="Updater" type="push" body="$ tar xf $FILE "> Partitioning...</CMD>
    <CMD state="Updater" type="push" body="$ sh mksdcard-android.sh /dev/mmcblk0"> Partitioning...</CMD>
    <!-- 使用脚本将/dev/mmcblk0进行分区-->
    <CMD state="Updater" type="push" body="$ ls -l /dev/mmc* ">Formatting sd partition</CMD>
    <!-- burn the uboot: -->
    <CMD state="Updater" type="push" body="send" file="files/android/u-boot.bin">Sending U-Boot</CMD>
    <!-- 将/dev/mmcblk0清0，每次操作512字节，操作次数200次，操作位置，从偏移2block的地方开始输出-->
    <CMD state="Updater" type="push" body="$ dd if=/dev/zero of=/dev/mmcblk0 bs=512 seek=2 count=2000">Clean U-Bootenvironment</CMD>
    <!-- 将u-boot.bin写道/dev/mmcblk0，每次写512字节，从uboot偏移地址是2 block的地方开始读取，从/dev/mmcblk0偏移2block的地方开始输出 -->
    <CMD state="Updater" type="push" body="$ dd if=$FILE of=/dev/mmcblk0 bs=512 seek=2 skip=2">write U-Boot to sdcard</CMD>
    <!-- burn the uImage: -->
    <CMD state="Updater" type="push" body="send" file="files/android/boot.img">Sending kernel uImage</CMD>
    <!-- 将boot.img写入到/dev/mmcblk0p1 -->
    <CMD state="Updater" type="push" body="$ dd if=$FILE of=/dev/mmcblk0p1">write boot.img</CMD>
    <CMD state="Updater" type="push" body="frf">flush the memory.</CMD>
    <!-- 将/dev/mmcblk0p4格式化位ext4文件系统，并指定卷标名称为data-->
    <CMD state="Updater" type="push" body="$ mkfs.ext4 -L data /dev/mmcblk0p4">Formatting sd partition</CMD>
    <!-- 将/dev/mmcblk0p5格式化位ext4文件系统，并指定卷标名称为system-->
    <CMD state="Updater" type="push" body="$ mkfs.ext4 -L system /dev/mmcblk0p5">Formatting system partition</CMD>
    <!-- 将/dev/mmcblk0p6格式化位ext4文件系统，并指定卷标名称为cache-->
    <CMD state="Updater" type="push" body="$ mkfs.ext4 -L cache -O^extent /dev/mmcblk0p6">Formatting cache partition</CMD>
    <!-- 将/dev/mmcblk0p7格式化位ext4文件系统，并指定卷标名称为vender-->
    <CMD state="Updater" type="push" body="$ mkfs.ext4 -L vender /dev/mmcblk0p7">Formatting data partition</CMD>
    <CMD state="Updater" type="push" body="frf">flush the memory.</CMD>
    <CMD state="Updater" type="push" body="$ mkfs.ext4 /dev/mmcblk0p8">Formatting misc partition</CMD>
    <!-- 将system.img些到/dev/mmcblk0p5中,由于文件比较大，所以是通过读取管道再写入-->
    <CMD state="Updater" type="push" body="pipe dd of=/dev/mmcblk0p5 bs=512" file="files/android/system.img">Sending and writting system.img</CMD>
    <CMD state="Updater" type="push" body="frf">flush the memory.</CMD> 
```


# 2. 启动模式
```
1. 根据BOOT_MODE[1:0]引脚的值选择启动类型
2. 根据BOOT_CFG1[7:4]选择启动设备的类型，如果没有选择的设备，则进入download模式
3. 新版与旧版的一个区别是烧写使用的uboot后缀是.imx，而不是原来的.bin。以后缀.imx结尾的uboot在镜像开头1k的地方添加了IVT表，这两个镜像的区别是，u-boot.bin文件编译后，会在u-boot.bin的开头添加一个大小为1K的IVT头，用于告诉BOOT ROM找到uboot的位置和函数,要运行在什么模式，DRAM的配置数据等。新生成的文件就是u-boot.imx文件
4. Device Configuration Data(DCD)，The Image Vector Table (IVT)
```
# ROM读取IVT中内容。
# IVT包含DCD的入口点和其他的入口点，给ROM使用。
# IVT在设备中的地址是固定的，这样ROM才能够找到。
# IVT表在不同设备中的偏移地址和空间的大小(Table 8-24. Image Vector Table Offset and Initial Load Region Size
这个是在每个设备中都是固定的)
8.6.2 Device Configuration Data (DCD)
# 开启启动的时候根据需要更改寄存器的默认值,方便一些外设一开机就配置

查看编译uboot生成的System.map也能够知道大概的分布情况。

imx6开启启动之后，运行板子上的ROM程序。ROM确定启动的设备，进行一些初始化，然后读取IVT，进行寄存器初始化,最后运行uboot/cpu/arm_cortexa8/start.S中的_start函数。

IVT中记录了寄存器的地址和要设置的值，以及uboot的_start函数。

初始化完成之后，最后运行uboot/cpu/arm_cortexa8/start.S中的 _start函数，进行uboot的初始化。
