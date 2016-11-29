# -*- coding: utf-8 -*-
"""
Created on Wed Aug 24 09:59:37 2016

@author: zhengyaolin
@description：基于数据对的聚类算法(the clustering algorithm based on data pairs
"""

import numpy as np
import pandas as pd
import os

#数据保存根目录
path = r'/home/zhengyaolin/data'

def save(out, info):
    '''存储
    
    Parameters
    ----------
    out： output path
    info：list of lists
    '''
    print('saving...')
    df = pd.DataFrame(info)
    df.to_csv(out, sep = '|', index = False, header = False, encoding = 'utf-8')
 
 
def clustering_BDP(k = 2):
    '''
    基于数据对的分类算法
    
    Parameters
    ----------
    k：k项完全连通集聚类
    
    Attributes
    ----------
    S2：2项连通集(原始通话数据对)
    Sk：k项完全连通集
    Skp：k+1项完全连通集
    
    Notes
    -----
    1、连接
    2、判断联通性
    '''
    #原始数据对：2项连通集
    df = pd.read_csv(os.path.join(path, os.path.normpath('S2.csv')), sep = '|', header = None, dtype = str)   
    S2 = []    
    for i in np.array(df).tolist():
        S2.append(tuple(i))
    S2_map = dict([(k,1) for k in S2])    
    
    #输入
    if k == 2:
        data = df
    else:
        data = pd.read_csv(os.path.join(path, os.path.normpath('S' + str(k) + '.csv')), sep = '|', header = None, dtype = str)
    
    #边跑边存
    output = os.path.join(path, os.path.normpath('S' + str(k + 1) + '.csv'))
    by = [i for i in range(k - 1)]
    Skp = []
    for u, group in data.groupby(by):
        m = group.shape[0]
        if m > 1:
            sets = np.array(group)
            for i in range(m - 1):
                set1 = list(sets[i])
                j = i + 1
                while j < m:
                    set2 = list(sets[j])
                    if set1[k - 1] < set2[k - 1]:
                        pair = [set1[k - 1], set2[k - 1]]
                    else:
                        pair = [set2[k - 1], set1[k - 1]]
                    p = tuple(pair)
                    if p in S2_map:
                        u_set = set1[:-1]
                        u_set.extend(pair)
                        Skp.append(u_set)
                    j += 1
    save(output, Skp)
    print(str(k) + "-items sets have been clusted to " + str(k + 1) + "-items sets!")

    
if __name__ == "__main__": 
    clustering_BDP(k = 2) 

     
