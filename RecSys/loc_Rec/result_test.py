# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 16:49:52 2016

@author: zhengyaolin
"""

import pandas as pd
import numpy as np
import os

path = os.getcwd()
city = 'CA'
#city = 'NY'

check_names = ['user_id', 'venue_id']

def user_checkin():
    '''
    user_id|train|test
    
    '''
    old = pd.read_csv(os.path.join(path, os.path.normpath('data/user_venue_' + city + '_train.csv')), names = ['venue_id', 'user_id'], sep = '|', dtype = str)
    old = old[check_names]    
    new = pd.read_csv(os.path.join(path, os.path.normpath('data/user_venue_' + city + '_test.csv')), sep = '|', dtype = str)
    new = new[check_names]
    new.drop_duplicates(inplace = True)
    for user, group in old.groupby('user_id'):
        info = str(user) + '|'
        for i, row in group.iterrows():
            info += str(row['venue_id']) + ','
        info = info[:-1] + '|'
        new_venue = new[new['user_id'] == user]
        for i, row in new_venue.iterrows():
            info += str(row['venue_id']) + ','
        info = info[:-1] + '\n'
        with open(os.path.join(path, os.path.normpath('data/user_venue_novelty_' + city + '.csv')), 'a') as f:
            f.write(info)
            
def test_new():
    '''
    user_id|count_new|new&old|p
    
    '''
    df = pd.read_csv(os.path.join(path, os.path.normpath('data/user_venue_novelty_' + city + '.csv')), sep = '|', header = None, dtype = str)     
    for i, row in df.iterrows():
        old = set(row[1].split(','))
        new = set(row[2].split(','))
        a = len(old & new)
        n = len(new)
        with open(os.path.join(path, os.path.normpath('data/test_new_' + city + '.csv')), 'a') as f:
            f.write(str(row[0]) + '|' + str(n) + '|' + str(a) + '|' + str(a/n) + '\n')
    df = pd.read_csv(os.path.join(path, os.path.normpath('data/test_new_' + city + '.csv')), sep = '|', header = None, dtype = str)   


def test_result(topN):
    '''
    topN: int
    '''
    test = pd.read_csv(os.path.join(path, os.path.normpath('test/user_venues_test_' + city + '.csv')), sep = '|', names = ['user_id', 'venue_id'], dtype = str)     
    predict = pd.read_csv(os.path.join(path, os.path.normpath('test/part-r-00000')), sep = '|', header = None, dtype = str)    
    right_all = 0
    venue_test = 0
    for i, row in predict.iterrows():
        u = row[0]
        rec = set([row[i] for i in range(1, topN+1)])
        v = set(np.array(test[test['user_id'] == u]['venue_id'])[0].split(','))
        right = len(rec & v)
        right_all += right
        venue_test += len(v)
    # 准确率
    precise = right_all / (len(predict) * topN)
    # 召回率
    recall = right_all / venue_test
    # F1值
    f1 = 2 * precise * recall / (precise + recall)
    print('precise:', precise * 100, '%')   
    print('recall:', recall * 100, '%')
    print('f1:', f1)

            

def test_CF(topN):
    test = pd.read_csv(os.path.join(path, os.path.normpath('test/user_venues_test_' + city + '.csv')), sep = '|', names = ['user_id', 'venue_id'], dtype = str)     
    predict = pd.read_csv(os.path.join(path, os.path.normpath('test/predict_result_' + city + '')), sep = '\t', header = None, dtype = str)
    right_all = 0
    venue_rec = 0
    venue_test = 0
    #test_v = []
    for i,row in predict.iterrows():
        u = row[0]
        rec = []
        venues = row[1].split('|')
        for v in venues:
            rec.append(v.split(',')[0])
        v_real = set(np.array(test[test['user_id'] == u]['venue_id'])[0].split(','))
        right = len(set(rec[:topN]) & v_real)
        right_all += right
        venue_rec += len(rec[:topN])
        venue_test += len(v_real)
        #test_v.append(len(v_real))
    count_u = len(test)
    if venue_rec < topN*count_u:
        venue_rec = topN*count_u
    # 准确率
    precise = right_all / venue_rec
    # 召回率
    recall = right_all / venue_test
    # F1值
    f1 = 2 * precise * recall / (precise + recall)
    print('precise:', precise * 100, '%')   
    print('recall:', recall * 100, '%')
    print('f1:', f1)
    print(venue_rec)
