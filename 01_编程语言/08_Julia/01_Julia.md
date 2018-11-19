# 学习一门新的语言的步骤
# 1. 变量
# 流程的pythonpdf
# 伯乐在线python板块
# https://www.codewars.com/ 好网站

Try `help help' or `man -k getpid' or `info getpid'
asb@docker:ParallelProcess$ g++  paralleProcess.cc  -lpthread

-std=c++11

shared_ptr<int> 和 int *是两种类型，不能直接相互使用
CaptureRecipe.hpp (pipetasks\capture\nahka):    std::queue<std::shared_ptr<CaptureParams>> requests;


shared_ptr<T> smart;

// ... some code here points smart at an object ...

T *dumb1 = smart.get(); // creates a dumb pointer to the object managed by smart
void *dumb2 = smart.get(); // dumb pointers automatically convert to void*

遗留的问题：
1. new和delete使用，申请了但是没有释放，所以有些东西是否要copy，内存检测工具测试自己的代码
2. enum的使用
3. 把vector拆分成数组