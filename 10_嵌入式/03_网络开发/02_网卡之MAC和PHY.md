### **网卡之MAC和PHY**
整理自[网口扫盲三:以太网芯片MAC和PHY的关系](http://www.cnblogs.com/jason-lu/p/3195473.html)

#### **MAC的概念**
**数据链路层**包含**MAC(介质访问控制)子层**和**LLC(逻辑链路控制)子层**, 一块以太网卡MAC芯片的作用不但要实现MAC子层和LLC子层的功能,还要提供符合规范的PCI界面以实现和主机的数据交换.

**MAC(Media Access Control)**,即媒体访问控制子层协议, 位于OSI七层协议中数据链路层的下半部分, 主要负责**控制与连接物理层**的物理介质   
**发送数据**,MAC协议会先判断是否可以发送数据, 若可以则给数据加上一些控制信息,最终将数据以及控制信息以帧格式发送到物理层  
**接收数据**,MAC协议会先判断输入的信息是否发生传输错误,如果没有错误,则去掉控制信息发送至LLC层
> MAC层协议由IEEE-802.3以太网标准定义, 最新的MAC同时支持10Mbps和100Mbps两种速率.


MAC从PCI总线收到IP数据包(或者其他网络层协议的数据包)后,将之拆分并重新打包成最大1518Byte,最小64Byte的帧.这个帧里面包括了目标MAC地址、自己的源MAC地址和数据包里面的协议类型(比如IP数据包的类型用80表示).最后还有一个DWORD(4Byte)的CRC码.

可是目标的MAC地址是哪里来的呢?这牵扯到一个ARP协议(介乎于网络层和数据链路层的一个协议).第一次传送某个目的IP地址的数据的时候,先会发出一个ARP包,其MAC的目标地址是广播地址,里面说到：”谁是xxx.xxx.xxx.xxx这个IP地址的主人？”因为是广播包,所有这个局域网的主机都收到了这个ARP请求.收到请求的主机将这个IP地址和自己的相比较,如果不相同就不予理会,如果相同就发出ARP响应包.这个IP地址的主机收到这个ARP请求包后回复的ARP响应里说到:”我是这个IP地址的主人”.这个包里面就包括了他的MAC地址.以后的给这个IP地址的帧的目标MAC地址就被确定了.(其它的协议如IPX/SPX也有相应的协议完成这些操作.)

IP地址和MAC地址之间的关联关系保存在主机系统里面,叫做ARP表,由驱动程序和操作系统完成.在Microsoft的系统里面可以用arp-a的命令查看ARP表.收到数据帧的时候也是一样,做完CRC以后,如果没有CRC效验错误,就把帧头去掉,把数据包拿出来通过标准的借口传递给驱动和上层的协议客栈,最终正确的达到我们的应用程序.

还有一些控制帧,例如流控帧也需要MAC直接识别并执行相应的行为.

以太网MAC芯片的一端接计算机PCI总线,另外一端就接到PHY芯片上,它们之间是通过MII接口链接的.


#### **PHY的概念**
问:以太网PHY是什么?
答:PHY是物理接口收发器,它实现物理层.IEEE-802.3标准定义了以太网PHY.包括MII/GMII(介质独立接口)子层,PCS(物理编码子层),PMA(物理介质附加)子层,PMD(物理介质相关)子层,MDI子层.它符合IEEE-802.3k中用于10BaseT(第14条)和100BaseTX(第24条和第25条)的规范.

PHY在发送数据的时候,收到MAC过来的数据(对PHY来说,没有帧的概念,对它来说,都是数据而不管什么地址,数据还是CRC.对于100BaseTX因为使用4B/5B编码,每4bit就增加1bit的检错码),然后把并行数据转化为串行流数据,再按照物理层的编码规则把数据编码,再变为模拟信号把数据送出去.收数据时的流程反之.PHY还有个重要的功能就是实现CSMA/CD的部分功能.它可以检测到网络上是否有数据在传送,如果有数据在传送中就等待,一旦检测到网络空闲,再等待一个随机时间后将送数据出去.如果两个碰巧同时送出了数据,那样必将造成冲突,这时候,冲突检测机构可以检测到冲突,然后各等待一个随机的时间重新发送数据.这个随机时间很有讲究的,并不是一个常数,在不同的时刻计算出来的随机时间都是不同的,而且有多重算法来应付出现概率很低的同两台主机之间的第二次冲突.

许多网友在接入Internt宽带时,喜欢使用”抢线”强的网卡,就是因为不同的PHY碰撞后计算随机时间的方法设计上不同,使得有些网卡比较”占便宜”.不过,抢线只对广播域的网络而言的,对于交换网络和ADSL这样点到点连接到局端设备的接入方式没什么意义.而且”抢线”也只是相对而言的,不会有质的变化.

现在交换机的普及使得交换网络的普及,使得冲突域网络少了很多,极大地提高了网络的带宽.但是如果用HUB,或者共享带宽接入Internet的时候还是属于冲突域网络,有冲突碰撞的.交换机和HUB最大的区别就是:一个是构建点到点网络的局域网交换设备,一个是构建冲突域网络的局域网互连设备.

除此之外PHY还提供了和对端设备连接的重要功能并通过LED灯显示出自己目前的连接的状态和工作状态让我们知道.当我们给网卡接入网线的时候,PHY不断发出的脉冲信号检测到对端有设备,它们通过标准的”语言”交流,互相协商并却定连接速度、双工模式、是否采用流控等.通常情况下,协商的结果是两个设备中能同时支持的最大速度和最好的双工模式.这个技术被称为AutoNegotiation或者NWAY,它们是一个意思–自动协商.

具体传输过程为,发送数据时,网卡首先侦听介质上是否有载波(载波由电压指示),如果有,则认为其他站点正在传送信息,继续侦听介质.一旦通信介质在一定时间段内(称为帧间缝隙IFG=9.6微秒)是安静的,即没有被其他站点占用,则开始进行帧数据发送,同时继续侦听通信介质,以检测冲突.在发送数据期间,如果检测到冲突,则立即停止该次发送,并向介质发送一个“阻塞”信号,告知其他站点已经发生冲突,从而丢弃那些可能一直在接收的受到损坏的帧数据,并等待一段随机时间(CSMA/CD确定等待时间的算法是二进制指数退避算法).在等待一段随机时间后,再进行新的发送.如果重传多次后(大于16次)仍发生冲突,就放弃发送.接收时,网卡浏览介质上传输的每个帧,如果其长度小于64字节,则认为是冲突碎片.如果接收到的帧不是冲突碎片且目的地址是本地地址,则对帧进行完整性校验,如果帧长度大于1518字节(称为超长帧,可能由错误的LAN驱动程序或干扰造成)或未能通过CRC校验,则认为该帧发生了畸变.通过校验的帧被认为是有效的,网卡将它接收下来进行本地处理.
