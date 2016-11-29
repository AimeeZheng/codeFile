# -*- coding: utf-8 -*-
"""
Created on Mon Aug 15 09:10:22 2016

@author: zhengyaolin
"""

import pandas as pd
import numpy as np
import os
import re

#中间数据路径
root = os.getcwd()
#原始数据路径
path = r'E:\zhengyaolin\互联网电视分析模型\data\家庭成员模型'
info_columns = ['用户ID', '手机号码', '姓名', '性别', '年龄', '婚姻状况', '地市', '区县',
                '联系地址', '居住地址', '用户居住地LAC', '用户居住地CELL', '带宽',  '归属群']
call_columns_orig = ['用户ID', '手机号码', '对方号码', '亲情号码', '通话次数', '通话天数', '通话总时长', '平均通话时长', '闲时通话次数', '闲时通话天数', '闲时通话总时长', '归属群', '群组成员类别角色标识', 'V网短号',
                     '名称', '性别', '年龄', '婚姻状况',  '地市标识', '区县编码', '联系人电话', '联系地址', '邮编', '居住地址', '用户居住地LAC', '用户居住地CELL']
call_columns = ['手机号码', '对方号码', '亲情号码', '通话次数', '通话总时长', '闲时通话次数', '闲时通话总时长']
            
def sampling(source, n = 10000, output = 'output'):
    '''
    对用户进行抽样，抽取10w用户集
    
    Parameters
    ----------
    source：数据源 name of data
    n：样本容量
    output：输出文件名
    '''
    df = pd.read_csv(os.path.join(root, os.path.normpath('data/' + source +'.csv')), sep = '|', names = ['phone_num'], dtype = str)
    phone_number = df['phone_num']
    phone_number.drop_duplicates(inplace = True)
    #抽样
    sample = phone_number.take(np.random.permutation(len(phone_number))[:n])
    sample.to_csv(os.path.join(root, os.path.normpath('data/' + output + '.csv')), index = False, header = False, sep = '|', encoding = 'utf-8')


def is_cmcc(x):
    '''
    判断号码是否是移动的号码
    '''
    phonenum = re.compile('^[1](3[4-9]|4[7]|5[012789]|7[8]|8[23478])[0-9]{8}$')
    match = phonenum.match(x)
    if match:
        return True
    return False

close_code = 'C'
def call_orig():
    '''
    原始通话记录处理（分块）：
    1、亲情号码、家庭v网用户间通话记录筛选
    2、对端号码是本网用户筛选
    3、样本用户集user0通话记录筛选    
    '''
    #通话记录
    reader = pd.read_csv(os.path.join(path, os.path.normpath('201607_sample_user_calls.csv')), sep = '|', names = call_columns_orig, dtype = str, chunksize = 1000000)
    #家庭v网用户信息
    family = pd.read_csv(os.path.join(root, os.path.normpath('data/gitv_user_familyv.csv')), sep = '|', dtype = str)
    #初始用户集user0    
    samples = pd.read_csv(os.path.join(root, os.path.normpath('data/user0.csv')), sep = '|', names = ['手机号码'], dtype = str)    
    user0 = list(samples['手机号码'].unique())
    
    for chunk in reader:
        #亲情号码通话记录
        close_call = chunk[chunk['亲情号码'] == close_code]
        close_call = close_call[['用户ID', '手机号码', '对方号码', '通话次数', '通话天数', '通话总时长', '平均通话时长', '闲时通话次数', '闲时通话天数', '闲时通话总时长']]
        close_call.to_csv(os.path.join(root, os.path.normpath('data/201607_user_close_calls.csv')), sep = '|', index = False, header = False, mode = 'a', encoding = 'utf-8')    
        #家庭v网用户通话记录（同一群）
        v_call = pd.merge(chunk, family, on = ['用户ID', '归属群'],  suffixes=('_x', '_y'), how = 'inner')
        v_call = v_call[['用户ID', '手机号码_x', '对方号码', '亲情号码', '通话次数', '通话天数', '通话总时长', '平均通话时长', '闲时通话次数', '闲时通话天数', '闲时通话总时长', '归属群']]
        v_call.sort_values(by = '用户ID', inplace = True)
        v_call.to_csv(os.path.join(root, os.path.normpath('data/201607_user_familyv_calls.csv')), sep = '|', index = False, header = False, mode = 'a', encoding = 'utf-8')
        #user0通话记录
        user0_call = chunk[chunk['手机号码'].isin(user0)]
        user0_call = user0_call[call_columns]
        user0_call.to_csv(os.path.join(path, os.path.normpath('201607_user0_calls.csv')), sep = '|', index =False,  header = False, mode = 'a', encoding = 'utf-8')
        
        #对端号码筛选  1：移动号码
        chunk = chunk[chunk['对方号码'].apply(is_cmcc)]
        chunk.to_csv(os.path.join(root, os.path.normpath('data/201607_user_calls_cmcc.csv')), sep = '|', index = False, header = False, mode = 'a', encoding = 'utf-8')

