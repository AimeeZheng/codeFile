# -*- coding: utf-8 -*-
"""
Created on Mon Aug  8 15:15:45 2016

@author: zhengyaolin
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

'''全局设置'''
plt.style.use('ggplot')
root = os.getcwd()
#指定默认字体
yh = mpl.font_manager.FontProperties(fname='D:/Program Files (x86)/Anaconda3/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/msyh.ttc')
#颜色
colors = ['b', 'g', 'r', 'c', 'm', 'y']

#柱状图：标签
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x(), 500 + height, "%s" % int(height))

#绘制地市分布柱状图
def city_bar(labels, height):
    title = plt.title('用户地市分布柱状图', fontproperties = yh)
    title.set_fontsize(15)
    title.set_position((0.5, 1.05))
    print(title.get_position())
    plt.xlabel('地级市', fontproperties = yh)
    plt.ylabel('用户数', fontproperties = yh)
    plt.axis([-1, 14, 0, 50000])
    plt.xticks([i for i in range(len(labels))], labels, fontproperties = yh)
    chart = plt.bar(left = [i for i in range(len(labels))], height = height, width = 0.8, align = 'center')
    autolabel(chart)
    plt.show()

#绘制饼状图
def draw_pie(labels, x, title):
    title = plt.title(title, fontproperties = yh)
    title.set_fontsize(15)
    title.set_position((0.5, 1.05))
    color = [colors[i % len(colors)] for i in range(len(labels))]
    patches, l_text , p_text = plt.pie(x, radius = 1, colors = color, labels = labels, labeldistance = 1.05, autopct = '%1.2f%%', pctdistance = 0.75)    
    for t in l_text:
        t.set_fontproperties(yh)
    plt.axis('equal')
    plt.show()
    
#地市分布(所有用户)
def city_distribution(users):
    '''
    Parameters:
        users: user city info (DataFrame)
    '''
    location = []
    count = []
    for loc, group in users.groupby(['市']):
        n = len(group['宽带账号'].unique())
        location.append(loc)
        count.append(n)
        print(loc, n)
    #绘图
    draw_pie(location, count, '用户地市分布饼状图')
    #plt.savefig('E:\zhengyaolin\互联网电视分析模型\银河_互联网电视用户地市分布饼状图.png')
    #plt.clf()
    #city_bar(location, count)

#判断是否是市区
def is_city(x):
    if '市区' in x:
        return True
    return False
    
def city_or_county(users):
    city = users[users['地市'].apply(is_city)]
    county =  users[~users['地市'].apply(is_city)]  
    location = ['市区', '县']
    count = [len(city['宽带账号'].unique()), len(county['宽带账号'].unique())]
    draw_pie(location, count, '用户地域分布')    

#性别分布
def gender_distribution(users):
    men = users[users['性别'] == '男']
    women = users[users['性别'] == '女']
    other = users[users['性别'] == '不详']
    labels = ['男', '女', '不详']
    count = [len(men['宽带账号'].unique()), len(women['宽带账号'].unique()), len(other['宽带账号'].unique())]
    draw_pie(labels, count, '用户性别分布图')   

#年龄是否合法：True if not valid
def invalid_age(x):
    if x <= 0 or x > 120:
        return True
    return False

#实际有效年龄段 [15,80]
def age_filt(x):
    if x >= 15 and x <= 80:
        return True
    return False
    
#年龄分布
def age_distribution(users):
    valid = users[~users['年龄'].apply(invalid_age)]
    #柱状图
    age = []
    count = []
    for i, group in valid.groupby('年龄'):
        n = len(group['宽带账号'].unique())
        age.append(i)
        count.append(n)
        print(i, n)
    title = plt.title('用户年龄分布柱状图', fontproperties = yh)
    title.set_fontsize(15)
    title.set_position((0.5, 1.05))
    plt.xlabel('年龄', fontproperties = yh)
    plt.ylabel('用户数', fontproperties = yh)
    #plt.axis([0, 120, 0, 20000])
    #plt.xticks([i * 5 for i in range(25)], [i * 5 for i in range(25)])
    #plt.bar(left = age, height = count, width = 0.3, align = 'center')
    plt.axis([15, 80, 0, 5500])
    plt.xticks([i * 5 for i in range(3, 17)], [i * 5 for i in range(3, 17)])
    plt.bar(left = age[14:80], height = count[14:80], width = 0.3, align = 'center')
    
#年龄层分布图：分段柱状图、饼状图
def age_group_distribution(users):
    valid = users[~users['年龄'].apply(invalid_age)]
    mask = valid['年龄'].apply(age_filt)
    labels = ['青少年', '青壮年','中年', '中老年', '老年']
    patch_men, patch_women, patch_other = age_sex_group(valid[mask])
    count = [x + y + z for x, y, z in zip(patch_men, patch_women, patch_other)]
    draw_pie(labels, count, '用户年龄层分布图')
    #plt.savefig('E:\zhengyaolin\互联网电视分析模型\银河_互联网电视用户年龄层分布饼状图.png')
    plt.clf()
    #print(count, patch_men, patch_women, patch_other)
    title = plt.title('用户年龄分布柱状图', fontproperties = yh)
    title.set_fontsize(15)
    title.set_position((0.5, 1.05))
    plt.xlabel('年龄层', fontproperties = yh)
    plt.ylabel('用户数', fontproperties = yh)
    plt.axis([-1, 5, 0, 65000])
    plt.xticks([i for i in range(len(labels))], labels, fontproperties = yh)
    b1 = plt.bar(left = [i for i in range(len(labels))], height = patch_men, color = 'g', width = 0.6, align = 'center', linewidth = 0)
    b2 = plt.bar(left = [i for i in range(len(labels))], height = patch_women, bottom = patch_men, color = 'y', width = 0.6, align = 'center', linewidth = 0)
    b3 = plt.bar(left = [i for i in range(len(labels))], height = patch_other, bottom = [x + y for x, y in zip(patch_men, patch_women)], color = 'b', width = 0.6, align = 'center', linewidth = 0)
    legend = plt.legend((b1[0], b2[0], b3[0]), ('男', '女', '不详'))
    for t in legend.get_texts():
        t.set_fontproperties(yh)
    #plt.savefig('E:\zhengyaolin\互联网电视分析模型\银河_互联网电视用户年龄性别交叉分布图.png')    

def age_sex_group(users):
    sex = ['男', '女', '不详']
    age = [18, 35, 45, 60]
    user = []
    for i in sex:
        user.append(users[users['性别'] == i])
    x = []
    for i in range(len(user)):
        u = user[i]
        p = []
        p.append(len(u[u['年龄'] <= age[0]]['宽带账号'].unique()))
        p.append(len(u[u['年龄'] > age[0]][u['年龄'] <= age[1]]['宽带账号'].unique()))
        p.append(len(u[u['年龄'] > age[1]][u['年龄'] <= age[2]]['宽带账号'].unique()))
        p.append(len(u[u['年龄'] > age[2]][u['年龄'] <= age[3] ]['宽带账号'].unique()))
        p.append(len(u[u['年龄'] > age[3]]['宽带账号'].unique()))
        x.append(p)
    return x
        
#带宽分布
def bandwidth_distribution(users):
    users = users[users['带宽（M）'] != -1]
    labels = ['<10M', '10M', '20M', '30M', '50M', '100M']
    band = []
    count = []
    for b, group in users.groupby('带宽（M）'):
        band.append(b)
        count.append(len(group['宽带账号'].unique()))
    #print(band, count)
    n = []
    n.append(count[0] + count[1])
    n.extend(count[2:])
    print(labels, n)
    draw_pie(labels, n, '用户宽带分布图')
    plt.savefig('E:\zhengyaolin\互联网电视分析模型\银河_互联网电视用户宽带分布饼状图.png')
    
#每户月平均收入分布
def arpu_distribution(users):
    arpu_max = round(users['arpu'].max(), 2)
    #arpu_min = round(users['arpu'].min(), 2)
    arpu = [i * 10 for i in range(int(arpu_max / 10) + 1)]
    #labels = ['[' + str(arpu[i]) + ',' + str(arpu[i + 1]) + ')' for i in range(len(arpu) - 1)]
    count = []
    #[a,b)区间
    for i in range(len(arpu) - 1):
        a = arpu[i]
        b = arpu[i + 1]
        n = len(users[(users['arpu'] >= a) & (users['arpu'] < b)]['宽带账号'].unique())
        count.append(n)
    labels = [i * 100 for i in range(len(count))]
    #print(np.array(count).max())
    title = plt.title('用户ARPU分布图', fontproperties = yh)
    title.set_fontsize(15)
    title.set_position((0.5, 1.05))
    plt.xlabel('arpu', fontproperties = yh)
    plt.ylabel('用户数', fontproperties = yh)
    '''全量
    plt.axis([-1, len(arpu), 0, (int(np.array(count).max() / 100) + 1) * 100])
    plt.xticks([i * 10 for i in range(int(len(count) / 10) + 1)], labels, fontproperties = yh)
    plt.bar(left = [i for i in range(len(count))], height = count, width = 0.6, align = 'center', linewidth = 0)
    '''
    #<400  >98%的用户
    arpu = [i * 10 for i in range(int(400 / 10) + 1)]
    count = count[:len(arpu) - 1]
    labels = ['[' + str(arpu[i]) + ',' + str(arpu[i + 1]) + ')' for i in range(len(arpu) - 1)]
    #plt.axis([-1, len(arpu) + 1, 0, (int(np.array(count).max() / 100) + 1) * 100])
    ticks = plt.xticks([i*1.5 for i in range(len(count))], labels, fontproperties = yh)
    for t in ticks[1]:
        t.set_fontsize(6)
    rects = plt.bar(left = [i*1.5 for i in range(len(count))], height = count, width = 0.5, align = 'center', linewidth = 0)
    for rect in rects:
        height = rect.get_height()
        t = plt.text(rect.get_x(), 50 + height, "%s" % int(height))
        t.set_fontsize(8)
        
#用户月上网流量
def dou_distribution(users, full = True):
    #99.9% <10000
    if full is True:
        dou = [i * 100 for i in range(int(10000 / 100) + 1)]
        title = plt.title('用户dou分布直方图', fontproperties = yh)
    elif full is False:
        #98.5 <4000
        dou = [i * 10 for i in range(int(4000 / 10) + 1)]
        title = plt.title('用户dou分布图', fontproperties = yh)
    else:
        raise ValueError('invalid value: full must be bool')
    count = []
    #[a,b)
    for i in range(len(dou) - 1):
        a = dou[i]
        b = dou[i + 1]
        n = len(users[(users['dou'] >= a) & (users['dou'] < b)]['宽带账号'].unique())
        count.append(n)   
    labels = [i * 10 for i in dou]
    title.set_fontsize(15)
    title.set_position((0.5, 1.05))
    plt.xlabel('dou', fontproperties = yh)
    plt.ylabel('用户数', fontproperties = yh)
    plt.axis([-1, len(count), 0, (int(np.array(count).max() / 100) + 1) * 100])
    plt.xticks([i*10 for i in range(int(len(count)/10) + 1)], labels, fontproperties = yh)
    plt.bar(left = [i for i in range(len(count))], height = count, width = 0.4, align = 'center', linewidth = 0)

#用户dou分布饼状图
def dou_pie(users):
    dou = [i * 100 for i in range(1,11)]
    labels = [str(dou[i]) + '-' + str(dou[i+1]) +'M' for i in range(len(dou)-1)]
    labels.insert(0, '<100M')
    labels.append('>1000M')
    count = []
    #[a,b)
    for i in range(len(dou) - 1):
        a = dou[i]
        b = dou[i + 1]
        n = len(users[(users['dou'] >= a) & (users['dou'] < b)]['宽带账号'].unique())
        count.append(n)
    count.insert(0, len(users[(users['dou'] >= 0) & (users['dou'] < 100)]['宽带账号'].unique()))
    count.append(len(users[users['dou'] >= 1000]['宽带账号'].unique()))
    draw_pie(labels, count, '用户dou分布饼状图')

#终端品牌分布    
def brand_distribution(users):
    grouped = users.groupby('终端品牌')
    brand = grouped.count()['宽带账号']
    brand.name = 'count'
    brand = brand.sort_values(ascending = False)
    top = brand.drop('Z')[:10]
    #top_brand(top)
    labels = top.index.tolist()
    count = list(top)
    count.append(brand.drop(labels).sum())
    labels.append('其他')
    draw_pie(labels, count, '用户终端品牌分布')

def top_brand(top):
    title = plt.title('终端品牌top20', fontproperties = yh)
    title.set_fontsize(15)
    title.set_position((0.5, 1.05))
    plt.xlabel('用户数', fontproperties = yh)
    plt.ylabel('品牌', fontproperties = yh)
    labels = top.index.tolist()
    w = list(top)
    plt.yticks(np.arange(len(labels)), labels, fontproperties = yh)
    rects = plt.barh(bottom = np.arange(len(labels)), left = 0, height = 0.6, width = w, align = 'center')
    for rect in rects:
        width = rect.get_width()
        plt.text(500 + width, rect.get_y() + rect.get_height()/2, "%s" % int(width))
        
#特征分析   
def get_user_info():
    '''
    Returns
    -------
    gitv_user_city_info：用户地市信息（宽带账号|地市|市）
    gitv_user_detail：用户个人信息（宽带账号|地市|﻿UserID|年龄|性别|dou|arpu|带宽（M）|终端品牌）
    '''
    #数据源
    gitv_user_path = os.path.join(root, os.path.normpath('data/gitv_user_all.csv'))
    gitv_user_df = pd.read_csv(gitv_user_path, sep = '|', dtype = 'str')
    gitv_user_df.drop('牌照方', axis = 1, inplace = True)
    user_info = pd.read_csv(os.path.join(root, os.path.normpath('data\\user_info_valid.csv')), sep = '|', dtype = 'str')
    city_info = pd.read_csv(os.path.join(root, os.path.normpath('data\\gitv_user_location.csv')), sep = '|', dtype = 'str', encoding = 'gbk')
    
    #合并、匹配用户信息(先对宽带账号去重)
    gitv_user_info = gitv_user_df[['宽带账号', '地市']]
    gitv_user_info.drop_duplicates(inplace = True)
    gitv_user_info.sort_values(by = '宽带账号', inplace = True)
    gitv_user_city_info = pd.merge(gitv_user_info, city_info, on = '地市', how = 'left')    
    gitv_user_detail = pd.merge(gitv_user_info, user_info, left_on = '宽带账号', right_on = '用户号码', how = 'inner')
    gitv_user_detail.drop('用户号码', axis = 1, inplace = True)
    #gitv_user_detail.to_csv(os.path.join(root, os.path.normpath('data/gitv_user_valid_info.csv')), sep = '|', encoding = 'utf-8', index = False)       

    #预处理
    gitv_user_detail['性别'].fillna('不详', inplace = True)
    gitv_user_detail['年龄'].fillna('不详', inplace = True)
    gitv_user_detail['带宽（M）'].fillna('不详', inplace = True)
    gitv_user_detail['年龄'].replace('不详', -1, inplace = True)
    gitv_user_detail['年龄'] = gitv_user_detail['年龄'].astype(int)
    gitv_user_detail['带宽（M）'].replace('不详', -1, inplace = True)
    gitv_user_detail['带宽（M）'] = gitv_user_detail['带宽（M）'].apply(int)
    gitv_user_detail['arpu'] = gitv_user_detail['arpu'].apply(lambda x : round(float(x), 2))
    gitv_user_detail['dou'] = gitv_user_detail['dou'].apply(float)
    gitv_user_detail['终端品牌'].fillna('其他', inplace = True)
    
    return gitv_user_city_info, gitv_user_detail
    
#脚本运行入口 
def test():
    gitv_user_city_info, gitv_user_detail = get_user_info() 
    '''
    #用户地市分布
    city_distribution(gitv_user_city_info)
    #市区/县
    city_or_county(gitv_user_city_info)
    #性别分布
    gender_distribution(gitv_user_detail)
    #年龄分布
    age_distribution(gitv_user_detail)
    #年龄分段分布
    age_group_distribution(gitv_user_detail)
    #带宽分布
    bandwidth_distribution(gitv_user_detail)
    #业务消费特征分析
    arpu_distribution(gitv_user_detail)
    dou_distribution(gitv_user_detail, full = False)
    dou_pie(gitv_user_detail)
    plt.clf()
    '''
    brand_distribution(gitv_user_detail)
    

if __name__ == "__main__":  
    test()  
    
