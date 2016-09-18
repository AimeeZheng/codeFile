# -*- coding: utf-8 -*-
"""
Created on Tue Jul 19 09:35:38 2016

@author: zhengyaolin
"""

import pandas as pd
import numpy as np
import os
import time
import math
import random

path = os.getcwd()
act = 'click'
#act = 'onlineplay'
path1 = r'D:\Anaconda_code\migu\contentclick.csv'
path2 = r'F:\data\dmdata\onlineplay.txt'
click_columns = ['IP', 'PLATFORM', 'LOGINTYPE', 'MAIL', 'MEDIAID', 'CONTENTID', 'CONTENTTYPE', 'DTIME', 
                 'PCHANELID', 'COLUMNID', 'CHANNELID', 'CONNECTTYPE', 'CLIENTVERSION', 'GENERATION', 
                 'UA', 'IMSI',  'STATIS_DATE', 'MD5_MSISDN', 'MD5_IMEI']
onlineplay_columns = ['IP', 'PORTAL', 'MAIL', 'MEDIAID', 'DTIME', 'CHANNELID', 'CLIENTVERSION', 
                      'UA', 'CONNECTTYPE', 'IMSI', 'GENERATION', 'CONTENTID', 'STATIS_DATE', 
                      'MD5_MSISDN', 'MD5_IMEI']
                      
def pre(start, end, input_path):
    output_path = os.path.join(path, os.path.normpath('migu/user_item_' + act + '_' + str(start) + '_' + str(end) + '.csv'))
    if act == 'click':
        columns = click_columns
    else:
        columns = onlineplay_columns
    reader = pd.read_csv(input_path, sep=',', names = columns, chunksize = 3000000)
    item_columns = ['CP_ID', 'CONTENT_ID', 'CONTENT_NAME', 'CONTENT_TYPE', 'CONTENT_PRICE', 'UPDATE_TIME',
           'OPUS_TYPE', 'OPUS_ID', 'OPUS_NAME', 'SUBJECT_ID', 'CONTENT_NUM', 'ZONE_ID', 'SEX_ID', 
           'ACOUSTIC_DUB', 'LANGUAGE_ID', 'DEFINITION_ID', 'SPACE_ID', 'COLOR_ID', 'STYLE_ID',
           'GUT_ID', 'SERIAL_ID', 'STORY_ID', 'ORIGINAL_ID', 'TYPE_ID', 'OPUS_PRICE', 'OPUS_UPDATE_TIME']
    content_info = pd.read_csv(r'D:\Anaconda_code\migu\content_opus_list_new.txt', sep = '$', names = item_columns)
    
    for chunk in reader:
        chunk = chunk[chunk['STATIS_DATE'] >= start]
        chunk = chunk[chunk['STATIS_DATE'] <= end]
        chunk = chunk[['MD5_IMEI', 'CONTENTID']]
        chunk.drop_duplicates(inplace = True)
        data = pd.merge(chunk, content_info[['CONTENT_ID', 'OPUS_ID']], left_on = 'CONTENTID', right_on = 'CONTENT_ID', how = 'left')
        data = data[['MD5_IMEI', 'OPUS_ID']]
        chunk.drop_duplicates(inplace = True)
        data.dropna(inplace = True)
        print(act + ' actions:', len(data))
        data.to_csv(output_path, header = False, index = False, encoding = 'utf-8', mode = 'a', float_format = '%d')



def user_act():
    input_path = os.path.join(path, os.path.normpath('migu/contentclick.csv'))
    df = pd.read_csv(input_path, names = ['MD5_IMEI', 'OPUS_ID'], dtype = 'str',encoding='gbk')
    print('--step1-')
    reader=pd.read_csv(input_path, sep=',', names = ['MD5_IMEI', 'OPUS_ID'], chunksize = 3000000,encoding='gbk')
    print('---succeed---')
    for chunk in reader:
        print(time.time())
        chunk.drop_duplicates(inplace = True)#在原来的数据上去重
        chunk.dropna(inplace = True)#在原来的数据上 去除空值
        for user, group in chunk.groupby('MD5_IMEI'):
            info = str(user) + ','
            for opus in group['OPUS_ID']:
                info += str(opus) + '|'
            info = info[:-1] + '\n'
            with open(os.path.join(path, os.path.normpath('migu/user_' + act + '_items.csv')), 'a',encoding= 'gbk') as f:
                f.write(info)
    df.drop_duplicates(inplace = True)
    print('--step2---')
    df.dropna(inplace = True)
    print('--step3--')
    for user, group in df.groupby('MD5_IMEI'):
        print(time.time())
        print(user)
        info = str(user) + ','
        for opus in group['OPUS_ID']:
            info += str(opus) + '|'
        info = info[:-1] + '\n'
        with open(os.path.join(path, os.path.normpath('migu/user_' + act + '_items.csv')), 'a',encoding= 'gbk') as f:
            f.write(info)
    
