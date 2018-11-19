原文来自[更新homebrew](https://blog.csdn.net/u010275932/article/details/76080833)

# 1. 安装
安装自行百度      

# 2. 更新
Homebrew的更新源由三部分组成：本体（brew.git）、核心（homebrew-core.git）以及二进制预编译包(homebrew-bottles)
## 2.1 诊断Homebrew
```
$ brew doctor
```

## 2.2 重置brew.git设置
```
$ cd "$(brew --repo)"
$ git fetch
$ git reset --hard origin/master
```

## 2.3 重置homebrew-core.git
```
$ cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
$ git fetch
$ git reset --hard origin/master
```
## 2.4 应用生效
```
$ brew update
```

## 2.5 更新源的选择
```
# 替换brew.git:
$ cd "$(brew --repo)"
# 中国科大:
$ git remote set-url origin https://mirrors.ustc.edu.cn/brew.git
# 清华大学:
$ git remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/brew.git
# 官方:
$ git remote set-url origin https://github.com/Homebrew/brew.git


# 替换homebrew-core.git:
$ cd "$(brew --repo)/Library/Taps/homebrew/homebrew-core"
# 中国科大:
$ git remote set-url origin https://mirrors.ustc.edu.cn/homebrew-core.git
# 清华大学:
$ git remote set-url origin https://mirrors.tuna.tsinghua.edu.cn/git/homebrew/homebrew-core.git
# 官方:
$ git remote set-url origin https://github.com/Homebrew/homebrew-core.git


# 替换homebrew-bottles:
# 中国科大:
$ echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.ustc.edu.cn/homebrew-bottles' >> ~/.bash_profile
$ source ~/.bash_profile
# 清华大学:
$ echo 'export HOMEBREW_BOTTLE_DOMAIN=https://mirrors.tuna.tsinghua.edu.cn/homebrew-bottles' >> ~/.bash_profile
$ source ~/.bash_profile

# 应用生效:
$ brew update

# 更新软件
$ brew upgrade

# 删除old的安装文件
$ brew cleanup
```

## 2.6 更新vim配置
```
// 更新使得terminal显示颜色
liu:~ xingyanl$ brew install coreutils
liu:~ xingyanl$ cat ~/.vimrc
syntax on
set background=dark
colorscheme solarized
liu:~ xingyanl$ 
```


## 2.7 禁止MAC的itunes备份iphone资料
```
liu:~ xingyanl$ defaults write com.apple.iTunes DeviceBackupsDisabled -bool YES
liu:~ xingyanl$ 
liu:~ xingyanl$ defaults delete com.apple.iTunes DeviceBackupsDisabled
liu:~ xingyanl$ 
liu:~ xingyanl$ defaults write com.apple.iTunes DeviceBackupsDisabled -bool YES
liu:~ xingyanl$ 
```