# 1. STL算法
1. 提供大量的泛型数据结构
2. 泛型编程就是**不依赖于类型的编程**，主要实现方式是**模板**
3. 大量的泛型算法大部分(少数部分例外)都可以应用于任何容器元素，通过这些算法可以在容器中查找、排序和处理元素，并执行大量其他的操作
4. 算法之美在于算法不仅独立于底层元素的数据类型，还独立于操作的容器类型，**算法仅使用迭代器接口执行操作**===>**迭代器是一种类型**
5. 大部分算法都接受回调(callback)，回调可以是**函数指针**，也可以是**行为上类似于函数指针的对象**；为了提供方便，STL还提供了一组**可用于创建算法使用的回调对象的类**，这些回调对象称为**函数对象或者仿函数(functor)**===>回调类生成的对象

# 2. 基本概念
## 2.1 核心思想
1. 算法通过**迭代器**作为中介操作容器，并不直接作用于容器本身
2. **通过这种方式，算法没有绑定到特定的容器实现**
3. 所有的算法都实现为**函数模板的形式**，其中模板的类型参数**一般都是迭代器**，迭代器被指定为函数的参数
4. 模板化的函数通常可以通过函数参数推导出模板类型，因此通常情况下可以像调用普通函数那样调用算法

## 2.2 迭代器 
1. 迭代器参数一般都是**迭代器范围**，通常是[)半闭半开区间，因此包含范围中的**第一个元素**，但是不包含**最后一个元素**，因此**尾迭代器实际上是跨越最后一个元素(past-the-end)**的标记    
2. C++11的forward\_list容器只支持**前向迭代器**，这意味着**需要双向迭代器，或者随机访问迭代器的算法**都不能作用于forward\_list容器    
3. 某些算法要求额外的模板类型参数和实参，有时候这些参数是回调，**回调可以是函数对象，函数指针，或者lambda表达式**
4. 大部分算法定义在**<algorithm>**头文件中，还有少数在**<numeric>**头文件中

# 3. lambda表达式
C++11引入lambda表达式来编写内嵌的匿名函数，从而避免编写独立函数或函数对象，是的代码更容易理解===> 没有名字的函数      
```
// 语法
[capture_block](parameters) mutable exception_specification -> return_type {body}

```
1. capture_block ===> 捕捉块，指定如何获取所在作用域的变量，提供给body用 ===> 作用域指的是什么？变量指的是啥？      
2. parameters ===> (可选)参数，只有在**不需要任何参数**，并且**没有指定mutable**，**一个exception specification**， **一个return_type**的情况下可以省略  ===> 怀疑参数是不是可选的?
3. 参数列表和普通函数参数类型一样，但是：**不能有默认值**， **不允许变长参数列表**， **不允许未命名的参数**
> [] {return 10;}

4. mutable：(可选)，所在作用域中的变量如果是**通过值获取**，则lambda body中**可以使用这些变量的副本**，默认这些副本是const的，在lambda body中是不可以修改的，使用**mutable关键字**则可以修改本地副本

5. exception_specification：(可选)：用于指定lambda表达式可以抛出的异常
6. return_type：(可选)：返回值类型，如果忽略，则通过以下原则判断：
7. 如果body为{return expression;}, 则为expression类型； 其他情况下return_type为void类型  ===> 类型推断??

```
// 例子1，其中()代表立即执行这个lambda表达式 ===> (参数)的确是可以省略的  ===> 这个方式
[]{cout << "Hello from lambda!" <<endl;}() ===> 是否执行这个表达式

// 例子2，最后的()代表立即执行，括号内的为调用lambda表达式传入的实际参数，其中返回值可以忽略
// 注意参数传递的方式
string result = [](const string & str) -> string {return "Hello from " + str;}("Second Lambda"); ===>实际参数和形式参数

// 例子3，保存指向lambda表达式的指针，并且通过函数指针执行这个lambda表达式 ===> 怎么推断是个指针的，返回值明明是string类型的
auto fn = [](const string & str) -> string {return "Hello from " + str;}; ===> 只是声明，并没有调用
cout << fn("Call 1") << endl;
cout << fn("Call 2") << endl;

```

## 3.1 capture_block捕捉块
捕捉变量的意思是指：可以在lambda body中使用作用域中的变量，捕捉方式有两种, 默认捕捉是捕捉块中的第一个元素，可以是=或者&：
1. [=]---> 通过**值**捕捉变量  ===> copy值，不改变原来的值
2. [&]---> 通过**引用**捕捉变量 ===> 左值引用，会改变原来的值
3. []---> 代表不从所在作用域中捕捉变量
4. [&x]---> **只通过引用捕捉x**，不捕捉其他变量
5. [x]---> **只通过值捕捉x**，不捕捉其他变量
6. [=, &x, &y] ---> 默认通过值捕捉，变量x，y例外，通过引用捕捉
7. [&, x] ---> 默认通过引用捕捉，变量x是例外，通过值捕捉
8. [&x, &x] ---> 非法，标识符不允许重复