def item_act():
    input_path = os.path.join(path, os.path.normpath('data/user_item_' + act + '_20160519_20160602.csv'))
    df = pd.read_csv(input_path, names = ['MD5_IMEI', 'OPUS_ID'], dtype = 'str')
    df.drop_duplicates(inplace = True)
    df.dropna(inplace = True)
    for item, group in df.groupby('OPUS_ID'):
        info = str(item) + ','
        for user in group['MD5_IMEI']:
            info += str(user) + '|'
        info = info[:-1] + '\n'
        with open(os.path.join(path, os.path.normpath('data/item_' + act + '_users.csv')), 'a') as f:
            f.write(info)
                                        
def item_count_user():
    input_path = os.path.join(path, os.path.normpath('migu/user_item_' + act + '_20160519_20160602.csv'))
    df = pd.read_csv(input_path, names = ['MD5_IMEI', 'OPUS_ID'], dtype = 'str')
    df.drop_duplicates(inplace = True)
    df.dropna(inplace = True)
    for item, group in df.groupby('OPUS_ID'):
        count = len(group['MD5_IMEI'].unique())
        count_info = str(item) + ',' + str(count) + '\n'
        with open(os.path.join(path, os.path.normpath('migu/item_count_' + act + '_users.csv')), 'a') as g:
           g.write(count_info)
                                 
def users_and_items():
    input_path = os.path.join(path, os.path.normpath('migu/contentclick_test.csv'))
    df = pd.read_csv(input_path, names = ['MD5_IMEI', 'OPUS_ID'],encoding='gbk')
    df.dropna(inplace = True)
    user_list = sorted(df['MD5_IMEI'].unique())
    item_list = sorted(df['OPUS_ID'].unique())
    with open(os.path.join(path, os.path.normpath('migu/users_' + act + '.csv')), 'w',encoding='gbk') as f:
        for i in user_list:
            f.write(i + '\n')
    with open(os.path.join(path, os.path.normpath('migu/items_' + act + '.csv')), 'w',encoding='gbk') as g:
        for i in item_list:
            g.write(str(i) + '\n')



#形成事务矩阵 （数据量过大时不建议使用）  
def transaction():  
    df1 = pd.read_csv(os.path.join(path, os.path.normpath('data/user_' + act + '_items.csv')), names = ['MD5_IMEI', 'items'])
    df2 = pd.read_csv(os.path.join(path, os.path.normpath('data/items_' + act + '.csv')), names = ['OPUS_ID'])
    items = [str(i) for i in sorted(list(df2['OPUS_ID']))]
    #数据量过大 无法直接存储
    data = pd.DataFrame(np.zeros((df1.shape[0], len(items))), columns = items, dtype = np.int64)
    for i, item in enumerate(df1['items']):
        data.ix[i, item.split('|')] = 1
    data.to_csv(os.path.join(path, os.path.normpath('data/transaction_' + act + '.csv')), index = False, header = False)

#计算关联指标 （数据量过大时不建议使用）
def associationRule(X):
    '''
    Parameters
    ----------
    X : array-like or sparse matrix, shape = (n_transactions, n_items)
    '''
    count_t, count_items = X.shape
    x_transpose = np.transpose(X)
    #用来存取每个item的用户数 初始化全0
    item_v = []
    for i in range(count_items):
        item_v.append(0)
        
    for i in range(count_items):
        item_i =  x_transpose[i]
        if item_v[i] == 0:
            n_i = len(item_i.nonzero()[0])
            item_v[i] = n_i
        else:
            n_i = item_v[i]
            
        j = i + 1
        while j < count_items:
            item_j = x_transpose[j]
            if item_v[j] == 0:
                n_j = len(item_j.nonzero()[0])
                item_v[j] = n_j
            else:
                n_j = item_v[j] 
            
            n_i_j = len((item_i & item_j).nonzero()[0])
            #支持度
            support = n_i_j / count_t
            #置信度i->j
            confidence_i = n_i_j / n_i
            #置信度j->i
            confidence_j = n_i_j / n_j
            #余弦值
            cosine = n_i_j / math.sqrt(n_i * n_j)
            #不平衡因子 n_j / n_i
            IR = confidence_i / confidence_j
            
            '''
            #提升度i->j
            lift_i = confidence_i / n_j
            #提升度j->i
            lift_j = confidence_j / n_i
            '''
            
            info = str(i) + '|' + str(j) + '|' + str(n_i) + '|' + str(n_j) + '|' + str(n_i_j) + '|' + str(support) + '|' + str(confidence_i) + '|' + str(confidence_j) + '|' + str(cosine) + '|' + str(IR) + '\n'
            with open(os.path.join(path, os.path.normpath('data/association_rule_results_' + act + '.csv')), 'a') as f:
                f.write(info)
            j += 1
            
