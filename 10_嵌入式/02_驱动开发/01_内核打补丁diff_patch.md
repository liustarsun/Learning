## **diff和patch命令**
> 这对命令获取更新文件和历史文件差异，并更新到历史文件；diff相当于两个集合的差运算，patch相当于两个集合的和运算

### **diff命令**
```
asb@IoT:linux$ diff original.txt updated.txt
1,4c1 // 1-4行，原来内容，每段以这种格式开始
< #include <stdio.h>
<
< function old(){
<         printf("This is a file\n");
---
> #include stdio.h  // 替换后的1行的新内容
5a3,4    // 在源文件中，追加新文件的3,4行内容
> function new(){
>         printf("This is b file\n");
asb@IoT:linux$
```
+ > **1,4c1:** 这个内容输出实际上是给patch看的，表示告诉patch在*original.txt*文件中的1到4行应当被*updated.txt*中的第1行替换; 每次都以这种格式开始
+ > **c:** 表示在original文件中的m,n行的内容将要被updated文件中的内容替换
+ > **a:** 表示追加，这时左边的数字只能是一个数字，而不会是一个范围，表示向original文件中追加右侧数字表示内容
+ > **d:** 表示删除。左侧的数字可能是一个范围，表示要删除的内容，右侧是一个数字，表示如果没有被删除应该出现在updated文件的什么位置。也许有人觉得后边的数字是多余的，保留这个数字是因为补丁可以反向使用
+ > **<:** 表示patch应当将这个标志后面的内容删除
+ > **\>:** 表示patch应当将这个标志后面的内容添加

### **patch命令**
> 补丁实际上就是diff的输出结果，直接将输出结果保存成文件

```
// 生成patch文件
asb@IoT:linux$ diff original.txt updated.txt  > mypatch.patch

// 更新文件
asb@IoT:linux$ patch original.txt -i mypatch.patch -o updated-1.txt // 打patch文件命令
patching file updated-1.txt (read from original.txt)
asb@IoT:linux$ diff updated.txt updated-1.txt // 可以看出patch已经打上，两则相同了
```


### **上下文补丁**
> 问题: 观察之前diff给出的结果样式，对于需要替换的位置，仅仅给出了行号，如果文件突然新增了一个空行，补丁应用的时候就会发生问题。另外一种情况，如果将补丁文件应用到了一个错误的源文件上，假如恰好这个文件有同样的行数，那么补丁也可以成功应用。而这都是我们不希望看到的结果。幸好，diff提供了一种不同的结果样式来避免上面的这些问题

```
asb@IoT:linux$ diff -c original.txt updated.txt  // 上下文patch
*** original.txt        2017-12-06 13:14:55.703280899 +0800
--- updated.txt 2017-12-06 13:15:16.287280858 +0800
***************
*** 1,7 ****   // 行号
! #include <stdio.h>  // 需要替换内容
!
! function old(){
!         printf("This is a file\n");

          return 0;
  }
--- 1,6 ----   // 行号
! #include stdio.h

+ function new(){   // 添加内容
+         printf("This is b file\n");
          return 0;
  }
// 打patch，如果不指定输出文件的话，源文件就会被更新
asb@IoT:linux$ patch -i mypatch.patch -o updated3.txt
```
+ > 比较结果中包含了文件名，这样我们在应用补丁的时候，就不用输入文件名，从而节省了时间，避免了文件名输入错误的可能, 文件名后都跟着文件的修改时间
+ > 15个星号 * 表示后面的内容为文件替换、更新、删除等
+ > **\*\*\*号和---号** 包含的数字或者数字范围表示行号
+ > **!号:** 开始的内容表示需要替换的内容
+ > **-:** 表示需要删除的内容
+ > **+:** 表示需要增加的内容

**patch会依据以上的上下文关系对文件进行更新**


#### **GNU常用打补丁方式**
```
// 内核常用方式,从介绍来看这个使用更普遍
// -u 显示有差异行的前后几行(上下文), 默认是前后各3行, 这样, patch中带有更多的信息.
// -p 显示代码所在的c函数的信息
// -r 递归地对比一个目录和它的所有子目录(即整个目录树)
// -N 如果某个文件缺少了, 就当作是空文件来对比.
// 如果不使用本选项, 当diff发现旧代码或者新代码缺少文件时, 只简单的提示缺少文件. 如果使用本选项, 会将新添加的文件全新打印出来作为新增的部分.
asb@IoT:linux$ diff -purN original.txt updated.txt > mypatch2.patch
// 生成的补丁中, 路径信息包含了你的Linux源码根目录的名称, 但其他人的源码根目录可能是其它名字,
// 所以, 打补丁时, 要进入你的Linux源码根目录, 并且告诉patch工具, 请忽略补丁中的路径的第一级目录(参数-p1).
asb@IoT:linux$ cd linux-2.6.31.3
asb@IoT:linux$ patch -p1 < mypatch
```

### **比较多个文件并应用补丁**
> 比较多个文件最简单的办法就是直接在命令后面跟文件夹; 如果包含子文件夹，需要加上-r参数
> patch会在当前文件夹查找文件（默认情况下patch会将文件名前的所有文件夹去掉）因为此时补丁文件在文件夹外面，所以我们应当告诉patch不要这么做，使用-p参数

```
// 对目录打patch
patch -p0 -i directory.patch
// 有时候版本需要进行回撤，这时可以使用 -R 参数
patch -p0 -R -i directory.patch
// GNU的diff和patch还提供了一种格式，称为 the unified format
// 与上下文格式类似。但是不再将源文件和更新文件分开，而是组合在一起。并且没有特殊的替换标志，只有-和+
diff -u original update
```
