# ipython入门
[在ipython中安装TensorFlow](https://www.cnblogs.com/aloiswei/p/6510355.html)

> 大牛之所以为大牛，就是因为他们更认真，付出更多

## python版本更换
> 前提是/usr/bin要在PATH的最前面

```
// 查看版本
asb@IoT:fsl-release-bsp$ update-alternatives --list python 
/home/asb/anaconda3/bin/python
/usr/bin/python2.7
/usr/bin/python3.4
asb@IoT:fsl-release-bsp$ 

// 添加1：python2.7
asb@IoT:fsl-release-bsp$ sudo update-alternatives --install /usr/bin/python python /usr/bin/python2.7  1

// 添加2：python3.4
asb@IoT:fsl-release-bsp$ sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.4 2 

// 添加3: anaconda3 python
asb@IoT:~$ sudo update-alternatives --install /usr/bin/python python /home/asb/anaconda3/bin/python 3

// 更换为2.7
asb@IoT:fsl-release-bsp$ sudo update-alternatives --config python
There are 3 choices for the alternative python (providing /usr/bin/python).

  Selection    Path                            Priority   Status
------------------------------------------------------------
* 0            /home/asb/anaconda3/bin/python   3         auto mode
  1            /home/asb/anaconda3/bin/python   3         manual mode
  2            /usr/bin/python2.7               1         manual mode
  3            /usr/bin/python3.4               2         manual mode

Press enter to keep the current choice[*], or type selection number: 2
update-alternatives: using /usr/bin/python2.7 to provide /usr/bin/python (python) in manual mode
asb@IoT:fsl-release-bsp$ 

// 删除某个版本
asb@IoT:fsl-release-bsp$ sudo update-alternatives --remove python /usr/bin/python2.7 
update-alternatives: removing manually selected alternative - switching python to auto mode
update-alternatives: using /home/asb/anaconda3/bin/python to provide /usr/bin/python (python) in auto mode
asb@IoT:fsl-release-bsp$ 

asb@IoT:fsl-release-bsp$ sudo update-alternatives --remove python /usr/bin/python3.4
update-alternatives: removing manually selected alternative - switching python to auto mode
update-alternatives: using /home/asb/anaconda3/bin/python to provide /usr/bin/python (python) in auto mode

asb@IoT:fsl-release-bsp$ sudo update-alternatives --remove python /home/asb/anaconda3/bin/python

```