#计算共现次数（不用）
def count_concurrent(X, n_matrix):
    '''
    Parameters
    ----------
    X : array-like or sparse matrix, shape = (n_transactions, n_items)
    n_matrix : symmetrical matrix, shape = (n_items, n_items)
    '''
    count_t, count_items = X.shape
    x_transpose = np.transpose(X)
    for i in range(count_items):
        item_i =  x_transpose[i]
        j = i + 1
        while j < count_items:
          item_j = x_transpose[j]
          n_i_j = len((item_i & item_j).nonzero()[0])
          n_matrix[i][j] += n_i_j
    return n_matrix
    
def filt():
#    df = pd.read_csv(os.path.join(path, os.path.normpath('migu/association_rule_results_' + act + '.csv')), sep = '|', names = ['itemA', 'itemB', 'userA', 'userB', 'userAB', 'support', 'confidenceA', 'confidenceB', 'cosine', 'IR'])
#    df = pd.read_csv(os.path.join(path, os.path.normpath('migu/association_rule_results_' + act + '.csv')), sep = '|', names = ['itemA', 'itemB', 'userA', 'userB', 'userAB', 'support', 'confidenceA', 'confidenceB', 'cosine'])
    df = pd.read_csv(os.path.join(path, os.path.normpath('migu/association_rule_results_' + act + '_4.txt')), sep = '|', names = ['itemA', 'itemB', 'support', 'confidenceA', 'confidenceB', 'cosine'])

    #支持度 前90%
    m, n = df.shape
    df.sort_values(by = 'support', inplace = True)
    df = df[int(m * 0.1):]    
    #1.余弦值 > 0.5
    df.sort_values(by = 'cosine', inplace = True)
    df = df[df['cosine'] > 0]
    #df = df[int(m * 0.1):] 
    
    #把一行的数据拆开，A->B  B->A都写在表里  置信度和IR值有变化
    df1 = df[['itemA', 'itemB', 'support', 'confidenceA', 'cosine']]
    df2 = df[['itemB', 'itemA', 'support', 'confidenceB', 'cosine']]
    names = ['itemA', 'itemB', 'support', 'confidence', 'cosine']
    df1.columns = names
    df2.columns = names
    df = pd.concat([df1, df2])
    '''
    #把一行的数据拆开，A->B  B->A都写在表里  置信度和IR值有变化
    df1 = df[['itemA', 'itemB', 'support', 'confidenceA', 'cosine', 'IR']]
    df2 = df[['itemB', 'itemA', 'support', 'confidenceB', 'cosine']]
    df2['IR'] = df['IR'].apply(lambda x : 1 / x)
    names = ['itemA', 'itemB', 'support', 'confidence', 'cosine', 'IR']
    df1.columns = names
    df2.columns = names
    df = pd.concat([df1, df2])
    '''
    #2.IR < 1
#    df = df[df['IR'] < 1]
    
    df.to_csv(os.path.join(path, os.path.normpath('migu/association_rules_filted_' + act + '.csv')),mode='a', sep = '|', index = False)
    
    for item, group in df.groupby('itemA'):
        info = str(item) + '|'
        group.sort_index(by = 'confidence', ascending = False, inplace = True)
        top = group[:100]#推荐100个
        for i, row in top.iterrows():
            info += str(int(row['itemB'])) + '|' + str(row['confidence']) + '|'
        info = info[:-1] + '\n'
        with open(os.path.join(path, os.path.normpath('migu/association_items_' + act + '.csv')), 'a') as f:
            f.write(info) 
            

def calculate():  
    tran_path = os.path.join(path, os.path.normpath('migu/user_' + act + '_items.csv'))
    tran_df = pd.read_csv(tran_path, names = ['user', 'items'])
    item_df = pd.read_csv(os.path.join(path, os.path.normpath('migu/items_' + act + '.csv')), names = ['item'])
    items = sorted(list(item_df['item']))
