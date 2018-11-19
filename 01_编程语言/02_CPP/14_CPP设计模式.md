# 1. 单子模式
只存在某类的单一共享对象, 存在某种全局访问策略，在需要的时候访问该对象, **需要研究一下**      
```
clas Singleton
{
    public:
        static Singleton * Get()
        {
            if(!m_s)
            m_s = new Singleton; // 调用构造函数
            return m_s;
        }    // 间接获得成员

        int GetData() 
        {
            return ++a;
        }    
    private:
        Singleton:a(0)() {}
        Singleton(const Singleton &other); // 只声明不定义，禁止copy
        Singleton & operator=(cosnt Singleton &other); // 禁止赋值
        ~Singleton();// 禁止析构 

    private:
        static Singleton * m_s; // 静态数据成员，指向本类唯一对象的指针
        int a; // 验证数据
};

Singleton * Singleton::m_s = NULL; // static变量进行定义

int main()
{

    cout << Singleton::GetData() << endl; // 错误，GetData不是静态方法，不能使用类调用
    cout << Singleton::Get() -> GetData() << endl; // 使用指向对象的指针调用

    return 0;
}

```