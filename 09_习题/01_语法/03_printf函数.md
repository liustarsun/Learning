# 1. 函数原型
**返 回 值: 成功则返回实际输出的字符数，失败返回-1**      
```
int printf(const char *format[,argument]...)
```

**函数说明**:      
1. 在printf()函数中，format后面的参数个数不确定，且类型也不确定，这些参数都存放在栈内
2. 调用printf()函数时，根据format里的格式("%d %f...")依次将栈里参数取出，从最靠近第一个可变参数的固定参数开始，依次获取每个可变参数的地址
3. 而取出动作要用到va_arg、va_end、va_start这三个宏定义，再加上va_list

## 1.1 va_list
```
char *类型==> typedef char* va_list;
```

## 1.2 三个宏定义
```
#define _INTSIZEOF(n)    ((sizeof(n) + sizeof(int) - 1) & ~(sizeof(int) - 1) ) 

// 宏va_start： 通过该宏定义可以获取到可变参数表的首地址，并将该地址赋给指针ap
#define va_start(ap,v)     ( ap = (va_list)&v + _INTSIZEOF(v) ) 

// 宏va_arg： 通过该宏定义可以获取当前ap所指向的可变参数，并将指针ap指向下一个可变参数==>该宏的第二个参数为类型
#define va_arg(ap,type)  ( *(type *)((ap += _INTSIZEOF(type)) - _INTSIZEOF(type)) )

// 宏va_end：通过该宏定义可以结束可变参数的获取
#define va_end(ap)          ( ap = (va_list)0 ) 
```

## 1.3 例子
```
#include <stdio.h>  
  
typedef char* va_list;   

#define _INTSIZEOF(n)    ((sizeof(n) + sizeof(int) - 1) & ~(sizeof(int) - 1) )   

#define va_start(ap,v)   ( ap = (va_list)&v + _INTSIZEOF(v) )   

#define va_arg(ap,type)  ( *(type *)((ap += _INTSIZEOF(type)) - _INTSIZEOF(type)) )   

#define va_end(ap)       ( ap = (va_list)0 )   
  
int cal_val(int c, ...)   
{   
    int sum = c;   
    va_list ap;              //声明指向char型的指针  
    va_start(ap,c);          //获取可变参数列表的首地址，并赋给指针ap  
  
    c = va_arg(ap,int);      //从可变参数列表中获取到第一个参数(返回值即为参数)  
    while(0 != c)   
    {   
        sum += c;   
        c = va_arg(ap,int);  //循环的从可变参数列表中获取到参数(返回值即为参数)  
    }  
    va_end(ap);              //结束从可变参数列表中获取参数  
    return sum;   
}    
   
int main(int argc, char* argv[])   
{   
    int value1；  
      
    value1 = cal_val(1,2,3,4,5,6,7,8,9,0);   
    printf("value1=%d/n",value1);  
    value2 = cal_val(6,7,8,9,0);   
    printf("value2=%d/n",value2);  
      
    return 0;   
}     
```