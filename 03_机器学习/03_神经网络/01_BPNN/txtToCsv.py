# -*- coding: utf-8 -*-

# 果然是两个功能强大的库哦
import numpy as np
import pandas as pd

def txt_to_csv(txt, csv):
    txtFile = np.loadtxt(txt)
    txtDF = pd.DataFrame(txtFile)
    txtDF.to_csv(csv, index=False)


if __name__ == '__main__':
    txt_to_csv('seeds_dataset.txt', 'seeds_dataset.csv')