call_num_threshold = 8
free_to_all_num_threshold = 0.494
free_to_all_duration_threshold = 0.433
def call_close(userA_call_record, userB):
    '''
    筛选通话记录（样本用户）
    1：移动号码 
    2：通话次数 >= 8
    3：闲时通话次数/通话次数 >= 0.494
    4：闲时通话总时长/通话总时长 >= 0.433
    
    Parameters
    ----------
    userA_call_record：初始用户集的通话记录
    userB：关联用户集 name
    '''
    reader = pd.read_csv(os.path.join(path, os.path.normpath(userA_call_record + '.csv')), sep = '|', names = call_columns, dtype = str, chunksize = 1000000)
    for chunk in reader:
        #对端号码筛选
        df = chunk[['手机号码', '对方号码', '通话次数', '通话总时长', '闲时通话次数', '闲时通话总时长']]
        df.fillna(0, inplace = True)        
        df.replace('\\N', 0, inplace = True)
        df = df[df['对方号码'].apply(is_cmcc)]
        df['通话次数'] = df['通话次数'].apply(int)
        df['闲时通话次数/通话次数'] = df['闲时通话次数'].astype(float)/df['通话次数'].astype(float)
        df['闲时通话总时长/通话总时长'] = df['闲时通话总时长'].astype(float)/df['通话总时长'].astype(float)
        df = df[(df['通话次数'] >= call_num_threshold) & (df['闲时通话次数/通话次数'] >= free_to_all_num_threshold) & (df['闲时通话总时长/通话总时长'] >= free_to_all_duration_threshold)]
        #df.to_csv(os.path.join(root, os.path.normpath('data/201607_' + userB + '_calls_detail.csv')), sep = '|', index = False, header = False, mode = 'a', encoding = 'utf-8')
        df[['手机号码', '对方号码']].to_csv(os.path.join(root, os.path.normpath('data/201607_' + userB + '_calls_set.csv')), sep = '|', index = False, header = False, mode = 'a', encoding = 'utf-8')

def user_associate(user):
    '''
    关联用户集
    
    Parameters
    ----------
    user：关联用户集
    '''
    df = pd.read_csv(os.path.join(root, os.path.normpath('data/201607_' + user + '_calls_set.csv')), sep = '|', names = ['手机号码', '对方号码'], dtype = str)
    users = pd.DataFrame(df['对方号码'].unique())
    users.to_csv(os.path.join(root, os.path.normpath('data/associate_' + user + '.csv')), sep = '|', index = False, header = False, encoding = 'utf-8')

set_name = ['user1', 'user2', 'user3']
def all_pairs():
    #汇总所有二项集：排序、去重
    data = pd.DataFrame()
    for name in set_name:
        df = pd.read_csv(os.path.join(root, os.path.normpath('data/201607_' + name + '_calls_set.csv')), sep = '|', names = ['a', 'b'], dtype = str)
        data = data.append(df)
    for i, row in data.iterrows():
        print('row:', i)
        if row['a'] > row['b']:
            tmp = row['a']
            row['a'] = row['b']
            row['b'] = tmp
    data.drop_duplicates(inplace = True)
    data.sort_values(by = 'a', inplace = True)
    data.to_csv(os.path.join(root, os.path.normpath('data/S2.csv')), sep = '|', index = False, header = False, encoding = 'utf-8')    

