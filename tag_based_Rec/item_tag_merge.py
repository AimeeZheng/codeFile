# -*- coding: utf-8 -*-
"""
Created on Wed Jun 22 11:07:53 2016

@author: zhengyaolin
@description：生成动漫标签全集（动漫属性+外站）—— 暂时不用
"""

import pandas as pd
import numpy as np

content_info = pd.read_csv(r'G:\pythonWork\recommendation\data\content_opus_list_add.csv')
#动漫unique
content_info = content_info.drop_duplicates('OPUS_ID')
#滤除theme类型
content_info = content_info[content_info['OPUS_TYPE'] != 'theme']
#按顺序生成items集
items = content_info[['OPUS_ID','OPUS_NAME']]
items = items.sort_index(by = 'OPUS_ID')
items.to_csv(r'G:\pythonWork\recommendation\data\items.csv', index = False, encoding = 'utf-8')

content_info = content_info.drop(['CP_ID', 'CONTENT_ID', 'CONTENT_NAME', 'CONTENT_TYPE', 'CONTENT_PRICE', 'UPDATE_TIME',
           'CONTENT_NUM', 'ZONE_ID', 'ACOUSTIC_DUB', 'DEFINITION_ID', 'GUT_ID', 'STORY_ID', 'ORIGINAL_ID', 'OPUS_UPDATE_TIME',
           'ac_name', 'ac_author', 'ac_score', 'ac_comment_num'], axis = 1)
content_info = content_info.fillna('')
tag_columns = ['OPUS_TYPE', 'SUBJECT_ID', 'SEX_ID', 'LANGUAGE_ID', 'SPACE_ID', 'COLOR_ID', 'STYLE_ID',
           'SERIAL_ID', 'TYPE_ID']
#定义标签全集
tags_all_df = pd.read_csv(r'G:\pythonWork\recommendation\data\tags.csv', header = None, encoding = 'gbk')
tags_all = set(t for t in tags_all_df[0])
#合并标签
m, n = content_info.shape
content_info.index = range(m)
for i in range(m):
    book = content_info.ix[i]
    info = str(book['OPUS_ID']) + ',"' + str(book['OPUS_NAME']) + '",'
    price = book['OPUS_PRICE']
    if price <= 20:
        price_tag = '价格低'
    elif price <= 40:
        price_tag = '价格较低'
    elif price <= 60:
        price_tag = '价格中等'
    elif price <= 80:
        price_tag = '价格较高'
    else:
        price_tag = '价格高' 
    tag_iter = (set(book[t].split('|')) for t in tag_columns)
    tags = set.union(*tag_iter)
    #invalid_tags = set(['', '其他', '其它', '未知', '5040'])
    #tags = tags - invalid_tags
    tags.add(price_tag)
    print('dm tags:', tags)
    #外站标签
    tags_add = set(book['ac_type'].split(','))
    print('qq tags:', tags_add)
    tags = tags | tags_add
    tags = tags & tags_all
    print('final tags:', tags)
    for t in tags:
        info += t + '|'
    info = info[:-1] + '\n'
    with open(r'G:\pythonWork\recommendation\data\item_tag.csv', 'a') as f:
        f.write(info)


#生成item-tag矩阵
df = pd.read_csv(r'G:\pythonWork\recommendation\data\item_tag.csv', names = ['OPUS_ID', 'OPUS_NAME', 'tag'], encoding = 'gbk')
m = df.shape[0]
tag_columns = sorted(tags_all)
dummies = pd.DataFrame(np.zeros((m, len(tags_all))), columns = tag_columns)
for i, tag in enumerate(df['tag']):
    dummies.ix[i, tag.split('|')] = 1
data = df.join(dummies)
data = data.drop(['tag', '咨讯'], axis = 1)
data.to_csv(r'G:\pythonWork\recommendation\data\item_tag_matrix.csv', index = False, float_format = '%d', encoding = 'utf-8')
