### **安装步骤**

#### **1. 使用pip安装virtualenv**
```
liu:~ xingyanl$ pip install --upgrade virtualenv
```

#### **2. 设置环境**
```
liu:~ xingyanl$ virtualenv --system-site-packages -p python3 ~/tensorflow
```

#### **3. source环境**
```
liu:~ xingyanl$ source ~/tensorflow/bin/activate
(tensorflow) liu:~ xingyanl$
(tensorflow) liu:~ xingyanl$ easy_install -U pip
(tensorflow) liu:~ xingyanl$ pip3 install --upgrade tensorflow
```
[源代码链接](tensorflow-tutorial/Deep_Learning_with_TensorFlow/datasets at master · caicloud/tensorflow-tutorial)

#### **4. 退出环境**
```
(tensorflow) liu:~ xingyanl$ deactivate
```