def save(out, info):
    '''存储
    
    Parameters
    ----------
    out： output path
    info：list of lists
    '''
    print('saving...')
    df = pd.DataFrame(info)
    df.to_csv(out, mode = 'a', sep = '|', index = False, header = False, encoding = 'utf-8')
     
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
    df = pd.read_csv(os.path.join(root, os.path.normpath('data/S2.csv')), sep = '|', header = None, dtype = str)   
    S2 = []
    for i in np.array(df).tolist():
        S2.append(tuple(i))
    S2_map = dict([(k,1) for k in S2])    
    
    #输入
    if k == 2:
        data = df
    else:
        data = pd.read_csv(os.path.join(root, os.path.normpath('data/S' + str(k) + '.csv')), sep = '|', header = None, dtype = str)
    
    #边跑边存
    output = os.path.join(root, os.path.normpath('data/S' + str(k + 1) + '.csv'))
    
    by = [i for i in range(k - 1)]
    for u, group in data.groupby(by):
        Skp = []
        m = group.shape[0]
        if m != 1:
            sets = np.array(group)
            for i in range(m - 1):
                j = i + 1
                while j < m:
                    set1 = tuple(sets[i])
                    set2 = tuple(sets[j])
                    p = (set1[k - 1], set2[k - 1])
                    if p in S2_map:
                        u = set(set1).union(set(set2))
                        Skp.append(sorted(u))
                        print(u)
                    j += 1
            if len(Skp) > 0:
                save(output, Skp)

def call_and_location():
    '''
    用户通话记录和地址信息
    1、group_id归属群为空
    2、对端号码为移动本网
    
    保留字段：
    |用户号码|对方号码|通话次数|联系地址_y|居住地址_y|归属群_y|联系地址_x|居住地址_x|归属群_x|
    '''
    #通话记录
    reader = pd.read_csv(os.path.join(path, os.path.normpath('201607_sample_user_calls.csv')), sep = '|', names = call_columns_orig, dtype = str, chunksize = 1000000)
    info = pd.read_csv(os.path.join(path, os.path.normpath('iptv_user_info.csv')), sep = '|', names = info_columns, dtype = str)
    info = info[['手机号码', '联系地址', '居住地址', '归属群']]
    
    for chunk in reader:
        chunk = chunk[['手机号码', '对方号码', '通话次数', '联系地址', '居住地址', '归属群']]
        chunk = chunk[chunk['对方号码'].apply(is_cmcc)]
        df = pd.merge(chunk, info, on = '手机号码', how = 'left', suffixes=('_y', '_x'))
        df.to_csv(os.path.join(root, os.path.normpath('data/201607_sample_user_call_location.csv')), sep = '|', index = False, header = False, mode = 'a', encoding = 'utf-8')   
 
invalid_loc = ['null', 'Unknow', 'UnKnow', 'FFFF', '不详', '\\N', '同上', '0', '1']
def valid_lac(x):
    '''
    地址是否有效，有效返回True，否则为False
    地址有效：不为空且长度大于6的字符串
    '''
    if x is not np.nan and type(x) == str and x not in invalid_loc:
        return True
    return False
                     
def test():
    '''
    通话次数>=10
    用户地址相同
    '''
    columns = ['用户号码', '对方号码', '通话次数', '联系地址_y', '居住地址_y', '归属群_y', '联系地址_x', '居住地址_x', '归属群_x']
    df = pd.read_csv(os.path.join(root, os.path.normpath('data/201607_sample_user_call_location.csv')), sep = '|', names = columns, dtype = str)
    df = df[['用户号码', '对方号码', '通话次数', '居住地址_y', '归属群_y', '居住地址_x', '归属群_x']]    
    #通话次数>=10
    df['通话次数'] = df['通话次数'].apply(int)
    df = df[df['通话次数'] >= 10]
    #df.to_csv(os.path.join(root, os.path.normpath('data/test.csv')), sep = '|', index = False, encoding = 'utf-8')
    #居住地址相同的用户
    data = df[df['居住地址_y'] == df['居住地址_x']]
    data = data[~data['居住地址_x'].isin(invalid_loc)][['用户号码', '对方号码', '通话次数', '居住地址_y', '归属群_y', '归属群_x']]
    data.sort_values(by = '用户号码', inplace = True)
    #data.to_csv(os.path.join(root, os.path.normpath('data/same_location_calls.csv')), sep = '|', index = False,header = False, encoding = 'utf-8')  
    family = df[df['归属群_y'] == df['归属群_x']]
    family = family[family['归属群_x'] != '\\N']
    family = family[~((family['居住地址_x'].isin(invalid_loc)) | (family['居住地址_y'].isin(invalid_loc)))]
    
    result = pd.DataFrame()
    for u, group in data.groupby('用户号码'):
        group.sort_values(by = '通话次数', inplace = True)
        result = pd.concat([result, group[:3]])
        #print(len(result))
           
    right = result[result['归属群_y'] == result['归属群_x']]
    right = right[right['归属群_x'] != '\\N']


