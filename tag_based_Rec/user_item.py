# -*- coding: utf-8 -*-
"""
Created on Tue Jun 21 11:05:46 2016

@author: zhengyaolin
@description: 用户行为统计计算
"""

import pandas as pd
import numpy as np
import os

"""
Parameters
--------
loc：root path of data

"""
path = os.getcwd()
loc = os.path.join(path, os.path.normpath('data'))

#information for content
content_info = pd.read_csv(loc + '\content_opus_list_add.csv')

#统计用户行为并存储
def saveInfos(data, path):
    user_group = data.groupby('MD5_IMEI')
    for user, user_item in user_group:
        info = ''
        #print(user)
        item_group = user_item.groupby('OPUS_ID')
        for item, record in item_group:
            #print(int(item))
            count = len(record)
            if count > 0:
                info += str(user) + ',' + str(int(item)) + ',' + str(count) + '\n'
        with open(path, 'a') as f:
            f.write(info)
         
#统计用户收藏动漫行为
def count_collect(start, end):
    """
    start: start date
    end: end date
    """
    collect_columns = ['IP', 'PORTAL', 'MAIL', 'MEDIAID', 'DTIME', 'CHANNELID', 'CLIENTVERSION', 
                        'UA', 'CONNECTTYPE', 'IMSI', 'GENERATION', 'OPUSID', 'OPERTYPE', 'STATIS_DATE', 
                        'MD5_MSISDN', 'MD5_IMEI']
    data = pd.read_csv(loc + r'\contentcollect.csv', header = None, names = collect_columns)
    data = data.drop(['IP', 'PORTAL', 'MAIL', 'MEDIAID', 'CHANNELID', 'CLIENTVERSION', 'UA', 'CONNECTTYPE', 'IMSI', 'GENERATION', 'MD5_MSISDN'], axis = 1) 
    data = data[data['STATIS_DATE'] >= start]
    data = data[data['STATIS_DATE'] <= end]
    output_path = loc + r'\user_item_collect_' + str(start) + '_' + str(end) + '.csv'   
    user_group = data.groupby('MD5_IMEI')
    for user, item_collect in user_group:
        info = ''
        #print(user)
        content_group = item_collect.groupby('OPUSID')
        for item, collect in content_group:
            #print(item)
            count = len(collect[collect['OPERTYPE'] == 1]) - len(collect[collect['OPERTYPE'] == 2])
            if count > 0:
                info += str(user) + ',' + str(item) + ',' + str(count) + '\n'
        with open(output_path, 'a') as f:
            f.write(info)

#统计用户下载动漫行为
def count_download(start, end):
    download_columns = ['IP', 'PORTAL', 'MAIL', 'MEDIAID', 'DTIME', 'CHANNELID', 'CLIENTVERSION', 
                        'UA', 'CONNECTTYPE', 'IMSI', 'GENERATION', 'CONTENTID', 'STATIS_DATE', 
                        'MD5_MSISDN', 'MD5_IMEI']
    data = pd.read_csv(loc + r'\contentdownload.csv', header = None, names = download_columns)
    data = data.drop(['IP', 'PORTAL', 'MAIL', 'MEDIAID', 'CHANNELID', 'CLIENTVERSION', 'UA', 'CONNECTTYPE', 'IMSI', 'GENERATION', 'MD5_MSISDN'], axis = 1)
    data = data[data['STATIS_DATE'] >= start]
    data = data[data['STATIS_DATE'] <= end]    
    temp = pd.merge(data, content_info, left_on = 'CONTENTID', right_on = 'CONTENT_ID', how = 'left')
    output_path = loc + r'\user_item_download_' + str(start) + '_' + str(end) + '.csv'
    saveInfos(temp, output_path)

#统计用户在线观看动漫行为
def count_onlinclick(start, end):
    onlineplay_columns = ['IP', 'PORTAL', 'MAIL', 'MEDIAID', 'DTIME', 'CHANNELID', 'CLIENTVERSION', 
                        'UA', 'CONNECTTYPE', 'IMSI', 'GENERATION', 'CONTENTID', 'STATIS_DATE', 
                        'MD5_MSISDN', 'MD5_IMEI']
    data = pd.read_csv(loc + r'\onlineplay.csv', header = None, names = onlineplay_columns)    
    data = data.drop(['IP', 'PORTAL', 'MAIL', 'MEDIAID', 'CHANNELID', 'CLIENTVERSION', 'UA', 'CONNECTTYPE', 'IMSI', 'GENERATION', 'MD5_MSISDN'], axis = 1)
    data = data[data['STATIS_DATE'] >= start]
    data = data[data['STATIS_DATE'] <= end]    
    temp = pd.merge(data, content_info, left_on = 'CONTENTID', right_on = 'CONTENT_ID', how = 'left')
    output_path = loc + r'\user_item_onlineplay_' + str(start) + '_' + str(end) + '.csv'
    saveInfos(temp, output_path)