#   items = list(item_df['item'])
    item_count = item_df.shape[0]
    #存储itemA、B同时出现的次数
    n_i_j_matrix = pd.DataFrame(np.zeros((item_count, item_count)), index = items, columns = items, dtype = np.int64)
    count_t = tran_df.shape[0]
    
    #计算itemA、itemB同时出现的次数
    for i, t_items in enumerate(tran_df['items']):
        print(str(i) + ':', tran_df.ix[i]['user'])
        items_list = sorted([np.int64(x) for x in t_items.split('|')])
        n = len(items_list)
        for i in range(n):
            item_i = items_list[i]
            j = i
            while j < n:
                item_j = items_list[j]
                n_i_j_matrix.loc[item_i, item_j] += 1
                j += 1
    #n_i_j_matrix.to_csv(os.path.join(path, os.path.normpath('migu/items_con' + act + '_matrix.csv')), index_label = 'OPUS_ID') 
    #n_i_j_matrix = pd.read_csv(os.path.join(path, os.path.normpath('migu/items_con' + act + '_matrix.csv')), index_col = 'OPUS_ID')
    #指标计算
    for i in range(item_count):
        item_i = items[i]
        n_i = n_i_j_matrix.loc[item_i, item_i]
        j  = i + 1
        print('i in item_count is %d'%i)
        while j < item_count:
            item_j = items[j]
            n_j = n_i_j_matrix.loc[item_j, item_j]
            n_i_j = n_i_j_matrix.loc[item_i, item_j]
            #支持度
            support = n_i_j / count_t
            #置信度i->j
            confidence_i = n_i_j/ n_i
            #置信度j->i
            confidence_j = n_i_j / n_j
            #提升度
            #lift = n_i_j * count_t / (n_i * n_j)
            #余弦值
            cosine = n_i_j / math.sqrt(n_i * n_j)
            #不平衡因子 confidence_i / confidence_j
            #IR = n_j / n_i
            #info = str(item_i) + '|' + str(item_j) + '|' + str(n_i) + '|' + str(n_j) + '|' + str(n_i_j) + '|' + str(support) + '|' + str(confidence_i) + '|' + str(confidence_j) + '|' + str(cosine) + '\n'#'|' + str(IR) 
            info = str(item_i) + '|' + str(item_j) + '|'   + str(support) + '|' + str(confidence_i) + '|' + str(confidence_j) + '|' + str(cosine) + '\n' 
            #print(info)           
            with open(os.path.join(path, os.path.normpath('migu/association_rule_results_' + act + '.csv')), 'a') as f:
                f.write(info)
            j += 1
            
  
def test():
    num=0
    his_df = pd.read_csv(os.path.join(path, os.path.normpath('migu/user_' + act +'_items.csv')), names = ['MD5_IMEI', 'items'])
    test_df = pd.read_csv(os.path.join(path, os.path.normpath('migu/user_item_' + act +'_20160603_20160605.csv')), names = ['MD5_IMEI', 'OPUS_ID'])
    rule_df = pd.read_csv(os.path.join(path, os.path.normpath('migu/association_rules_filted_' + act +'.csv')), sep = '|')
    test_imei = sorted(test_df['MD5_IMEI'].unique())
    his_df = his_df[his_df['MD5_IMEI'].isin(test_imei)]
    n_pre = 0
    n_test = 0
    n_right = 0
    n = 1
    for user, group in test_df.groupby('MD5_IMEI'):
        print(n, ':', user)
        info = str(user) + ','
        rec_items = set()
        for record in his_df[his_df['MD5_IMEI'] == user]['items']:
            his_items = set([np.int64(i) for i in record.split('|')])
        for i in his_items:
            associate_items = rule_df[rule_df['itemA'] == i][['itemB','confidence']]
            #推荐列表过滤用户历史行为
            associate_items = associate_items[~associate_items['itemB'].isin(his_items)]
            if len(associate_items) != 0:
                associate_items.sort_values(by = 'confidence', inplace = True)
                rec = set(associate_items[:50]['itemB'])
                rec_items = rec_items.union(rec)
        test_items = set(group['OPUS_ID']).difference(his_items)
        rec_items.difference_update(his_items)
        
        if len(rec_items) != 0:
            num +=1
            for i in rec_items:
                info += str(i) + '|'
            info = info[:-1] +'\n'
        else:
            info += '\n'
        with open(os.path.join(path, os.path.normpath('migu/user_item_recommend_' + act +'.csv')), 'a') as f:
            f.write(info)
                    
        n_right += len(test_items & rec_items)
        n_test += len(test_items)
        n_pre += len(rec_items)
        n += 1
        
    #准确率
    precision = n_right / n_pre   
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
    print(num)
            
