# vim 配置
## 1. 安装依赖环境
```
 set encoding=utf-8

// 删除原来安装的vim
 apt-get autoremove vim vim-runtime gvim vim-tiny vim-common vim-gui-common

// 安装依赖包
apt-get install libncurses5-dev libgnome2-dev libgnomeui-dev libgtk2.0-dev libatk1.0-dev libbonoboui2-dev libcairo2-dev libx11-dev libxpm-dev libxt-dev python-dev ruby-dev mercurial

// 下载vim
git clone https://github.com/vim/vim.git
cd vim

// 配置环境
 ./configure --with-features=huge --enable-pythoninterp --enable-rubyinterp --enable-luainterp --enable-perlinterp --with-python-config-dir=/usr/lib/python2.7/config-x86_64-linux-gnu/ --enable-gui=gtk2 --enable-cscope --prefix=/usr

// 编译安装
 make && make install

// 重新安装的时候需要先
make clean & make distclean

// 安装成功以后查看python是否可用
vim
:echo has('python')
```

```
https://github.com/yangyangwithgnu/use_vim_as_ide/blob/master/README.md?utf8=%E2%9C%93#7.1

https://blog.csdn.net/eudivkfdskf/article/details/52206572
http://www.eet-china.com/news/article/201704051605
http://www.hahack.com/codes/cmake/
```

```
clang中不使用using namespace std;

安装ctags
root@1b7b55948b9b:~# apt-get install ctags

```

// 安装LLVM clang
```
root@1b7b55948b9b:~/build# apt-get install cmake

make -j 4
```