def all_sets(k = 7):
    '''
    筛选出多项连通集中包含互联网电视用户的集合
    筛选出多项连通集中包含互联网电视用户中订购家庭v网业务的集合
    
    '''
    user0 = pd.read_csv(os.path.join(root, os.path.normpath('data/user0.csv')), sep = '|', header = None, dtype = str)
    iptv_user0 = sorted(list(user0[0]))
    info = pd.read_csv(os.path.join(path, os.path.normpath('sample_user_info.csv')), sep = '|', header = None, dtype = str)
    info = info[[2,24]]
    info.columns = ['phone_num', 'group_id']
    info = info[info['phone_num'].isin(iptv_user0)]
    iptv_user0_family = sorted(info[info['group_id'] != '\\N']['phone_num'].unique())
    
    for i in range(3, 8):
        df = pd.read_csv(os.path.join(root, os.path.normpath('data/S' + str(i) + '.csv')), sep = '|', header = None, dtype = str)
        data = df[df[0].isin(iptv_user0)]        
        for j in range(1, i):
            data = pd.concat([data, df[df[j].isin(iptv_user0)]])
        data.drop_duplicates(inplace = True)
        if len(data) > 0:
            data.to_csv(os.path.join(root, os.path.normpath('data/S' + str(i) + '_iptv.csv')), sep = '|', index = False, header = False, encoding = 'utf-8')
  
    for i in range(3, 8):
        df = pd.read_csv(os.path.join(root, os.path.normpath('data/S' + str(i) + '.csv')), sep = '|', header = None, dtype = str)
        data = df[df[0].isin(iptv_user0_family)]        
        for j in range(1, i):
            data = pd.concat([data, df[df[j].isin(iptv_user0_family)]])
        data.drop_duplicates(inplace = True)
        if len(data) > 0:
            data.to_csv(os.path.join(root, os.path.normpath('data/S' + str(i) + '_iptv_family.csv')), sep = '|', index = False, header = False, encoding = 'utf-8')

def location_filt(k = 2):
    '''
    筛选出互联网电视用户的k项集合中地址信息相同的集合
    '''
    df = pd.read_csv(os.path.join(root, os.path.normpath('data/iptv_set' + str(k) + '_location.csv')), sep = '|', header = None, dtype = str, error_bad_lines = False)
    location_columns = [i for i in range(1, k * 2, 2)]
    for i in range(k):
        col1 = location_columns[i]
        j = i + 1
        while j < k:
            col2 = location_columns[j]
            df = df[df[col1] == df[col2]]
            j += 1
    df = df[~df[1].isin(invalid_loc)]
    df = df[[i for i in range(0, k * 2, 2)] + [1]]
    data = df[[i for i in range(0, k * 2, 2)]]
    print('filted:', len(df))
    if len(df) > 0:
        data.to_csv(os.path.join(root, os.path.normpath('data/iptv_set' + str(k) + '_filted.csv')), sep = '|', index = False, header = False, encoding = 'utf-8')
        df.to_csv(os.path.join(root, os.path.normpath('data/iptv_set' + str(k) + '_location_filted.csv')), sep = '|', index = False, header = False, encoding = 'utf-8')
 
def evaluate(k = 2):
    '''
    评估：判断k项集中各用户家庭v网group_id情况
    
    Parameters
    ----------
    k：k项集
    '''
    df = pd.read_csv(os.path.join(root, os.path.normpath('data/iptv_set' + str(k) + '_filted_group_id.csv')), sep = '|', header = None, dtype = str)
    group_id_columns = [i for i in range(1, k * 2, 2)]
    for i in range(k):
        col1 = group_id_columns[i]
        j = i + 1
        while j < k:
            col2 = group_id_columns[j]
            df = df[df[col1] == df[col2]]
            j += 1
    print('null:', len(df[df[1] == '\\N']))
    df = df[df[1] != '\\N'] 
    print('right:', len(df))
    if len(df) > 0:
        df.to_csv(os.path.join(root, os.path.normpath('data/iptv_set' + str(k) + '_filted_right.csv')), sep = '|', index = False, header = False, encoding = 'utf-8')
    
def run():
    #call_close('201607_user2_calls', 'user3')
    #user_associate('user2')
    #all_pairs()
    #clustering_BDP(k = 3)
    #call_and_location()
    evaluate(3)
    pass
    
if __name__ == "__main__":  
    run()          
        