**通过引用捕获的时候，要保证当lambda表达式执行的时候，这个引用还是可用的**===> 因为会改变传入的值      

## 3.2 lambda表达式作为返回值
1. 定义在<functional>头文件中的std::function是一个**多态的函数对象包装**，类似于**函数指针**
2. 它可以绑定到任何被调用的对象(仿函数，成员函数指针，函数指针，lambda表达式)，只要参数和返回类型符合包装的类型即可 
```
// 返回一个double、接受两个整数参数的函数包装
function<double(int, int)> myWrapper; ===> function是函数模板，接收函数作为模板类型参数 ===> 这是个类型吧？？？

// 返回一个lambda表达式
function<int(void)> multiplyBy2Lambda(int x) ===> 作为函数的返回值
{
    return []()->int{return 2*x};
}

// 调用
function<int(void)> fn = multiplyBy2Lambda(10); 
// 使用C++11中的auto可以简化为：
auto fn = multiplyBy2Lambda(10); ===> 这个难道没有执行？？？ 

// 带()是因为要立即执行
cout << fn() << endl; ===> 立即执行
// 如果修改为引用捕捉，则上面就会出问题，因为执行fn()的时候，x引用不再有效  ===> 这个要注意
```

## 3.3 把lambda表达式用做参数
```
// 函数定义
void testCallback(const vector<int> & vec, const function<bool(int)> & callback)
{
    for (auto i : vec)
    {
        if (!callback(i))
        {
            break;
        }
        cout << i << endl;
    }

    cout << endl;
}

// 函数调用
vector<int> vec(10);
int index = 0;

// generate算法要求传入迭代器范围，并将这个范围内的值，替换为lambda表达式的返回值
generate(vec.begin(), vec.end(), [&index]{return ++index;});

// for_each针对指定的范围的元素，执行第三个lambda表达式
for_each(vec.begin(), vec.end(), [](int i){cout << i << " ";});
cout << endl;

// 其中lambda表达式作为回调传入
testCallback(vec, [](int i){return i < 6;}); ===> 作为参数
```

# 4. 函数对象
在类中，可以**重载函数调用运算符()**，从而**使得类的对象可以取代函数指针**，这些对象称为**函数对象(function object)**，或称为**仿函数(functor)**===> 仿函数
> C++中建议尽量使用lambda表达式，而不是函数对象 ===> 函数对象  

## 4.1 算术函数对象
- C++中提供了5类二元运算符的仿函数类模板，plus, minus, multiplies, divides和modulus， 此外还提供了一元取反操作

```
// plus的模板
plus<int> my_plus;
int res = my_plus(4, 5);
cout << res << endl;
```
**上述例子非常愚蠢，没有理由在可以使用operator+的情况下，使用plus类模板**

- 算术函数对象的好处在于**以回调方式传递给算法，而使用算法运算符时却不能直接这样做**
```
// 例子
// 函数对象multiplies<int>()
double mult = accumulate(.begin(), .end(), 1, multiplies<int>());
```
- 表达式multiplies<int>()创建了一个新的multiplies仿函数类对象，并且通过int类型实例化，其他算术函数对象的行为是类似的
> 算术函数对象不过是算术运算符的简单包装，如果算法中使用函数对象作为回调，则务必要保证容器中的对象实现了恰当的操作，如operator*或者operator+等


### 比较函数对象

### 按位函数对象

### 函数对象适配器

### 编写自己的函数对象


# 5. 常用算法

## 5.1 find和find_if算法
**find算法**在一个迭代器范围内查找特定元素，可用于**任意类型容器**；成功则返回**找到元素的迭代器**，失败则返回**尾迭代器**(强调的是，不是底层容器的尾迭代器，而是函数调用中指定的尾迭代器)      
1. 调用find时，不强制要求是容器中元素的完整范围，还可以是元素的子集