#统计用户点击动漫行为
def count_click(start, end):
    click_columns = ['IP', 'PLATFORM', 'LOGINTYPE', 'MAIL', 'MEDIAID', 'CONTENTID', 'CONTENTTYPE', 'DTIME', 
                     'PCHANELID', 'COLUMNID', 'CHANNELID', 'CONNECTTYPE', 'CLIENTVERSION', 'GENERATION', 
                     'UA', 'IMSI',  'STATIS_DATE', 'MD5_MSISDN', 'MD5_IMEI']
    path = loc + r'\contentclick.csv'
    data = pd.read_csv(path, header = None, names = click_columns)
    data = data.drop(['IP', 'PLATFORM', 'LOGINTYPE', 'MAIL', 'MEDIAID', 'CONTENTTYPE', 'PCHANELID', 'COLUMNID', 
                      'CHANNELID', 'CONNECTTYPE', 'CLIENTVERSION', 'GENERATION', 'UA', 'IMSI', 'MD5_MSISDN'], axis = 1)
    data = data[data['STATIS_DATE'] >= start]
    data = data[data['STATIS_DATE'] <= end]
    temp = pd.merge(data, content_info, left_on = 'CONTENTID', right_on = 'CONTENT_ID', how = 'left')
    output_path = loc + r'\user_item_click_' + str(start) + '_' + str(end) + '.csv'
    saveInfos(temp, output_path)

#用户-动漫  用户行为合并
def user_item_gather(start, end):
    df1 = pd.read_csv(loc + r'\user_item_collect_' + str(start) + '_' + str(end) + '.csv', header = None, names = ['MD5_IMEI', 'OPUS_ID','collect'])
    df2 = pd.read_csv(loc + r'\user_item_download_' + str(start) + '_' + str(end) + '.csv', header = None, names = ['MD5_IMEI', 'OPUS_ID','download'])
    df3 = pd.read_csv(loc + r'\user_item_onlineplay_' + str(start) + '_' + str(end) + '.csv', header = None, names = ['MD5_IMEI', 'OPUS_ID','onlineplay'])
    df4 = pd.read_csv(loc + r'\user_item_click_' + str(start) + '_' + str(end) + '.csv', header = None, names = ['MD5_IMEI', 'OPUS_ID','click'])
    df = pd.merge(df1, df2, on = ['MD5_IMEI', 'OPUS_ID'], how = 'outer')
    df = pd.merge(df, df3, on = ['MD5_IMEI', 'OPUS_ID'], how = 'outer')
    df = pd.merge(df, df4, on = ['MD5_IMEI', 'OPUS_ID'], how = 'outer')
    df.fillna(0, inplace = True)
    #df['like'] = df['collect'] + df['download']
    df[['OPUS_ID', 'collect', 'download', 'onlineplay', 'click']] = df[['OPUS_ID', 'collect', 'download', 'onlineplay', 'click']].astype(np.int64)
    output_path = loc + r'\user_item_gather_' + str(start) + '_' + str(end) + '.csv'    
    df.to_csv(output_path, index = False)

#提取兴趣标签:去重、合并
def user_interest():
    interest = pd.read_csv(loc + r'\userinterest.csv', header = None)
    interest = interest[[11,14]]
    interest.columns = ['interestname', 'MD5_IMEI']
    interest = interest.drop_duplicates()
    for user, user_group in interest.groupby('MD5_IMEI'):
        info = str(user) + ','
        tags = set()
        for i in user_group['interestname']:
            tag = i.split(':')
            for j in tag:
                tags.add(j)
        for t in tags:
            info += str(t) + '|'
        info = info[:-1] + '\n'
        with open(loc + r'\user_tag_interest.csv', 'a') as f:
            f.write(info)

#用户-动漫 矩阵生成
"""
Parameters
----------
users: list of imei(sorted)
items: list of opus_id(sorted)
path: input path of data
"""
def user_item_matrix(users, items, input_path, output_path):
    df = pd.read_csv(input_path, names = ['MD5_IMEI', 'OPUS_ID', 'count'])
    data = pd.DataFrame(np.zeros((len(users), len(items))), columns = items)
    data.index = users
    m = df.shape[0]
    for i in range(m):
        user = df.ix[i]['MD5_IMEI']
        item = df.ix[i]['OPUS_ID']
        n = df.ix[i]['count']
        data.ix[user, item] = n
        print(user, item, n)
    data.to_csv(output_path, float_format = '%d')    