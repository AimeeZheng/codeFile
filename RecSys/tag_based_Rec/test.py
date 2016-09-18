# -*- coding: utf-8 -*-
"""
Created on Wed Jun 29 09:48:25 2016

@author: zhengyaolin
"""

import pandas as pd
import os

path = os.getcwd()
df = pd.read_csv(os.path.join(path, os.path.normpath('data\user_item_gather_20160519_20160602.csv')))
user_active = set(df['MD5_IMEI'])
    
def evaluate(topN):
    
    test = pd.read_csv(os.path.join(path, os.path.normpath('data\user_items_test.csv')), names = ['MD5_IMEI', 'test'], header = None)
    test.drop_duplicates(inplace = True)
    test.dropna(inplace = True)
    test_user = list(set(test['MD5_IMEI']) & user_active)
    print(len(test_user))
    
    predict = pd.read_csv(os.path.join(path, os.path.normpath('data\recommend_result_top' + str(topN) + '.csv')), names = ['MD5_IMEI', 'pre'], header = None)
    pre = predict[predict['MD5_IMEI'].isin(test_user)]
    
    data = pd.merge(pre, test, on = 'MD5_IMEI')
    m = data.shape[0]
    #p_all = 0
    #r_all = 0
    #f_all = 0
    n_test = 0
    n_right = 0
    
    for i in range(m):
        u = data.ix[i]
        imei = u['MD5_IMEI']
        print('User:', imei)
        test = set(u['test'].split('|'))
        test.remove('')
        pre = set(u['pre'].split('|'))
        
        n_right += len(test & pre)
        n_test += len(test)

    #准确率
    precision = n_right / (topN * m)   
    #召回率
    recall = n_right / n_test   
    #F1
    if precision > 0 and recall > 0:
        f1 = precision * recall * 2 / (precision + recall)
    else:
        f1 = 0 
    
    print('precision:', precision)
    print('recall:', recall)
    print('F1:', f1)

    