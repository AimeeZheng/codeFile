# -*- coding: utf-8 -*-
"""
Created on Fri Jun 17 13:41:50 2016

@author: zhengyaolin
@description: 外站标签合并
"""

import pandas as pd
import os

path = os.getcwd()
#腾讯动漫
qqac = pd.read_csv('G:\data\qqac\\ac.csv')
qqac = qqac.drop_duplicates('ac_name')
#tag
ac_tag = qqac['ac_type']
qq = qqac[['ac_name', 'ac_type', 'ac_author', 'ac_score', 'ac_comment_num']]

#咪咕动漫
columns = ['CP_ID', 'CONTENT_ID', 'CONTENT_NAME', 'CONTENT_TYPE', 'CONTENT_PRICE', 'UPDATE_TIME',
           'OPUS_TYPE', 'OPUS_ID', 'OPUS_NAME', 'SUBJECT_ID', 'CONTENT_NUM', 'ZONE_ID', 'SEX_ID', 
           'ACOUSTIC_DUB', 'LANGUAGE_ID', 'DEFINITION_ID', 'SPACE_ID', 'COLOR_ID', 'STYLE_ID',
           'GUT_ID', 'SERIAL_ID', 'STORY_ID', 'ORIGINAL_ID', 'TYPE_ID', 'OPUS_PRICE', 'OPUS_UPDATE_TIME']

data = pd.read_csv('G:\data\dmdata\content_opus_list_new.txt', sep = '$', header = None, names = columns)
data = data.drop_duplicates('OPUS_NAME')

#重合部分
df = pd.merge(data, qq, left_on = 'OPUS_NAME', right_on = 'ac_name')
df.to_csv(os.path.join(path, os.path.normpath('data\merge_dm_qq.csv')), index = False)

#可添加外站标签集
tag_add = set()
for i in df['ac_type']:
    tags = i.split(',')
    for j in tags:
        tag_add.add(j)
tag_add.remove('')
with open(os.path.join(path, os.path.normpath('data\ac_tags.csv')), 'w') as f:
    tag_str = ''
    for i in tag_add:
        tag_str += str(i) + ','
    f.write(tag_str)

#匹配、合并表
df = pd.merge(data, qq, left_on = 'OPUS_NAME', right_on = 'ac_name', how = 'left')
df.to_csv(os.path.join(path, os.path.normpath('data\content_opus_list_add.csv')), index = False, encoding = 'utf-8')
