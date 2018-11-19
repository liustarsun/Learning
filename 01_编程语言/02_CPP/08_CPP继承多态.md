# 1. 继承
1. **派生类**继承了基类的**所有属性和方法**，包含**私有属性**，但是派生类**不能访问**私有属性和方法===>私有的被隐藏起来了?
2. 派生类可以增加新的属性和方法===>扩展

## 1.1 单继承语法格式
```
class  Derived : public/private/protected Base
{

};
```
1. **public**===>**基类**的protected，public成员在派生类中保持，private成员在派生类中不可以见(**属于基类隐私**)
2. **protected**===>**基类**的protected和public在派生类中都是**protected**，private不可见
3. **private**===>**基类**的protected和public在派生类中都是**private**，private不可见
> 设计类时，若要使用继承机制，建议将派生类需要频繁使用的基类数据成员设为**protected**

## 1.2 函数覆盖
派生类中成员函数和基类相同的，基类的会被覆盖掉，使用派生类调用的是派生类中的成员函数

## 1.3 多继承
多继承会导致派生类中可能包含多个基类副本

## 1.4 虚拟继承
1. 虚继承的目的是为了取消多重继承时派生类中公共基类的多个副本，只保留一份，使用virtual ===> virtual public base??
```
// 找份代码看看

```

# 2. 多态性
1. 目的：**不同对象**在接收到相同消息时，作出**不同响应**
2. 现象：对应同样成员函数名称，执行不同函数体
3. 实现：使用virtual声明成员函数
4. 声明：virtual 返回值 成员函数名(参数列表);

## 2.1 纯虚函数
1. 充当占位函数，没有任何实现
2. **派生类负责实现其具体功能**
3. 声明：virtual void f(void *) = 0;  和虚函数的区别在于(=0)

## 2.2 抽象类
1. 带有**纯虚函数的类**
2. 作为类继承层次的上层
3. 保持多态性需要**虚析构函数**，以保证能够正确**释放对象**===>虚析构函数   

```
#include <iostream>
using namespace std;
  
class Empty
{};
  
class Derived1 : public Empty
{};
  
class Derived2 : virtual public Empty ===> 虚继承
{};
  
class Derived3 : public Empty
{    
    char c;
};
  
class Derived4 : virtual public Empty
{
    char c;
};
  
class Dummy
{
    char c;
};
  
int main()
{
    cout << "sizeof(Empty) " << sizeof(Empty) << endl;   // 1byte
    cout << "sizeof(Derived1) " << sizeof(Derived1) << endl;  // 1byte
    cout << "sizeof(Derived2) " << sizeof(Derived2) << endl;  // 4byte
    cout << "sizeof(Derived3) " << sizeof(Derived3) << endl;  // 1byte
    cout << "sizeof(Derived4) " << sizeof(Derived4) << endl;  // 8byte    
    cout << "sizeof(Dummy) " << sizeof(Dummy) << endl;        // 1byte   不要想太多，因为只有一个数据类型所以没有对齐要求 ===> 只有一个类型不需要对齐
  
    return 0;
}
```
