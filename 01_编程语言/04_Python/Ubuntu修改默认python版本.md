#  **Ubuntu修改默认python版本的方法**
> 需要root权限

## 1. 使用**update-alternatives**识别python的版本

```
asb@IoT:~$  sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7 1
asb@IoT:~$  sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.4 2
```
> **install** 选项使用多个参数用来创建符号链接，最后一个参数指定优先级(**数字越大，优先级越高**)，默认选择最高的优先级

```
asb@IoT:~$  python --version  
Python 3.4.2
```

## 2. 查看python版本

```
asb@IoT:~$ sudo update-alternatives --list python  
/usr/bin/python2.7
/usr/bin/python3.4
asb@IoT:~$
```

## 3. 选择默认使用python版本

```
asb@IoT:~$ sudo update-alternatives --config python
There are 2 choices for the alternative python (providing /usr/bin/python).

  Selection    Path                Priority   Status
------------------------------------------------------------
  0            /usr/bin/python3.4   2         auto mode
  1            /usr/bin/python2.7   1         manual mode
* 2            /usr/bin/python3.4   2         manual mode

Press enter to keep the current choice[*], or type selection number: （选择使用版本）

```

## 4. 移除使用版本

```
asb@IoT:~$ sudo update-alternatives --remove python /usr/bin/python2.7  
```
