# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 17:18:31 2016

@author: zhengyaolin
@description: 算法实现
"""

import pandas as pd
import numpy as np
import math
import sys
import os

'''
p(u,i) =  n(u,t) * n(t,i) / log(1 + n(t)) * log(1 + n(i))
'''
actions = ['download', 'collect', 'onlineplay', 'click']
path = os.getcwd()
loc = os.path.join(path, os.path.normpath('data'))

#users for test
imei_df = pd.read_csv(loc + r'\TRAIN_IMEI.csv')
imeis = sorted(imei_df['MD5_IMEI'].unique())

#items 
item_df = pd.read_csv(loc + r'\items.csv')
items = sorted(list(item_df['OPUS_ID']))

#使用公式计算某种行为下的p值
def tf_idf(act_type):
    #用户-动漫 （分段）
    user_item_reader = pd.read_csv(loc + r'\user_item_' + act_type + '_matrix.csv', index_col = 0, chunksize = 1000)
    #动漫-标签 item-tag(0/1)
    item_tag = pd.read_csv(loc + r'\item_tag_matrix.csv', index_col = 'OPUS_ID')
    items = list(item_tag.index)
    tags = list(item_tag.columns)
    y = np.array(item_tag)
    #标签-动漫
    item_tag_count = pd.read_csv(loc + r'\item_tag_' + act_type + '.csv', index_col = 'OPUS_ID')
    df2 = item_tag_count.T
    #使用标签t的用户数
    tag_users = pd.read_csv(loc + r'\tag_count_user_' + act_type + '.csv', index_col = 'tag', encoding = 'gbk')
    #标注物品i的用户数
    item_users = pd.read_csv(loc + r'\item_count_user_' + act_type + '.csv', index_col = 'OPUS_ID')
    f = lambda x: math.log10(x + 1)
    tf_idf2 = df2.div(item_users['count'].apply(f), axis = 1)
    
    print('tf-idf:', act_type)
    for chunk in user_item_reader:
        users = list(chunk.index)
        x = np.array(chunk).dot(y) #u-t
        df1 = pd.DataFrame(x, index = users, columns = tags)       
        tf_idf1 = df1.div(tag_users['count'].apply(f), axis = 1)
        tf_idf1.fillna(0, inplace = True)
        data = pd.DataFrame(np.array(tf_idf1).dot(np.array(tf_idf2)), index = users, columns = items)
        print(users[-1])
        data.to_csv(loc + r'\p_u_i_' + act_type + '.csv', mode = 'a', header = False, encoding = 'utf-8', float_format = '%.6f')
        
#冷启动计算兴趣标签项  
def user_interest():    
    #用户兴趣标签
    user_tag_reader = pd.read_csv(loc + r'\user_tag_like_matrix.csv', index_col = 'MD5_IMEI', chunksize = 1000)
    #标签t为兴趣的用户数
    tag_like_users = pd.read_csv(loc + r'\tag_count_user_interest.csv', index_col = 'tag')
    #动漫-标签 t打在i上的次数
    item_tag = pd.read_csv(loc + r'\item_tag_all.csv', index_col = 'OPUS_ID')
    items = list(item_tag.index)
    #标注物品i的用户数
    item_users = pd.read_csv(loc + r'\item_count_user_all.csv', index_col = 'OPUS_ID')
    f = lambda x: math.log10(x + 1)
    tf_idf2 = item_tag.T.div(item_users['count'].apply(f), axis = 1)
    y = np.array(tf_idf2)
    #计算用户对动漫的兴趣值
    for chunk in user_tag_reader:
        users = list(chunk.index)
        tf_idf1 = chunk.div(tag_like_users['count'].apply(f), axis = 1)
        tf_idf1.fillna(0, inplace = True)
        x = np.array(tf_idf1)  
        data = pd.DataFrame(x.dot(y), index = users, columns = items)
        print(users[-1])
        data.to_csv(loc + r'\p_u_i_interest.csv', mode = 'a', header = False, encoding = 'utf-8', float_format = '%.6f')

#权重叠加计算最终兴趣值
def p_u_i(a, topN):
    download = pd.read_csv(loc + r'\p_u_i_download.csv', index_col = 0, names = items, iterator = True)
    collect = pd.read_csv(loc + r'\p_u_i_collect.csv', index_col = 0, names = items, iterator = True)
    onlineplay = pd.read_csv(loc + r'\p_u_i_onlineplay.csv', index_col = 0, names = items, iterator = True)
    click = pd.read_csv(loc + r'\p_u_i_click.csv', index_col = 0, names = items, iterator = True)
    interest = pd.read_csv(loc + r'\p_u_i_interest.csv', index_col = 0, names = items, iterator = True)
    user_history = pd.read_csv(loc + r'\user_items_20160519_20160602.csv', names = ['MD5_IMEI', 'items'], index_col = 'MD5_IMEI')

    
    n_users = len(imeis)
    loop = int(n_users / 1000) + 1
    last = n_users % 1000
    
    while loop:
        print('loop:', loop)
        if loop == 1:
            chunksize = last
        else:
            chunksize = 1000
            
        p1 = download.get_chunk(chunksize)
        p2 = collect.get_chunk(chunksize)
        p3 = onlineplay.get_chunk(chunksize)
        p4 = click.get_chunk(chunksize)
        p5 = interest.get_chunk(chunksize)
        
        p = p1 * a[0] + p2 * a[1] + p3 * a[2] + p4 * a[3] + p5 * a[4]
        p.to_csv(loc + r'\p_u_i.csv', mode = 'a', header = None, encoding = 'utf-8', float_format = '%.6f')
        
        m = p.shape[0]
        for i in range(m):
            u = p.ix[i]
            print('User:', u.name)
            try:
                old = user_history.ix[u.name]['items'].split('|')
            except KeyError as e:
                print(sys.stderr, e)
                print('No history for user:', u.name)
                old = list()
            finally:
                #去除历史 从高到低 topN
                print('user history:', old)
                rec = list(u[~u.index.isin(old)].order(ascending = False)[:topN].index)
                info = u.name + ','
                for item in rec:
                    info += str(item) + '|'
                info = info[:-1] + '\n'
                with open(loc + r'\recommend_result_top' + str(topN) + '.csv', 'a') as f:
                    f.write(info)
        loop -= 1
    
#根据计算结果，取topN值    
def top(n, act = 'all'):
    if act == 'all':
        path = loc + r'\p_u_i.csv'
    else:
        path = loc + r'\p_u_i_' + act + '.csv'
    p_u_i_reader = pd.read_csv(path, index_col = 0, names = items, iterator = True)
    user_history = pd.read_csv(loc + r'\user_items_20160519_20160602.csv', names = ['MD5_IMEI', 'items'], index_col = 'MD5_IMEI')
    
    n_users = len(imeis)
    loop = int(n_users / 1000) + 1
    last = n_users % 1000
    
    while loop:
        print('loop:', loop)
        if loop == 1:
            chunksize = last
        else:
            chunksize = 1000
            
        p = p_u_i_reader.get_chunk(chunksize)
        m = p.shape[0]
        
        for i in range(m):
            u = p.ix[i]
            print('User:', u.name)
            try:
                old = user_history.ix[u.name]['items'].split('|')
            except KeyError as e:
                print(sys.stderr, e)
                print('No history for user:', u.name)
                old = list()
            finally:
                #去除历史 从高到低 topN
                print('user history:', old)
                rec = list(u[~u.index.isin(old)].order(ascending = False)[:n].index)
                info = u.name + ','
                for item in rec:
                    info += str(item) + '|'
                info = info[:-1] + '\n'
                with open(loc + r'\recommend_result_top' + str(n) + '.csv', 'a') as f:
                    f.write(info)
        loop -= 1
    


   
