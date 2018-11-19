# 1. static
编译时的语法检测行为?===>C++反汇编中有个位置代表是不是static，如果是的话，就不会再初始化      

## 1.1 C中===>控制存储方式和可见性(作用域)    
### 1. 修饰的变量保存在内存的静态区==>只要是静态的变量都是保存在静态区(存储放式)
**静态全局变量**：作用域限制在定义之处开始，到当前文件结尾处结束，其他文件使用extern声明也不能使用              
**静态局部变量**：作用域限制在函数体中，因static修饰的变量总是存储在静态区，因此下次进入函数，仍然可以使用上次的值        

### 2. 修饰函数称为静态函数
此时static**不代表存储方式**，而是指对函数的作用域局限于本文件(**内部函数**)；目的是为了防止和其他文件中的函数同名      

## 1.2 C++中===>除了上面的两个，多了修改类内变量和类内方法    

### 1. static类的变量
1. 声明：static int a; ===> 属于类
2. 只声明，不在对象上分配空间 ===> 保存在静态存储区
3. 定义==> int B::a = 10; ===> 在类外定义**一定不能加static**
4. 必须在外部初始化，**初始化动作和访问控制无关** ===> **不能在初始化列表中初始化，不能在定义处初始化**
> 初始化的时候**不能再带有关键字static**

```
// 直接在类定义处初始化static会出现如下问题
 error: ISO C++ forbids in-class initialization of non-const static member 'A::m_c'
         static int m_c = 100;

```

## 4.5 static类函数
1. 使用**类调用**，不使用对象调用
2. 目的是访问类的static数据成员，若要访问非static数据成员，**必须指定对象或者指向对象的指针===>之所以有static类函数，是为了要访问static类变量**

------
# 2. const
```
const int Max = 100; // 在定义的时候需要初始化，因为是readonly类型的变量
int array[Max];  // 在c语言中也没有出错
int array[Max] = {0};  // 在c语言中出错，因为并不知道Max的值

// C++中编译器通常不为普通的const只读变量分配存储空间，而是把它们保存在符号表中，使得它成为一个编译期间的值，没有了存储于读内存的操作
        const int a = 1000;
        #define M 3   // 预处理阶段替换
        int i = a;
        int I = M;
        int j = a;
        int J = M;

// C语言反汇编 
        pushl   %ebp
        movl    %esp, %ebp
        subl    $32, %esp
        movl    $1000, -20(%ebp)   
        movl    -20(%ebp), %eax    // 区别 ===> C编译阶段不替换
        movl    %eax, -16(%ebp)
        movl    $3, -12(%ebp)
        movl    -20(%ebp), %eax
        movl    %eax, -8(%ebp)
        movl    $3, -4(%ebp)
        leave  
        ret


// C++反汇编代码
        pushl   %ebp
        movl    %esp, %ebp
        subl    $32, %esp
        movl    $1000, -20(%ebp)  // ===> 编译阶段替换const的值
        movl    $1000, -16(%ebp)
        movl    $3, -12(%ebp)
        movl    $1000, -8(%ebp)
        movl    $3, -4(%ebp)
        movl    $0, %eax
        leave
        ret
```

## 2.1 C中
**const修饰的量是只读(readonly)的变量，其值在编译时不能被使用**==>因为编译器在编译的时候不知道其存储的内容 ===> 在运行时替换？？       
> 不是编译期替换的    

## 2.2 C++中
C++提供两种和**常量**相关的概念：
1. constexpr：编译时求值，把数据放在只读内存中，从而提升性能    
2. const：在当前作用域内，我承诺不修改这个值，即值不会发生改变；通常规定接口的不可修改性    
3. 如果某个函数用在常量表达式中，即表达式在编译时候求值，则函数必须定义为constexpr
```
constexpr double square(double x) {return x*x;}
```
4. 如果想定义成constexpr，则函数体要非常简单：即函数只能有一个计算某个值的return语句
5. constexpr函数可以接收**非常量实参**，但此时**结果将不是一个常量表达式**；当程序上下文不需要常量表达式的时候，可以用非常量表达式的实参调用constexpr函数；从而就不用把同一个函数定义两次了：一个用于常量表达式，一个用于变量

