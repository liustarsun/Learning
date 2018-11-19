# 1. 安装Anaconda
Anaconda是库管理工具，能够管理不同环境，不同环境下可以安装不同python版本以及其他库
```
# 下载地址
https://www.anaconda.com/download/#windows
```

------
# 2. 创建单独环境tensorflow
```
# 更新版本
(base) C:\Nsb\Test>conda update -n base conda

# 创建tensorflow环境
(base) C:\Nsb\Test>conda create -n tensorflow python=3.5
Solving environment: done

# 激活tensorflow
(base) C:\Nsb\Test>conda activate tensorflow

# 更新pip
(tensorflow) C:\Nsb\Test>pip install --ignore-installed --upgrade tensorflow

# 关闭tensorflow
(base) C:\Nsb\Test>conda deactivate
```


------
# 3. 验证安装是否成功
```
==>(base) C:\Users\xingyanl>python
Python 3.6.5 |Anaconda, Inc.| (default, Mar 29 2018, 13:32:41) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.

==>>> import tensorflow as tf
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named 'tensorflow'

==>>> exit()

==> (base) C:\Users\xingyanl>activate tensorflow

(tensorflow) C:\Users\xingyanl>python
Python 3.5.6 |Anaconda, Inc.| (default, Aug 26 2018, 16:05:27) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.

>>> import tensorflow as tf
>>> import os 

# 屏蔽AVX2告警     
>>> os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2' 
>>> hello = tf.constant('Hello, TensorFlow!')
>>> sess = tf.Session()
2018-09-08 16:01:22.865485: I T:\src\github\tensorflow\tensorflow\core\platform\cpu_feature_guard.cc:141] Your CPU supports instructions that this TensorFlow binary was not compiled to use: AVX2(CPU的低端指令，使用源码安装的时候，可以进行优化)

>>> print(sess.run(hello))
b'Hello, TensorFlow!'

>>>
```

------
# 4. 安装数据获取框架
```
(tensorflow) asb@docker:~$ pip install tushare   ======>  下载tushare框架
(tensorflow) asb@docker:~$ pip install tushare --upgrade  ====> 更新tushare框架
Requirement already up-to-date: tushare in ./.conda/envs/tensorflow/lib/python3.5/site-packages (1.2.15)
Requirement already satisfied, skipping upgrade: msgpack>=0.5.6 in ./.conda/envs/tensorflow/lib/python3.5/site-packages (from tushare) (0.5.6)
Requirement already satisfied, skipping upgrade: requests>=2.0.0 in ./.conda/envs/tensorflow/lib/python3.5/site-packages (from tushare) (2.20.0)
Requirement already satisfied, skipping upgrade: simplejson>=3.16.0 in ./.conda/envs/tensorflow/lib/python3.5/site-packages (from tushare) (3.16.0)
Requirement already satisfied, skipping upgrade: lxml>=3.8.0 in ./.conda/envs/tensorflow/lib/python3.5/site-packages (from tushare) (4.2.5)
Requirement already satisfied, skipping upgrade: pyzmq>=16.0.0 in ./.conda/envs/tensorflow/lib/python3.5/site-packages (from tushare) (17.1.2)
Requirement already satisfied, skipping upgrade: pandas>=0.18.0 in ./.conda/envs/tensorflow/lib/python3.5/site-packages (from tushare) (0.23.4)
Requirement already satisfied, skipping upgrade: certifi>=2017.4.17 in ./.conda/envs/tensorflow/lib/python3.5/site-packages (from requests>=2.0.0->tushare) (2018.8.24)
Requirement already satisfied, skipping upgrade: urllib3<1.25,>=1.21.1 in ./.conda/envs/tensorflow/lib/python3.5/site-packages (from requests>=2.0.0->tushare) (1.24.1)
Requirement already satisfied, skipping upgrade: idna<2.8,>=2.5 in ./.conda/envs/tensorflow/lib/python3.5/site-packages (from requests>=2.0.0->tushare) (2.7)
Requirement already satisfied, skipping upgrade: chardet<3.1.0,>=3.0.2 in ./.conda/envs/tensorflow/lib/python3.5/site-packages (from requests>=2.0.0->tushare) (3.0.4)
Requirement already satisfied, skipping upgrade: pytz>=2011k in ./.conda/envs/tensorflow/lib/python3.5/site-packages (from pandas>=0.18.0->tushare) (2018.7)
Requirement already satisfied, skipping upgrade: numpy>=1.9.0 in ./.conda/envs/tensorflow/lib/python3.5/site-packages (from pandas>=0.18.0->tushare) (1.15.4)
Requirement already satisfied, skipping upgrade: python-dateutil>=2.5.0 in ./.conda/envs/tensorflow/lib/python3.5/site-packages (from pandas>=0.18.0->tushare) (2.7.5)
Requirement already satisfied, skipping upgrade: six>=1.5 in ./.conda/envs/tensorflow/lib/python3.5/site-packages (from python-dateutil>=2.5.0->pandas>=0.18.0->tushare) (1.11.0)
(tensorflow) asb@docker:~$ 
```

## 4.1 接口的token
```
e49f11439ae007e705ebd16dc536cb79d585d99ea5a515d4bf1ea304
```