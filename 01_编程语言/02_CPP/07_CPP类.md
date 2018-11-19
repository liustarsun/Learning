# 1. 类和对象
类是抽象，对象是具体实现，使用C++filter反汇编出函数名字      

# 2. 类
类是属性和行为的统一，它实现了数据封装和信息隐藏，如果没有类的概念，则**无法定义非指针量**      

```
// 类声明
class A; // 只是声明了类的存在，没有提供任何细节

// 类定义
class A
{
public: // 关键字顺序任意
    // 成员可以是函数和数据
    成员类型 成员名;
protected:
    成员类型 成员名;
private:    
    成员类型 成员名;
};

```

类类型声明**仅用于函数原型中**，不可以用来定义类的数据成员，因为**类定义的时候要分配空间大小，此时需要所有的数据成员都是确定的类型**      
空类类型大小为1，**是为了保证定义两个不同对象的时候有不同的地址**===>有的可不是1    

## 2.1 空struct之c
```
root@8691524eec08:~/c++# cat test_class.c
#include <stdio.h>

struct A {};
int main()
{
    printf("The sizeof struct is %d\n", sizeof(struct A));  // 0, struct A不可以分开写 ===>空struct是0
    return 0;
}
root@8691524eec08:~/c++# 

// 对应汇编
080483db <main>:
 80483db:       55                      push   %ebp
 80483dc:       89 e5                   mov    %esp,%ebp
 80483de:       b8 00 00 00 00          mov    $0x0,%eax  // sizeof的大小在编译期间就计算出来了, 直接输出？ ===> sizeof是在编译期计算的

 80483e3:       5d                      pop    %ebp
 80483e4:       c3                      ret

```
## 2.2 空类之c++
```
// 源代码
#include <iostream>
using namespace std;

struct AA
{

};

class A
{
public:
    A(){};
private:
    int m_a;
    char *m_p;
    char m_c;
    bool m_d;
};

class B
{
public:
    B(){};
private:
    int m_a;
    bool m_b;
    char *m_p;
    char m_c;
};

class C
{

};

int main()
{

    int a = sizeof(A);
    int b = sizeof(AA);
    int c = sizeof(B);
    int d = sizeof(C);
    
    return 0;
}

// 对应汇编
main:
        pushl   %ebp
        movl    %esp, %ebp
        subl    $16, %esp
        movl    $12, -16(%ebp)  // A，4字节对齐
        movl    $1, -12(%ebp)   // AA 空struct为1 ===> 和C不一样
        movl    $16, -8(%ebp)   // B  4字节对齐
        movl    $1, -4(%ebp)    // C  空class为1
        movl    $0, %eax
        leave
        ret
```

# 3. 对象
可以像结构体一样定义和使用对象及其公开的成员，而私有成员不可在**类的**外部直接访问，即使**对象也不可以访问private变量**
> 结构体默认是**public**，class默认是**private**的

## 3.1 对象构造   
构造就是初始化，在定义对象的时候初始化它的数据成员; 在C++中使用**构造函数**给对象初始化===>定义对象时自动调用构造函数

### 3.1.1 构造函数特点
1. 和类类型同名，没有返回值类型(包括不能使用**void**类型)     
2. 允许重载
3. 可以带缺省参数，但是不建议，因为会混淆参数的个数===>不建议
4. 至少公开一个构造函数，除非不在外面定义对象===>private在类的外部不能访问
5. 只能由系统创建对象时自动调用，程序其他部分不能直接调用===>不能手动调用      

### 3.1.2 缺省构造函数    
1. 系统自动产生，自动调用  
2. 无参数，且函数体中没有任何语句===>啥也不干
3. 如果定义任意一个构造函数，则不再生产缺省构造函数===>C++11中的default关键字
4. **函数有{}为定义，没有的是声明**，区分函数的定义和声明===>区分函数的定义和声明

### 3.1.3 copy构造函数
1. 用于构造**已有对象副本** ===>定义
2. 参数为本类**常量对象**的引用 ===> 不能修改copy的那个对象
3. 如果未定义，系统产生一个缺省copy构造函数 ===>有个缺省的，也是啥都不干?
4. 对应含有**指针**的类，需要自定义copy构造函数进行**深copy**，缺省copy构造函数只进行**浅copy**===>类里面有指针类型的时候，注意深浅copy问题

