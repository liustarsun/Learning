# UART

-----
## 1. 概念
- Universal Async Receiver transmitter，通用异步的接收和发送装置
- 异步串行通讯：**双方协商一个固定的速率，以一个bit的顺序发送和接收数据**
- SCI串行通讯接口，和UART相互兼容
> 串行的，异步的，点对点的，全双工的，对等的

------
## 2. 硬件
- 每个设备都需要3条线：发送，接收和地线：
1. 一个发送TX引脚
2. 一个接收RX引脚
3. 一个共地
> 一个TX接另一个的RX，**发送端没有给接收端使用同一个时钟**，而是**约定一个速率**，双方进行通讯

------
## 3. 协议
- 如何传送数据：**双方约定波特率**
- 串口控制器：设置好**串口控制器**自动产生数据，让引脚发生变化；通过设置**串口控制器对应的寄存器**来确定双方的协议，把值写进去**某个地址位置**就可以了
- 双方使用**自己的时钟的驱动**进行发送和接收，因此有可能会导致频率不同，产生错位误差
- 使用**数据帧的格式**进行发送和接收，USB和以太网中的数据也是以**帧格式**进行传递，每个帧中**承载若干字节的数据**，通过结构把它封装起来，形成一个**Frame**
> 通道是空闲的状态的时候，维持**逻辑1的状态不变**，每当一次通讯发起的时候，数据帧有一个**起始位和停止位**，并且**起始位永远为逻辑0**，**停止位永远为逻辑1**，数据帧为8位
> 1个bit的宽度的倒数定义为**波特率**，即每秒钟传递多少个宽度来定义的
> 使用数据帧的格式是为了避免误差的累积

### 3.1 参数
- LSB：从低位开始发送；MSB：从高位开始发送    
> UART约定：**LSB先发，跟着起始位的后面，MSB后发，跟在停止位的前面；**起始位--->(低位----->高位**8个bit的数据位**)--->(可选的校验位)------>停止位，有可能还会有一个校验位
> 在数据帧存在的情况下，误差不会被累积，当一个帧的里面时钟**误差不大于%5**，就是可以接受的


### 3.2 过采样

------
## 4. RS232标准(串口serial port)


------
## 5. UART寄存器编程
- 对所有外设的编程都是通过**映射在地址上的一系列寄存器的写0或者1来实现的**；写入的是数据，实际工作的是通过这些0或者1对电路的控制来实现**对外设工作方式，工作状态的控制**，从而实现让外设工作
- 编程实现则需要：
1. 首先把模块所用到的**时钟打开**，因为默认状态下，这些时钟是关闭的，这样一个模块是属于低功耗的
2. 决定**管脚复用模式iomux**
3. 对于每个模块，再**控制其相关的寄存器**

### 5.1 打开时钟
- Bus clock是**总的时钟的一半**，查数据手册看看需要打开那个寄存器
> MCU中有两个寄存器，一个是**UART模块的时钟源**，一个是UART用的那个**引脚所对应的port的时钟源**

### 5.2 选择复用的功能

### 5.3 相关寄存器
- UART发送的电路是通过对应的寄存器的值来控制，有序的发送的

#### 5.3.1 波特率寄存器
- 有一个16倍的概念

#### 5.3.2 数据寄存器
- 对于数据寄存器写和读是**通过两个不同的方向**，和存储器写个值，然后把写的那个值再读出来**不一样**
- 写操作是**发送一个值**，读操作是**把对方给的回应读出来**

#### 5.3.3 控制寄存器
- 控制逻辑会有一个副产品，就是会有一系列的**中断产生**，串行通讯和IO一样，也是可以工作在中断方式下的
- 要打开控制寄存器的**RX enable**和**TX enable** 

#### 5.3.4 状态寄存器
- 发送器数据缓存**TDRE**，如果**空了为1**，才继续发送
- 接收器数据缓存**RDRF**，如果**空了为1**，才继续接收
> 以上的都是阻塞的