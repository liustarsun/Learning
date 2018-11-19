# 1. 标准输入流
stdin(C语言) / cin(CPP语言)      
 
# 2. 标准输出流
stdout(C语言) / cout(CPP语言)
1. 数据有缓冲，在缓冲区满，程序正常退出；流被关闭或强制刷新(fflush()函数)时输出
2. 等缓冲区满后，同时打印多个句号

#### 注释 
在某些操作系统中是无缓冲的      

```
while(1)
{
    printf(".");
    sleep(1);
}
```
# 3. 标准错误流
stderr(C语言) / cerr(CPP语言)     
1. 默认是无缓冲的，直接输出的

```
while(1)
{
    fprintf(stderr, ".");
    sleep(1);
}
```