### 3.1.4 构造函数的初始化列表
1. 在构造对象时，同步构造内部对象===>给对象的成员使用()进行初始化
2. 部分成员(**常量和引用**)，只能初始化，不能赋值===>只能在初始化列表中初始化
3. 部分成员(类的对象)如果赋值，将导致两次构造===>提高效率，调用其他类对象的构造函数
> 在分配内存时，调用缺省构造函数构造，然后执行构造函数内的复制语句时再次构造，效率不佳；**如果类没有缺省构造函数，就会导致问题**

4. 成员初始化按照成员**定义顺序**，而不是初始化列表顺序，因此保持初始化列表和成员定义的顺序一致性===>即成员的定义顺序
5. 初始化列表使用在构造函数实现中，声明中不可以使用===>指的是构造函数

### 3.1.5 析构函数
1. 析构就是终止化，在对象生命周期结束时清除它===>可以直接调用
2. 和类类型同名，前面带有~记号，无参数，无返回值类型(**同样不能使用void**)
3. 必须是公开的，否则无法调用===>public的才可以在类外部进行调用
4. 可以由系统在销毁对象时自动调用，也可以由程序其他部分直接调用，两者工作原理不同
5. 每个类只能有一个析构函数，若未定义，则系统自动生成一个缺省析构函数，该函数无代码===>啥也不干
6. 析构函数的目的是为了释放动态分配的内存===>释放new或者是malloc申请的内存

# 4. 类和对象成员
## 4.1 内联函数
1. 为了进行程序优化，展开函数代码而不是调用===>没有调用栈，编译期就展开，实现在头文件中？？
2. 在函数**定义**前添加**inline**关键字，如果**仅仅只是在函数声明前使用**则无效===>定义和声明的时候要加inline关键字      
3. 编译器必须能看见内联函数的代码才能**在编译期**展开，因此**内联函数必须实现在头文件中**
4. **类定义**中给出**函数体的成员函数**会**自动成为内联函数**===>构造和析构是因为7才没有成内联函数??
5. 函数代码量较大，或者包含循环，则不要使用内联
6. 构造函数和析构函数有可能隐含附加操作，**慎用内联**
7. 内联函数仅仅是建议，编译器会自主选择是否内联===>这个是重点

## 4.2 const数据成员
1. 值在运行期间不可变===>编译期有没有被替换掉?
2. 只能在构造函数**初始化列表**中初始化===> 正确,const成员不能赋值
```
// const数据成员可以在类定义中直接出示，是在C++11以后才可以的
 warning: non-static data member initializers only available with -std=c++11 or -std=gnu++11
         const int m_a = 10;===>否则只能在构造函数初始化列表中初始化

```

## 4.3 const成员函数
1. 定义void hello(int a, int b) const; ===>这个是声明，保证不会修改类成员变量
2. 不能修改对象成员的值，在定义的时候**const不能省略，要写**===>在类外面定义类方法
3. 不能调用类中**非const成员函数**，因为如果可以调用，就可以修改成员了===>不能在其内部调用其他的非const类方法

4. static成员函数**不能定义**为const成员函数, 为什么呢？===>因为static成员函数属于类的，没有this指针

5. const成员只能调用const成员函数，**非const成员对象，可以调用const成员函数**===>还是关于是不是修改const属性的值的问题    

```
// 定义为const成员函数的时候会出现以下问题，因为static成员函数没有this指针
error: static member function 'static int A::f_c()' cannot have cv-qualifier
  static int f_c() const; ===> 不能同用

// 和volatile也不能同用
error: static member function 'static int A::f_c()' cannot have cv-qualifier
  static int f_c() volatile ; ===>不能同用

// 如果定义了构造函数，则需要初始化const成员变量===>因为在C++11之前const成员必须在初始化列表中初始化
 error: uninitialized const member in 'const int' [-fpermissive]
         A(){};
         ^
const_static_class.cc:11:19: note: 'const int A::m_a' should be initialized
         const int m_a;

```

## 4.4 static类变量
1. 声明：static int a; ===> 属于类
2. 只声明，不在对象上分配空间 ===> 保存在静态存储区
3. 定义: int B::a = 10; ===> 在类外定义**不能加static**
4. 必须在外部初始化，**初始化动作和访问控制无关** ===> 不能在初始化列表中初始化，不能在定义处初始化
> 初始化的时候**不能再带有关键字static**
```
// 直接在类定义处初始化static会出现如下问题
 error: ISO C++ forbids in-class initialization of non-const static member 'A::m_c'
         static int m_c = 100;

```

