# -*- coding: utf-8 -*-
"""
Created on Mon Jun 13 14:18:35 2016

@author: zhengyaolin
@description: 预处理，用于抽样和过滤

"""

import pandas as pd
import numpy as np
import csv
import os

df = pd.read_csv(r'G:\data\dmdata\login.txt', sep='$', header = None, na_values = np.nan)
path = os.getcwd()

#筛选用户
imei = df[14].unique()
m = int(len(imei) * 0.3)
sampler = np.random.permutation(len(imei))
sample = imei.take(sampler[:m])

files = ['useracfun', 'userinterest', 'usercomment_new', 'contentcollect', 'usersearch', 'contentdownload']
big_files = ['onlineplay', 'columnclick', 'channelclick', 'contentclick']

#筛选<1G的文件
for i in files:
    input_path = os.path.normpath(r'G:\data\dmdata\\' + i + '.txt')
    #忽略引用
    data = pd.read_csv(input_path, sep='$', header = None, quoting = csv.QUOTE_NONE)
    m, n = data.shape
    output_path = os.path.join(path, os.path.normpath('data/' + i + '.csv'))
    data[data[n - 1].isin(sample)].to_csv(output_path, index = False, header = False, encoding = 'utf-8')
    print(i, 'filted')

#分块筛选>1G的文件
for i in big_files:
    print('file', i, 'begin :')
    input_path = os.path.normpath(r'G:\data\dmdata\\' + i + '.txt')
    output_path =  os.path.join(path, os.path.normpath('data/' + i + '.csv'))
    reader = pd.read_csv(input_path, sep='$', header = None, chunksize = 3000000)
    for chunk in reader:
        m, n = chunk.shape
        data = chunk[chunk[n - 1].isin(sample)]
        print(data.shape[0], 'of', m, 'rows')
        data.to_csv(output_path, index = False, header = False, encoding = 'utf-8', mode = 'a')
    print('filted!')

