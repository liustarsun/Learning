# 1. 泛型编程基本概念
1. 什么是泛型编程？what
- 泛型就是通用型式，其**目的是**编写可重用的代码
- 编写不依赖于数据对象型式的代码就是泛型编程
- 泛型编程的基本工具是模板 ===> 引出模板

2. 为什么需要泛型编程？why
- 函数重载
- 相似类定义
- 型式兼容性

3. 如何实现泛型编程？how
- 模板 ===> 方式
- 型式参数化 ===> 这种是？？？

# 2. 泛型编程实践
1. 标准模板类 ===> STL
2. 泛型算法：函子与完美转发 ===> 基本概念是啥
3. 泛型数据结构：队列 ===> 数据结构
4. 泛型元编程：Fibonacci数列，素数枚举 ===> 啥叫元编程
5. 工程实践：事件机制 ===> C sharp里面的内容

685-694
# 3. 模板概述
- 过程式编程主要单元是函数，通过函数编写不依赖于特定值的算法，然后对函数进行重用
- 面向对象编程把数据和行为组织起来，但是并没有改变函数和方法参数化值的方式
- **模板**进一步利用了参数化的概念，不仅**值可以参数化**，**类型也可以参数化**
> 在C++中，**类型包括自定义类型** ===> 类型不定，用某种符号代替        

- 通过模板，不仅可以编写**不依赖于值的代码**，还可以编写**不依赖于类型的代码**，例如：可以编写一个堆栈的类定义，这个类定义可以用于任何类型
> 类还是原来的类，只不过类变量和类函数的参数类型不定

# 4. 类模板
主要应用于容器，或保存对象的数据结构；参数化数据成员，和成员方法      
```
// 类定义
template <typename T>  // 可以使用<class T>
class Grid
{
    public:
        Grid(size_t inWidth = kDefaultWidth, size_t inHeight = kDefaultHeight):m_a(inWidth), m_b(inHeight) ===> 不是不推荐使用默认值的吗
        {
            m_cells = new T*[m_width];
            for(size_t i = 0; i < m_width; ++i)
            {
                m_cells[i] = new T[m_height];
            }
        }

        // Grid<T> & 返回Grid<T>类型的引用，复制构造
        // 在定义模块的时候并没有指定模板要实例化的类型，因此必须使用一个占位参数T，这个T未来可能是任意类型
        Grid(const Grid<T>& src); 
        Grid<T>& operator=(const Grid<T> & rhs); // 赋值操作符重载
        virtual ~Grid();

        void setElementAt(size_t x, size_t y, const T & inElem);
        T & getElementAt(size_t x, size_t y);
        const T& getElementAt(size_t x, size_t y) const;
        
        size_t getHeight() const { return m_height};
        size_t getWidth() const {return m_width};

    protected:
        void copyFrom(const Grid<T>& src);

    private:
        static const size_t kDefaultHeight = 10;
        static const size_t kDefaultWidth = 10;

        // m_cells是动态分配的二维数组，===>因此需要重载一个const类型的const方法
        T** m_cells;
        size_t m_height;
        size_t m_width;
};

```
在类定义中，编译器会根据实际情况将Grid解析为Grid<T>，但是因为在类的外面**要表示这个模板产生的类型的时候需要使用这种语法**，因此最好养成**显式指定Grid**的习惯      
> 只有**构造函数**和**析构函数**应该使用Grid而不是Grid<T> ===> 构造/析构函数

模板要求把方法的实现也放在头文件的本身中，原因是：**编译器在创建模板之前需要知道完整的定义，包括方法的定义** ===> 实现也放在头文件中
> 在定义中，类名是Grid<T>，而不是Grid，在所有的方法和静态数据成员中，需要把**Grid<T>作为类名** ===> 构造析构例外