def get_results():
    item_columns = ['CP_ID', 'CONTENT_ID', 'CONTENT_NAME', 'CONTENT_TYPE', 'CONTENT_PRICE', 'UPDATE_TIME',
           'OPUS_TYPE', 'OPUS_ID', 'OPUS_NAME', 'SUBJECT_ID', 'CONTENT_NUM', 'ZONE_ID', 'SEX_ID', 
           'ACOUSTIC_DUB', 'LANGUAGE_ID', 'DEFINITION_ID', 'SPACE_ID', 'COLOR_ID', 'STYLE_ID',
           'GUT_ID', 'SERIAL_ID', 'STORY_ID', 'ORIGINAL_ID', 'TYPE_ID', 'OPUS_PRICE', 'OPUS_UPDATE_TIME']
    content_info = pd.read_csv(r'D:\Anaconda_code\migu\content_opus_list_new.txt', sep = '$', names = item_columns, index_col = 'OPUS_ID')
    item_info = content_info[['OPUS_NAME','SUBJECT_ID']]
    item_info.drop_duplicates(inplace = True)
    with open(os.path.join(path, os.path.normpath('migu/association_items_' + act+ '.csv'))) as f:
        associate_items = f.readlines()
    item_ids = []
    for i in associate_items:
        items = []
        i_list = i.split('|')
        items.append(i_list.pop(0))
        l_i = len(i_list)
        for j in range(l_i):
            e = i_list.pop(0)
            if j % 2 == 0:
                items.append(e)
        item_ids.append(items)
    for i in item_ids:
        info = ''
        for j in i:
            comic = item_info.ix[np.int64(j)]
            info += comic['OPUS_NAME'] + '(' + comic['SUBJECT_ID'] + ')|'
        info = info[:-1] + '\n'
        with open(os.path.join(path, os.path.normpath('migu/association_items_info_' + act +'.csv')), 'a') as g:
            g.write(info)
        
        
if __name__ == "__main__":
    fileR=open('./migu/migu_result.txt','r')
    fileWT=open('hello.txt','w')
    fileWT1=open('hello111.txt','w')
#    seed='100'
#    random.seed(seed)
    print(random.randint(0,3))    
#    for line in fileR:
#        print(line)
#        if random.randint(0,2)==1:
#            fileWT.write(line)
#        else: 
#            fileWT1.write(line)
#    df1 = pd.read_csv(os.path.join(path, os.path.normpath('migu/user_item_click_20160603_20160605.csv')), names = ['MD5_IMEI', 'OPUS_ID'])
#    del(df1['OPUS_ID'])    
#    df1.to_csv(os.path.join(path, os.path.normpath('migu/temp.csv')), index = False, header = False)
#   改目录
#   1.预处理    输入：contentclick.txt              -->   输出：user_item_click_20160519_20160602.csv
#                    content_opus_list_new.txt    
#    pre(20160519,20160602,path1)
#    pre(20160603,20160605,path1)
#    2.处理统计汇总     
#        输入：user_item_click_20160519_20160602.csv   -->    输出：user_click_items.csv
#        格式：           MD5_IMEI1,OPUS_ID1             
#                         MD5_IMEI1,OPUS_ID2  -->          MD5_IMEI1,OPUS_ID1|OPUS_ID2|OPUS_ID3              
#    user_act()

#    3.矩阵 计算指标
#        输入    user_click_items.csv                        输出 data/items_con_click_matrix.csv(矩阵，可不存)
#                items_click.csv(所有item的表)               association_rule_results_click.csv(要的表，所有结果)
#                                                    item_i|item_j|n_i|n_j|n_i_j|support|confidence_i|confidence_j|cosine|IR
#    users_and_items()    
#    calculate()
#     4.过滤
#         输入：association_rule_results_click.csv           输出 association_rules_filted_click.csv(过滤后剩下的规则) 
#                                                                 itemA|itemB|support|confidence|cosine|IR
#                                                            association_items_click.csv(推荐结果，前100个推荐)
#                                                                itemA|itemB1|confidnce1|itemB2|confidence2|itemB3|confidence3
#   filt()
#    get_results()
#    test()
