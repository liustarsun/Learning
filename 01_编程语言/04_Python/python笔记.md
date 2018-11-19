# **python笔记**

## **python基础语法**

### **字符串 String**

1.使用三引号用来输入包含多行文字的字符串
```
In [9]: s = ''' hello
   ...: world'''

In [12]: print(s)
    hello
   world   
```
2.字符串的分割
```
In [13]:  s = "hello world"
In [14]: s.split()
Out[14]: ['hello', 'world']
In [15]:
```
---
### **列表 List**
> 列表通过[]生成

1.添加元素
```
In [16]: a = ["a", 3, 8, "b"]

In [17]: a
Out[17]: ['a', 3, 8, 'b']

In [18]: a.append("world")

In [19]: a
Out[19]: ['a', 3, 8, 'b', 'world']
```
2.删除列表
```
In [24]: del(a)

In [25]: a
---------------------------------------------------------------------------
NameError                                 Traceback (most recent call last)
<ipython-input-25-60b725f10c9c> in <module>()
----> 1 a

NameError: name 'a' is not defined

In [26]:
```
---
### **集合 Set**
> 使用{}生成集合，集合不包含重复的元素，集合的key不能修改

```
In [26]: s = {4, 5, 6, "hello"}
In [29]: s.add(3)
In [30]: s
Out[30]: {'hello', 3, 4, 5, 6}
In [31]: s.add(4)
In [32]: s
Out[32]: {'hello', 3, 4, 5, 6}
```

> 集合操作，交集&，并集|, 差集-，对称差^

```
In [33]: a = {1, 3, 4, 5}
In [34]: b = {2, 3, 4, 6}
In [35]: a&b // 交集
Out[35]: {3, 4}
In [36]: a|b // 并集
Out[36]: {1, 2, 3, 4, 5, 6}
In [37]: a-b // 差集
Out[37]: {1, 5}
In [38]: b-a // 差集
Out[38]: {2, 6}
In [39]: a^b  // 对称差
Out[39]: {1, 2, 5, 6}
```
---
### **字典 Dictionary**
> 通过{key:value} 生成

```
In [40]: d = {'dogs':1, "cat":2, "pigs":3}
In [41]: d
Out[41]: {'cat': 2, 'dogs': 1, 'pigs': 3}
In [42]: d["targes"] = 5
In [43]: d
Out[43]: {'cat': 2, 'dogs': 1, 'pigs': 3, 'targes': 5}
In [44]: d["cat"] = 22
In [45]: d
Out[45]: {'cat': 22, 'dogs': 1, 'pigs': 3, 'targes': 5}
In [46]: d.keys() // 键
Out[46]: dict_keys(['dogs', 'cat', 'pigs', 'targes'])
In [47]: d.values() // 值
Out[47]: dict_values([1, 22, 3, 5])
In [48]: d.items() // 所有键值对
Out[48]: dict_items([('dogs', 1), ('cat', 22), ('pigs', 3), ('targes', 5)])
In [49]:
In [49]: del(d["dogs"])  // 删除键值对
In [50]: d
Out[50]: {'cat': 22, 'pigs': 3, 'targes': 5}
In [51]:
```
---
### **数组 Numpy Arrays**
> 需要先导入包，Numpy数组可以进行很多列表不能进行的运算

```
In [51]: from numpy import array

In [52]: a = array([1, 2, 3, 4])

In [53]: a
Out[53]: array([1, 2, 3, 4])

In [54]: a ** a
Out[54]: array([  1,   4,  27, 256])

In [55]: a + a
Out[55]: array([2, 4, 6, 8])

In [56]: a
Out[56]: array([1, 2, 3, 4])

In [57]: a - a
Out[57]: array([0, 0, 0, 0])

In [58]: a + 2
Out[58]: array([3, 4, 5, 6])
```
---
### **画图Plot**
```
PASSED
```
---
### **常用函数**
```
In [63]: a = 1+2j
In [64]: type(a)
Out[64]: complex
In [65]: a.real  // 查看实部
Out[65]: 1.0
In [68]: a.imag  // 查看虚部
Out[68]: 2.0
In [2]: a.conjugate() // 共轭
Out[2]: (1-2j)
```
---
### **优先级**
+ ()括号
+ **幂指运算
+ \* / // % 乘、除、整数除法，取余运算
+ \+ \- 运算
---
## **字符串方法: 返回的是新的字符串**
### **分割**
> s.split()将s按照空格（包括多个空格，制表符\t，换行符\n等）分割，并返回所有分割得到的字符串（列表）

```
In [3]: line = "hello world"
In [4]: line.split()
Out[4]: ['hello', 'world']
In [5]:
```
> s.split(sep)以给定的sep为分隔符对s进行分割

 ```
In [6]: line = "hello+world"  // +号
In [7]: line.split("+")  // 以+号进行分割
Out[7]: ['hello', 'world']
In [8]:
 ```

### **连接**
> s.join(str_sequence)的作用是以s为连接符将字符串序列str_sequence中的元素连接起来，并返回连接后得到的新字符串

```
In [14]: s="-"
In [15]: s.join(numbers)
Out[15]: 'hello-world'
```
### **替换**
> s.replace(part1, part2)将字符串s中指定的部分part1替换成想要的部分part2，并返回新的字符串

```
In [16]: s = "hello world"
In [17]: s.replace("world", "python")
Out[17]: 'hello python'
```

### **格式字符串**
> 用字符串的format()方法来格式化字符串,同旧式的%方法一样

---
## **元组**
> 元组单个元素的生成比较特殊,可以通过tuple(a)方法转换为元组

```
In [21]: a = (10,)
In [22]: a
Out[22]: (10,)
In [23]: type(a)
Out[23]: tuple
```
