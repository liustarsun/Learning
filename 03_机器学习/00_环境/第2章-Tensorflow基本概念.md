### **第2章-TensorFlow基本概念**
分为3个部分：计算模型，数据模型和运行模型      
#### **1. 计算模型**
##### **1.1 计算图的概念**  
在TensorFlow中，所有的计算都会被转换成为**计算图上**的节点，节点之间的边描述了计算之间的依赖关系，因此tensorflow是一个通过计算图的形式来表达计算的编程系统，即**计算图描述运算**   
- **Tensor和Flow**    
**Tensor**就是张量, 可以简单理解为多维数组，代表数据结构  
**Flow**则代表计算模型，它直观表达了张量之间通过计算相互转化的过程  

Tensorflow的计算图中每个节点都是一个运算，每条边代表了计算之间的依赖，如果一个运算的输入依赖于另一个运算的输出，则这两个运算有依赖关系  

##### **1.2 计算图的使用**  
通常分两个阶段：
- 第一阶段定义计算图中所有的运算  
系统自动维护一个默认的计算图，通过**tf.get_default_graph**函数可以获取当前默认的计算图  

```
In [2]: import tensorflow as tf
In [3]: a = tf.constant([1.0, 2.0], name="a")
In [4]: b = tf.constant([2.0, 3.0], name="b")
In [5]: result = a + b
# a.graph可以查看a张量所属的计算图，如果不特意指定，则属于默认计算图
In [6]: print(a.graph is tf.get_default_graph())
True
In [7]:
```
TensorFlow支持通过**tf.Graph函数**生成新的计算图，不同计算图上的张量和运算不共享，如：
```
import tensorflow as tf
g1 = tf.Graph()
with g1.as_default():
    # 在计算图g1中，定义v，初值为0
    v = tf.get_variable("v", initializer=tf.zeros_initializer(shape=[1]))

g2 = tf.Graph()
with g2.as_default():
    # 在计算图g2中，定义v，初值为1
    v = tf.get_variable("v", initializer=tf.ones_initializer(shape=[1]))
```

- 第二阶段执行计算  
**读取上面定义的g1和g2中的变量v**  

```
with tf.Session(graph=g1) as sess:
    tf.initializer_all_variables().run()
    # 计算图g1中，v为0，因此输出[0.]
    with tf.variable_scope("", reuse=True):
        print(sess.run(tf.get_variable("v")))

with tf.Session(graph=g2) as sess:
    tf.initializer_all_variables().run()
    # 计算图g2中，v为1，因此输出为[1.]
    with tf.variable_scope("", reuser=True):
        print(sess.run(tf.get_variable("v")))
```  

**可以看出计算图隔离和张量和计算，另外还可以隔离设备，例如将加法跑在GPU上：**

```
g = tf.Graph()
#指定运行设备
with g.device("/gpu:0"):
    result = a + b
```
----
##### **2. 数据模型-张量**  
###### **2.1 张量的定义**
从功能上讲，张量可以被理解为多维数组，是TensorFlow管理数据的形式；其中零张量表示标量，即一个数；第一阶张量为向量(vector)；第n阶可以看出n维数组；**但是**张量在TensorFlow中的实现并不是直接采用数组模式，它没有保存具体的数字，**它保存的是如何得到这些数字的计算过程**  

```
In [7]: print(result)
# 保存的是张量的结构，add:0说明张量是计算节点"add"输出的第一个结果(编号从0开始)
Tensor("add:0", shape=(2,), dtype=float32)
In [8]: print(a)
# shape=(2,)说明是个一维数组，数组长度为2
Tensor("a:0", shape=(2,), dtype=float32)
In [9]: print(b)
Tensor("b:0", shape=(2,), dtype=float32)
In [10]:
```

可以看出：张量中主要保存了三个属性：名字(name)、维度(shape)和类型(type)
> 名字唯一标识符，并且给出这个张量是如何计算出来的；TensorFlow中的计算都可以通过计算图模型来建立，而计算图上的每个节点代表一个计算，计算的结果就保存在张量中，因此张量和节点一一对应

- 名字(name)通过"node:src_output"的形式给出，其中node代表**节点的名字**，src_output代表**当前张量来自节点的第几个输出**

- 维度(shape)描述一个张量的维度信息

- 类型(type)是张量的类型，每个张量有唯一类型，TensorFlow会对参与计算的所有张量进行类型检查，发现类型不匹配时，会报错

###### **2.2 张量的使用**  
**两大类：**  
- 对中间结果的引用，如上面代码中的a，b  
- 当计算图构造完成后，通过会话(session)来获得计算结果
----
##### **3. 运行模型-会话**
**计算图描述运算，张量组织数据，会话就是用来执行数据的**  
TensorFlow中的会话(session)执行定义好的运算，它拥有并管理TensorFlow程序运行时的所有资源；当计算结束以后，需要关闭会话来帮助系统回收资源，否则就可能会出现资源泄漏的问题

###### **3.1 使用会话的模式**
一种是明确调用会话生成函数和关闭会话函数,在这种模式中，如果程序异常退出，关闭session可能就不会执行而导致资源泄漏
```
sess = tf.Session()
sess.run(...)
sess.close()
```

通过python的上下文管理器使用会话
```
with tf.session() as sess:
    sess.run(...)
# 上下文件退出时自动完成会话关闭和资源释放
```

###### **3.2 会话其他知识点**
- 会话不能自动生成，需要手动指定，当默认会话被指定后，可以通过tf.Tensor.eval函数计算一个张量的取值
```
In [12]: sess = tf.Session()
    ...: with sess.as_default():
    ...:     print(result.eval())
    ...:     
[ 3.  5.]
In [13]: print(sess.run(result))  # 等价命令
[ 3.  5.]
In [15]: print(result.eval(session=sess))  # 等价命令
[ 3.  5.]
```
- 在命令行交互环境中，可以通过使用tf.InteractiveSession函数自动将生成的会话注册为默认会话
```
sess = tf.InteractiveSession()
print(sess.run(result))
sess.close()
```
- 使用ConfigProto可以配置需要生成的会话