```
root@8691524eec08:~/c++# cat find.cc
#include <algorithm>
#include <vector>
#include <iostream>

using namespace std;

int main()
{
    int num;
    vector<int> my_vector;
    
    while (true)
    {
                cout << "Enter a number to add (0 to stop): ";
                cin >> num;
    
                if (num == 0)
                {
                break;
                }
        
                my_vector.push_back(num);
        }

    while (true)
    {
                cout << "Enter a number to lookup (0 to stop): " ;
                cin >> num;

                if (num == 0)
                {
                        break;
                }

                auto end = my_vector.end();

                // 搜索范围是从开始begin()，到结束end()，搜索的是vector的所有元素，如果需要搜索一个子范围，则修改begin()和end()的值
                auto it = find(my_vector.begin(), end, num);  

                if (it == end)
                {
                        cout << "Could not find " << num << endl;
                }
                else
                {
                        cout << "Found " << *it << endl;
                }
        }

    return 0;
}
// 编译c++11的时候需要带上-std=c++11 选项
root@8691524eec08:~/c++# g++ -std=c++11 find.cc -o find.out

// 代表错误出现在哪里，如果和分析错误？
find.cc: In function 'int main()':
// 36行，43行, 错误显示匹配第一个参数不对，这样就可以直接找出问题所在
find.cc:36:43: error: no matching function for call to 'find(<unresolved overloaded function type>, __gnu_cxx::__normal_iterator<int*, std::vector<int> >&, int&)'  
   auto it = find(my_vector.begin, end, num);
In file included from /usr/include/c++/5/algorithm:62:0,
                 from find.cc:1:
/usr/include/c++/5/bits/stl_algo.h:3782:5: note: candidate: _IIter std::find(_IIter, _IIter, const _Tp&) [with _IIter = __gnu_cxx::__normal_iterator<int*, std::vector<int> >; _Tp = int]
     find(_InputIterator __first, _InputIterator __last,
     ^
/usr/include/c++/5/bits/stl_algo.h:3782:5: note:   no known conversion for argument 1 from '<unresolved overloaded function type>' to '__gnu_cxx::__normal_iterator<int*, std::vector<int> >'
In file included from /usr/include/c++/5/bits/locale_facets.h:48:0,
                 from /usr/include/c++/5/bits/basic_ios.h:37,
                 from /usr/include/c++/5/ios:44,
                 from /usr/include/c++/5/ostream:38,
                 from /usr/include/c++/5/iostream:39,
                 from find.cc:3:
/usr/include/c++/5/bits/streambuf_iterator.h:369:5: note: candidate: template<class _CharT2> typename __gnu_cxx::__enable_if<std::__is_char<_CharT2>::__value, std::istreambuf_iterator<_CharT> >::__type std::find(std::istreambuf_iterator<_CharT>, std::istreambuf_iterator<_CharT>, const _CharT2&)
     find(istreambuf_iterator<_CharT> __first,
     ^
/usr/include/c++/5/bits/streambuf_iterator.h:369:5: note:   template argument deduction/substitution failed:
find.cc:36:43: note:   mismatched types 'std::istreambuf_iterator<_CharT>' and 'std::vector<int>::const_iterator (std::vector<int>::*)() const noexcept {aka __gnu_cxx::__normal_iterator<const int*, std::vector<int> > (std::vector<int>::*)() const noexcept}'
   auto it = find(my_vector.begin, end, num);
                                           ^
find.cc:36:43: note:   mismatched types 'std::istreambuf_iterator<_CharT>' and 'std::vector<int>::iterator (std::vector<int>::*)() noexcept {aka __gnu_cxx::__normal_iterator<int*, std::vector<int> > (std::vector<int>::*)() noexcept}'
find.cc:36:43: note:   could not resolve address from overloaded function 'my_vector.std::vector<int>::begin'
``` 
2. 一些容器(map和set)以**类方法的方式**提供了自己的find版本，其中如果一个容器提供的方法具有与泛型算法相同的功能，那么应该使用**容器提供的对应的方法**
3. 如泛型find算法的运行时间是**线性时间**，用于map迭代器的也是，但是map上的find()方法运行时间是**对数时间**

4. **find\_if算法**第3个参数是一个**谓词函数**而不是一个简单的匹配元素，**谓词函数返回true或者false**；算法对范围内的每个元素调用**谓词函数**，直到整个函数返回true，如果返回true，则整个算法返回引用**这个元素的迭代器**
```
// 谓词函数
bool perfectScore(int num)
{
    return (num >= 100);
}

// 函数指针，谓词函数会对vector中的每个int元素做比较，直到赴安徽true为止
auto it = find_if(my_vector.begin(), my_vector.end(), perfectScore);
```
为了简单期间，可以使用lambda表达式
```
// 使用了匿名函数lambda表达式
auto it = find_if(my_vector.begin(), my_vector.end(), [](int i) {return i >= 100;} );

```
**注意STL中没有提供find_all或者等效算法来返回匹配谓词的所有实例**


## 5.2 accumulate算法
- 用来计算所有元素的总和或者其他的算术运算，最基本的形式是计算指定范围内的元素的总和
```
// accumulate在<numeric>中声明的
#include <numeric>

// 接收的第3个参数总是和的初始值，例子中是从0开始累加， 返回值是double类型？
double sum = accumulate(.begin(), .end(), 0); 

```
- 通过添加第4个参数，来允许使用者指定要执行的操作，而不是默认的加法运算
```
int product(int num1, int num2)
{
    return num1 * num2;
}

// 第3个参数默认值是1，第4个是函数指针，代表要执行的操作
double mult = accumulate(.begin(), .end(), 1, product);


// lambda表达式版本
double mult = accumulate(.begin(), .end(), 1, [](int num1, int num2){return num1 * num2});

```

## 5.3 count_if算法


## 5.4 generate算法


## 5.5 for_each算法

## 5.6 算法中使用C++11移动语义
C++11移动语义能够提高特定算法的性能，因此在**自定义的类中**建议实现**移动copy构造函数**和**移动赋值运算符**