```
// 类实现
// 说明符号需要在每个方法的定义前面
template <typename T> ===> 考虑作用域的概念
Grid<T>::Grid(const Grid<T> & src)
{
    copyFrom(src);
}

template <typename T>
Grid<T>& Grid<T>::operator=(const Grid<T> & rhs)
{
    // check for self-assignment
    if(*this == rhs)
    {
        return *this;
    }

    // free old memory
    for(size_t i = 0; i < m_width; ++i)
    {
        delete[] m_cells[i]; ===> 考虑删除
    }

    delete[] m_cells;
    m_cells = nullptr; // 这个总是忘记，要记牢了 ===> 指针删除的概念不深刻

    // copy the new memory
    copyFrom(rhs);
    return *this;
}

template <typename T>
Grid<T>::~Grid() // virtual可带可不带？ ===> 类外定义时virtual不能带
{
    if (m_cells)
    {
        for (size_t i = 0; i < m_width; ++i)
        {
            delete[] m_cells[i];
        }

        delete[] m_cells;
        m_cells = nullptr; // 这个是在C++11中才有的空指针类型
    }
}


template <typename T>
void Grid<T>::setElementAt(size_t x, size_t y, const T & inElem)
{
    m_cells[x][y] = inElem;
}

template <typename T>
T & Grid<T>::getElementAt(size_t x, size_t y)
{
    return m_cells[x][y];
}

template <typename T>
const T& Grid<T>::getElementAt(size_t x, size_t y) const
{
    return m_cells[x][y];
}

template <typename T>
void Grid<T>::copyFrom(const Grid<T>& src)
{
    m_width = src.m_width;
    m_height = src.m_height;

    m_cells = new T *[m_width];

    for (size_t i = 0; i < m_width; ++i)
    {
        m_cells[i] = new T[m_height];
    }

    for (size_t i = 0; i < m_width; ++i)
    {
        for (size_t j = 0; j < m_height; ++j)
        {
            m_cells[i][j] = src.m_cells[i][j];
        }
    }
}

```
## 4.1 实例化模板类
在使用模板类的时候，需要指定这个Grid中保存的元素的具体的类型；**为某个特定的类型创建一个模板类的对象的过程称为模板的实例化**      

```
Grid<int> my_intGrid;
Grid<double> my_doubleGrid(11.0, 11.0);
my_intGrid.setElementAt(0, 0, 10);
int x = my_intGrid.getElementAt(0, 0);
Grid<int> grid2(my_intGrid);
Grid<int> another_intGrid = grid2;
```
## 4.2 注意事项    
1. 类型规范很重要，如下代码无法正常编译
```
Grid test; // 给出类似类模板的使用要求提供模板参数列表之类的错误
Grid<> test; //  给出模板参数数目错误
```
- 如果要声明一个方法或函数，接收Grid类型的参数，则需要指定具体的类型
```
void processIntGrid(Grid<int> & intGrid)
{
    //
}

```

2. 为了避免每次都编写完整的Grid类型名称，如Grid<int>，可以使用typedef
```
typedef Grid<int> intGrid

void processIntGrid(intGrid & otherIntGrid){}
```

3. Grid模板可以保存自定义类型的数据
```
Grid<SpreadsheetCell> mySpreadsheet; // 实例化SpreadsheetCell

Grid<char *> myStringGrid; // 实例化char *类型

Grid<vector<int> > // 实例化vector<int>类型

Grid<int> *myGridp = new Grid<int>(); // 在堆上动态分配
myGridp->setElementAt(0, 0, 10);
```


# 5. 编译器处理模板的原理
1. 当编译器遇到模板时，会**进行语法检查**，编译器无法编译模板，因为不知道要使用的类型是什么
2. 当编译器遇到一个实例化模板时，会将模板中的T，替换为具体的类型，如int    
3. 编译器生成代码的方式就像写非模板程序一样，为每个类型编写一个不同的类，如果程序中没有将类模板实例化为任何类型，那么**类方法也不会被编译**===>没有指明实际替换类型的方法不会被编译 ===> 这个是重点    
4. 实例化过程也解释了为何需要在定义中多个地方使用Grid<T>语法，当编译器为某个特定类型实例化模板的时候，编译器将T替换为int，使得Grid<int>称为类型     

## 5.1 选择性实例化
-编译器只为调用的类方法生成代码 ===> 调用哪个方法，为哪个方法生成代码
```
int main()
{
    Grid<int> my_intGrid;
    my_intGrid.setElementAt(0, 0, 10); // 只会为这个方法生成代码，其他的如copy构造函数，赋值操作符等方法，编译器不会为其生成代码
    return 0;
}
```

## 5.2 模板对类型的要求
- 如果某个类型不支持模板的某些方法，那么在**在模板实例化的时候，不要调用那些类型不支持的方法**，能这样做的原因就是因为**选择性实例化**


# 6. 模板代码分布
一般情况，会把类定义在.h文件中，把方法定义在.cc文件中，创建或使用类对象的代码通过#include来包含.h文件，并通过**链接器的作用**访问这些方法代码      

**但是**模板不能安装这种方法，由于编译器需要通过"模板"为实例化类型生成**实际的方法代码**，因此在**任何使用了模板的源代码中，编译器都应当能够同时访问到模板类定义和方法定义**，所有：   

1. 把模板定义放在头文件中，包括方法定义和类定义
- 把模板方法定义在**另一个头文件中**，然后在类定义的头文件中，#include这个头文件，而且要保证方法定义的#include在类定义之后，否则代码无法编译
```
// Grid.h
template <typename T>
class Grid
{

};

#include "GridDefinitions.h"  // 包含方法定义的头文件
```
需要使用模板的客户只要#include "Grid.h"文件即可; **这种分发有助于分开类定义和方法定义**

