**grep命令**   
```
// 递归目录搜索，关键字为mx6q
grep "mx6q" * -nR
```

**hexdump命令**
```
// 以二进制查看
asb@ubuntu:Iot$ hexdump -C imx6q-sabresd.dtb | more
```
**md5sum**
```
// 查看文件是否相同
xingyanl@yocto-DL580:~$ md5sum u-boot-sd-2017.03-r0.imx
b329bfc361609798c7c93d78686bc9fe  u-boot-sd-2017.03-r0.imx
xingyanl@yocto-DL580:~$ 
```

**vi中常用命令**
```
ggdG // 删除所有内容，从第1行到最后1行


```

### tar命令
```
xingyanl@yocto-DL580:sdk$ tar -zcvf 压缩文件 压缩目录


```

### vi命令

```
// 删除列
gg  "到文件首行

ctrl+v  "可视块模式

100j,2l "选中行和列

d   "删除行或则列
```
