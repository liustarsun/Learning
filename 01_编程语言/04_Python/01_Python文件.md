# python 脚本

# 目的：做几个python命令脚本

## 1. command execution
command file:
	CmdExecute.py

usage:
	CmdExecute.py <cmd> <para1> <para2>...

遇到的编码问题:
'ascii' codec can't encode characters in position 3-5:
解决方案：不再使用str来转换unicode到encode的代码了       
Basically, stop using str to convert from unicode to encoded text / bytes.
核心问题：
1. 如何接收命令行输入的参数，如果没有是让输入，还是给一个默认的？===>目前是不判断是否为空，也不判断是否输入正常
> 目前不进行判断，只是把输入的命令直接打印出来

2. 首先要ssh连接


## 2. file upload
command file:
	FileUpload.py

usage:
	FileUpload.py <local_file> <afaa_dir> ====>把代码里面的后面的参数拼接成afaa_dir+local_file名字的问题，如果后面是个文件就不用拼接
    FileUpload.py <local_dir> <afaa_dir>

核心问题：
1. 传文件
2. 传目录

```
// ftp退出命令
ftp> quit

// ftp服务重启
启动Vsftpd服务其命令为： service vsftpd start 或 /etc/init.d/vsftpd start

停止Vsftpd服务的命令为：service vsftpd stop 或 /etc/init.d/vsftpd stop

重新启动Vsftpd服务的命令为：service vsftpd restart 或 /etc/init.d/vsftpd restart

检查Vsftpd服务的运行状态：service vsftpd status
```

## 3. file download
command file:
	FileDownload.py

usage:
	FileDownload.py <afaa_file> <local_dir>===>在代码里面把这个转换成local_dir+afaa_file的样子，如果后面是个文件就不用拼接
	FileDownload.py <afaa_dir> <local_dir>

    字符串拼接问题

核心问题：
1. 下载文件
2. 下载目录

```
from common.ftp import *


if __name__ == '__main__':
    time_now = time.localtime()
    date_now = time.strftime('%Y-%m-%d', time_now)

    # 配置如下变量
    host_address = '135.252.5.238'  # ftp地址
    username = 'asb'  # 用户名
    password = 'asb#1234'  # 密码
    port = 21  # 端口号

    #**************************#
    # FileDownload.py <afaa_file> <local_dir>
    # FileDownload.py <afaa_dir> <local_dir>
    #**************************#
    # 1.1 输入2个参数 python FileDownload.py
    root_dir_local = 'D:/tmp'
    root_dir_remote = '/home/asb/ftptest'
    # f.download_files(root_dir_local, root_dir_remote)

    # 1.2 输入3个参数 
    # a. python FileDownload.py '/home/asb/test.cc'===>是文件
    file_remote = sys.argv[2]
    root_dir_remote = os.path.dirname(file_remote)
    root_dir_local = 'D:/tmp'
    file_local = root_dir_local + "/" + os.path.basename(file_remote)
    # f.download_file(file_local, file_remote)===>下载文件

    # b. python FileDownload.py '/home/asb'===>是目录
    root_dir_remote = sys.argv[2]
    root_dir_local = 'D:/tmp'
    # f.download_files(root_dir_local, root_dir_remote)===>下载目录
   

    # 1.3 输入4个参数，判断4个参数的
    // 这种情况
    # a. python FileDownload.py '/home/asb/test.cc' 'D:/ftptest'
    file_remote = sys.argv[2]
    root_dir_remote = os.path.dirname(file_remote)
    root_dir_local = sys.argv[3]
    file_local = root_dir_local + "/" + os.path.basename(file_remote)
    # f.download_file(file_local, file_remote)===>下载文件

# =========================
    # b. python FileDownload.py '/home/asb/test.cc' 'D:/ftptest/test.cc'
    file_remote = sys.argv[2]
    root_dir_remote = os.path.dirname(file_remote)
    file_local = sys.argv[3]
    # f.download_file(file_local, file_remote)===>下载文件
# =========================

// 这种情况
    # c. python FileDownload.py '/home/asb' 'D:/ftptest'
    root_dir_remote = sys.argv[2]
    root_dir_local = sys.argv[3] 
    # f.download_files(root_dir_local, root_dir_remote)===>下载目录

    f = FTPHelper(host_address, username, password, root_dir_remote, port)
    f.login()
    f.download_files(root_dir_local, root_dir_remote)
    f.download_file(file_local, file_remote)

    #**************************#
    # FileUpload.py <local_file> <afaa_dir>
    # FileUpload.py <local_dir> <afaa_dir>  ===> 下面考虑的就是如何把这些整合在一起
    #**************************#
    # 1.1 输入2个参数 python FileUpload.py
    root_dir_local = 'D:/tmp'
    root_dir_remote = '/home/asb/ftptest'
    # f.upload_files(root_dir_local, root_dir_remote)

    # 1.2 输入3个参数 
    # a. python FileUpload.py 'D:/tmp/test.cc'===>是文件
    file_local = sys.argv[2]
    root_dir_remote = '/home/asb/ftptest'
    file_remote = root_dir_remote + "/" + os.path.basename(file_local)
    # f.upload_file(file_local, file_remote)===>下载文件

    # b. python FileUpload.py 'D:/tmp'===>是目录
    root_dir_local = sys.argv[2]
    root_dir_remote = '/home/asb/ftptest'
    # f.upload_files(root_dir_local, root_dir_remote)===>下载目录
   
    # 1.3 输入4个参数
    // 这种情况
    # a. python FileUpload.py 'D:/tmp/test.cc' 'D:/ftptest'
    file_local = sys.argv[2]
    root_dir_remote = sys.argv[3]
    file_remote = root_dir_remote + "/" + os.path.basename(file_local)
    # f.upload_file(file_local, file_remote)===>下载文件

# =========================
    # b. python FileUpload.py 'D:/tmp/test.cc' 'D:/ftptest/test.cc'
    file_local = sys.argv[2]
    file_remote = sys.argv[3]
    root_dir_remote = os.path.dirname(file_remote)
    # f.upload_file(file_local, file_remote)===>下载文件
# =========================

// 这种情况
    # c. python FileUpload.py 'D:/tmp' '/home/asb'
    root_dir_local = sys.argv[2]
    root_dir_remote = sys.argv[3] 
    # f.upload_files(root_dir_local, root_dir_remote)===>下载目录


    f = FTPHelper(host_address, username, password, root_dir_remote, port)
    f.login()
    f.upload_file(file_local, file_remote)
    f.upload_files(root_dir_local, root_dir_remote)
```