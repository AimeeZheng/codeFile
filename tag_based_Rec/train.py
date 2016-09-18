# -*- coding: utf-8 -*-
"""
Created on Sun Jun 26 13:48:11 2016

@author: zhengyaolin
@description: 计算输入指标
"""

import pandas as pd
import user_item
import numpy as np
import os

path = os.getcwd()
loc = os.path.join(path, os.path.normpath('data'))
tag_all = ['情感', '宅男', '科幻', '悬疑', '经典', '热血', '穿越', '玄幻', '国学', '搞笑', '都市', '民俗', '校园',
       '武侠', '恐怖', '宫廷', '冒险', '运动', '萌系', '战争', '恋爱', '耽美', '魔法', '亲子']

def user_act(start, end):
    user_item.count_collect(start, end)
    user_item.count_download(start, end)
    user_item.count_onlinclick(start, end)
    user_item.count_click(start, end)
    user_item.user_item_gather(start, end)
    
#users for test
imei_df = pd.read_csv(loc + r'\TRAIN_IMEI.csv')
users = sorted(imei_df['MD5_IMEI'].unique())

#items 
item_df = pd.read_csv(loc + r'\items.csv')
items = sorted(list(item_df['OPUS_ID']))

#统计用户收藏、下载、点击、观看行为
def count():
    train_start = 20160519
    train_end = 20160602
    user_act(train_start, train_end)
    test_start = 20160603
    test_end = 20160605
    user_act(test_start, test_end)

#生成用户-动漫 各行为矩阵
def user_item(act_type):
    input_path = loc + r'\user_item_' + act_type + '_20160519_20160602.csv'
    output_path = loc + r'\user_item_' + act_type + '_matrix.csv'
    user_item.user_item_matrix(users, items, input_path, output_path)
    
#标签 t 打过物品 i 的次数
def count_tag_item(act_type):
    i_t = pd.read_csv(loc + r'\item_tag_matrix.csv', index_col = 'OPUS_ID')
    u_i = pd.read_csv(loc + r'\user_item_' + act_type + '_20160519_20160602.csv',  names = ['MD5_IMEI', 'OPUS_ID', 'count'])
    u_i.drop_duplicates(inplace = True)    
    u_i = u_i[u_i['OPUS_ID'].isin(items)]
    df = pd.DataFrame(np.zeros((len(items), 1)), index = items, columns = ['count'])
    for item, item_group in u_i.groupby('OPUS_ID'):
        count = item_group['count'].sum()
        df.ix[item]['count'] = count
    df['count'] += 1
    data = i_t.mul(df['count'], axis = 0) 
    data.to_csv(loc + r'\item_tag_' + act_type + '.csv', encoding = 'utf-8', float_format = '%d')

#标注过物品i的用户数
def count_itemUsers(act_type):
    u_i = pd.read_csv(loc + r'\user_item_' + act_type + '_20160519_20160602.csv',  names = ['MD5_IMEI', 'OPUS_ID', 'count'])
    u_i.drop_duplicates(inplace = True)    
    u_i = u_i[u_i['OPUS_ID'].isin(items)]
    df = pd.DataFrame(np.zeros((len(items), 1)), index = items, columns = ['count'])
    for item, item_group in u_i.groupby('OPUS_ID'):
        count_users = item_group['count'].count()
        df.ix[item]['count'] = count_users
    df['count'] += 1
    df.to_csv(loc + r'\item_count_user_' + act_type + '.csv', index_label = 'OPUS_ID', encoding = 'utf-8', float_format = '%d')
    
#使用过标签t的用户数
def count_tagUsers(act_type):
    reader = pd.read_csv(loc + r'\user_item_' + act_type + '_matrix.csv', index_col = 0, chunksize = 1000)
    df =  pd.read_csv(loc + r'\item_tag_matrix.csv', index_col = 'OPUS_ID')
    y = np.array(df)
    count = np.array(np.zeros(83), dtype = int)
    for chunck in reader:
        x = np.array(chunck)
        z = x.dot(y)
        m = len(z)
        for t in range(83):
            for i in range(m):
                if z[i][t] > 0:
                    count[t] += 1
        print(count)
    tags = list(df.columns)
    data = pd.DataFrame(count)
    data.index = tags
    data.columns = ['count']
    data.to_csv(loc + r'\tag_count_user_' + act_type + '.csv', index_label = 'tag')

#计算用户兴趣标签
def interest():
    df = pd.read_csv(loc + r'\user_tag_interest_matrix.csv', index_col = 'MD5_IMEI', encoding = 'gbk')
    tags = list(df.columns)
    data = pd.DataFrame(np.zeros((len(tag_all), 1)), index = tag_all, columns = ['count'])
    for t in tags:
        data.ix[t]['count'] = len(df[df[t] > 0])
    data.to_csv(loc + r'\tag_count_user_interest.csv', index_label = 'tag', encoding = 'utf-8', float_format = '%d')

def user_interest_tag():
    data = pd.DataFrame(users, columns = ['MD5_IMEI'])
    df = pd.read_csv(loc + r'\user_tag_interest_matrix.csv', index_col = 'MD5_IMEI', encoding = 'gbk')
    data = pd.merge(data, df, on = 'MD5_IMEI', how = 'left')
    data = data.fillna(0)
    d = data.drop('MD5_IMEI', axis = 1)
    d = d.reindex(columns = tag_all)
    d = d.fillna(0)
    df = pd.concat([data['MD5_IMEI'],d], axis = 1)
    df.to_csv(loc + r'\user_tag_like_matrix.csv', index = False, encoding = 'utf-8', float_format = '%d')




    