## 4.5 static类函数
1. 使用**类调用**，不使用对象调用
2. 目的是访问类的static数据成员，若要访问非static数据成员，必须**指定对象**，或者**指向对象的指针** ===>之所以有static类函数，是为了要访问static类变量

## 4.6 const static类变量
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

# 5. 访问属性
private属性的类变量，即使是本类定义的对象也不能访问
```
// 本类的也不能访问
error: 'const int A::m_a' is private
         const int m_a;

error: within this context
     cout << bb.m_a << endl;

```

# 6. 友元函数和友元类
**友元会破坏类数据的封装和信息的隐藏， 因此慎用**
1. 类的友元可以访问该**类对象的私有和保护成员** ===> 可以访问private类变量和类函数
> 类对象有区分私有和保护成员吗？===>如果是类定义一个对象，是不可以访问类的私有成员的
2. 友元可以是函数，**其他类**成员函数，或者其他类
3. 定义: friend 函数或类声明;
4. 友元关系不可逆，除非互为友元
5. 函数中传递类对象通常使用引用传递(&)
```
#include <iostream>
using namespace std;

class A
{
    public:
        A():m_a(30){};


    private:
        friend class B;
        int m_a;
};

class B
{
    public:
        int get_value(A& a)
        {
            return a.m_a;
        }
};

int main()
{
     A a;
     B b;
     cout << b.get_value(a) << endl;   // 放到函数可以访问===>这个实际也是神奇的
//     cout << a.m_a << endl;  // 直接不能访问 ===>这个会报错
     return 0;
}
```

------
# 7. 
extern关键字，两种用法
	1. 单纯的声明某个变量，如果在声明的时候被定义，则extern关键字自动忽略
	► external.h文件：
	extern int a;      // 单纯的声明
	extern int a = 10;    // 属于定义，编译时会有warning产生
	► external.cc文件：
	如果是单纯的声明，则需要重新定义，格式为：
	int a = 1000；
	如果已经定义，则直接使用，不可以重新定义
	a = 1000；
	
	2. extern "C"  // 大写的"C"
	代表按照C编译器的风格进行链接，但是语法还是要遵从C++的语法
结构体初始化
struct linux_binfmt {
	struct list_head lh;
	struct module *module;
	int (*load_binary) (struct linux_binprm *);
	int (*load_shlib) (struct file *);
	int (*core_dump) (struct coredump_params *cprm);
	unsigned long min_coredump; 
};

	1. 第一种方式，常用于内核中的初始化，成员初始化顺序可变
	static struct linux_binfmt elf_format = { 
		.module = THIS_MODULE, 
		.load_binary = load_elf_binary, 
		.load_shlib = load_elf_library, 
		.core_dump = elf_core_dump, 
		.min_coredump = ELF_EXEC_PAGESIZE, 
	};
	2. 第二种方式，成员初始化顺序可变，老版本非标准的初始化形式，可能已经废弃？
	static struct linux_binfmt elf_format = { 
		module : THIS_MODULE, 
		load_binary : load_elf_binary, 
		load_shlib: load_elf_library, 
		core_dump: elf_core_dump, 
		min_coredump: ELF_EXEC_PAGESIZE, 
	};
	3. 第三种方式，初始化顺序不可变
	static struct linux_binfmt elf_format = { 
		THIS_MODULE, 
		load_elf_binary, 
		load_elf_library, 
		elf_core_dump, 
		ELF_EXEC_PAGESIZE, 
	};
------
# 8. 构造函数为什么不能是虚函数
1. 从存储角度看，虚函数对应一个指向vtable虚函数表的指针，指向vtable的指针实际上保存在**对象内存空间的**，如果构造函数是虚的，则就需要通过vtable来调用，但是对象还没有实例化，也就是内存空间还没有，因此找不到vtable，所以构造函数不能是虚函数
2. 从实现来看vtable在构造函数调用后才建立的
3. 从实际含义来看，在调用构造函数时，还不能确定对象的真实类型(因为子类会调用父类的构造函数)；而且构造函数的作用是初始化对象(也就是类的变量)，在对象生命周期只执行一次，不是对象的动态行为，也没有必要成为虚函数