**在编译的时候把const类型的变量替换为值**==>代表修饰的是常量===>理解有问题？？  
**C语言中const修饰的是readonly的变量，这些只读变量不能作为定义数组的维数，也不能放在case关键字后面，但是C++可以**

## 2.3 修饰各种类型
### 普通变量   
```
const int i = 10;    
int const i = 10;    
```

### 数组 
```  
const int a[10] = {1};   ===> 两者相同，没有初始值的默认为0
int const a[10] = {1};   ===> 和上面相同
```

### 指针===> 把类型去掉来判断，const *(指向值不变) 还是 * const(本身地址不变)
```    
const ~~int~~ *p; // p(地址)可变，p指向对象不可变    
~~int~~ const *p; // p(地址)可变，p指向对象不可变    

~~int~~ *const p; // p不可变，p指向对象可变     
const ~~int~~ *const p; // 都不可变     
~~int~~ const *const p; // 都不可变     
```

### 修饰函数的参数，函数返回值
```
const int Fun(const int *p);
```

### const char*类型赋值给char*类型
使用**strcpy**, 直接复制则会更改同一块内存位置的属性        


## 2.4 const数据成员
1. 值在运行期间不可变===>编译期有没有被替换掉?
2. 只能在构造函数**初始化列表**中初始化===> 正确,const成员不能赋值
```
// C++11以后，const数据成员可以在类定义中直接出示，
 warning: non-static data member initializers only available with -std=c++11 or -std=gnu++11
         const int m_a = 10;===>否则只能在构造函数初始化列表中初始化

```

## 2.5 const成员函数
1. 定义void hello(int a, int b) const; ===>这个是声明，保证不会修改类成员变量
2. 不能修改对象成员的值，在定义的时候**const不能省略，要写**===>在类外面定义类方法
3. 不能调用类中**非const成员函数**，因为如果可以调用，就可以修改成员了===>不能在其内部调用其他的非const类方法
4. static成员函数**不能定义**为const成员函数, 为什么呢？===>因为static成员函数属于类的，没有this指针===>CV限定符的问题
5. const成员只能调用const成员函数，**非const成员对象，可以调用const成员函数**===>还是关于是不是修改const属性的值的问题    

```
// 如果定义了构造函数，则需要初始化const成员变量===>因为在C++11之前const成员必须在初始化列表中初始化
 error: uninitialized const member in 'const int' [-fpermissive]
         A(){};
         ^
const_static_class.cc:11:19: note: 'const int A::m_a' should be initialized
         const int m_a;

```
------
# 3. const static
## 3.1 const static类的变量
1. 值在程序运行期间不可变，且只有唯一副本
2. 声明：static const int a; ===> 只能在类中定义的时候进行初始化，或者在类外面初始化，但是**const不能省略** ===>有些不能加，有些必须加

```
// 直接在定义处进行初始化
    private:
        const int m_a;
        static const int m_b  = 0;

// 在类外通过定义：
const int A::m_b = 10; // 这种方式也可以初始化const int类型的成员，好神奇的东西，这个时候通过类直接访问 ===> static不能加，const必须加
```

## 3.2 const static类的函数===>会报错，不存在

```
// 定义为const成员函数的时候会出现以下问题，因为static成员函数没有this指针
error: static member function 'static int A::f_c()' cannot have cv-qualifier
  static int f_c() const; ===> 不能同用

// 和volatile也不能同用
error: static member function 'static int A::f_c()' cannot have cv-qualifier
  static int f_c() volatile ; ===>不能同用
```

**在const volatile修饰的变量中，volatile起作用===>也就是不会在编译期就替换掉了**    