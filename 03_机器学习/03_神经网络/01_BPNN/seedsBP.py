# -*- coding: utf-8 -*-

from txtToCsv import txt_to_csv

# BP算法用途：1：离散输出作为分类 2：连续输出作为回归

# 小麦种子有7个特征，因此设计7个神经元(7列)，输出是3个分类(3列)
# 设计只有一个隐含层，隐含层的神经元个数为5 ==> 超参数，凭借人工经验设定

from random import seed
from random import random

if __name__ == '__main__':
    seed(20)
    print(random())
    for i in range(20): # range函数相当于生成一个[0, 20)的范围
        print(i)