2. 把模板定义放在源文件中
```
// Grid.h
template <typename T>
class Grid
{

};

#include "GridDefinitions.cc"  // 包含方法定义的源文件

```

> C++11之前通过export关键字指定模板定义可以应用于所有编译单元，但是C++11中不允许这样做===>区别            


# 7. 模板参数
编写类模板时，可以在<>中指定模板的参数列表，和函数/方法一样，参数列表可以有多个，也可以有默认值，而且参数列表不一定都是类型       

## 7.1 非类型参数
非类型的模板参数的类型只能是**整数类型**(char, int, long...)、**枚举类型**，**指针和引用**，如使用**非类型模板参数**指定网格的高度(kDefaultHeight)和宽度(kDefaultHeight)
```
// 类模板定义
template <typename T, size_t WIDTH, size_t HEIGHT>
class Grid
{
    public:
        size_t getHeight() const 
        {
            return HEIGHT;
        }

        size_t getWidth() const
        {
            return WIDTH;
        }

    private:
        T m_cells[WIDTH][HEIGHT];
}；
```

**在上述定义的class中，模板参数列表有3个，这类中没有动态内存分配，因此不需要用户自定义copy构造，析构函数和赋值运算符，甚至不需要默认构造函数，使用缺省的就可以了**===>自定义那几个函数的情况            

```
// 方法实现
template <typename T, size_t WIDTH, size_t HEIGHT>
void Grid<T, WIDTH, HEIGHT>::setElementAt(....)  // 此时类为Grid<T, WIDTH, HEIGHT>
{
    ....
}

```

### 局限性===>不能使用非常量整数指定WIDTH和HEIGHT
```
int height = 10;
Grid<int, 10, height> my_intGrid; // 错误

// 需要替换为
const int height = 10;
```
Grid<int, 11, 12>和Grid<int, 10, 9>是两个类型，两种不能相互传递或者赋值等===>模板类+参数类型，是一体     

## 7.2 非类型化参数默认值
可以为非类型化参数提供默认值
```
// 类定义
template <typename T, size_t WIDTH = 10, size_t HEIGHT = 10>
class Grid
{
    ......
};
```
// 方法定义中，不需要再写默认参数 ===> 啥时候写，啥时候不写，整理一下      
```
template <typename T, size_t WIDTH, size_t HEIGHT>
void Grid<T, WIDTH, HEIGHT>::setElementAt(size_t x, size_t y, const T & inElem)  // 此时类为Grid<T, WIDTH, HEIGHT>
{
    m_cells[x][y] = inElem;
}


// 实例化, 以下三种都可以，但是理论上不推荐
Grid<int> myGrid;
Grid<int, 10> another_intGrid;
Grid<int, 10, 10> aThirdGrid;
```
**模板参数列表和函数方法一样，可以从右到左提供参数的默认值**===>和参数传递的顺序一致     

# 8. 方法/函数模板
C++允许模板化类中的单个方法，这些方法可以在一个**类模板中**，也可以在**非模板化的类中**       
在类模板中，方法模板对**赋值运算符**和**复制构造函数**非常有用     
> **不能用方法模板编写虚函数和析构函数**

### 考虑：
```
Grid<int> my_intGrid;
Grid<double> my_doubleGrid;
```
两者是不同类型，即使int可以强制类型转换为double，两者也不能互相赋值，最根本的原因在于operator的原型为：
```
Gird(cosnt Grid<T> & src);
Grid<T> & operator=(const Grid<T> & rhs);
```
在实例化的时候，两者只能选择其一，因此可以修改为如下**方法模板**

```
template <typename T>
class Grid
{
    public:
        ......

        Grid(const Grid<T> &src); // 普通方法
        
        template <typename E>     
        Grid(const Grid<E> &src); // 方法模板

        Grid<T> & operator=(const Grid<T> &rhs); // 普通方法

        template <typename E>;
        Grid<T> & operator=(const Grid<E> &rhs); // 只是参数类型，返回值还是要是Grid<T>类型
};

```
### 注意:
1. 方法模板并不会替换**普通方法**，这条规则会导致copy构造函数和operat=的问题 ===> 这是规制       
2. 如果编写两者的方法模板并忽略普通方法，则编译器在给同样类型的Grid赋值时就不会调用这些新的方法模板版本，而会生成缺省的版本进行操作，因此要保留**普通方法版本**===> 缺省的啥都不做      

```
// 实现 ===> 两重前缀
template <typename T>  // 类模板
template <typename E>  // 方法模板
Grid<T>::Grid(const Grid<E> &src)
{
    copyFrom(src);
}

```

在模板operator=中不需要检查自赋值，因为自赋值用的是**普通的operator=版本**，因此在方法模板中不可能自赋值===> 模板方法不能自赋值      

# 9. 模板特例化