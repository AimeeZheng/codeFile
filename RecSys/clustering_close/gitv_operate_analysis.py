# -*- coding: utf-8 -*-
"""
Created on Wed Aug 10 14:29:43 2016

@author: zhengyaolin
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

'''全局设置'''
#绘图默认风格
plt.style.use('ggplot')
#中间数据根路径
root = os.getcwd()
#指定默认字体
yh = mpl.font_manager.FontProperties(fname='D:/Program Files/Anaconda3/Lib/site-packages/matplotlib/mpl-data/fonts/ttf/msyh.ttf')
#颜色
colors = ['b', 'g', 'r', 'c', 'm', 'y', '#FFB5C5']

weekday = ['20160624', '20160627', '20160628', '20160629', '20160630']
weekend = ['20160625', '20160626']
all_day = ['20160624', '20160625', '20160626', '20160627', '20160628', '20160629', '20160630']
watch_columns = ['UserID', '用户地市', '开始时间', '结束时间', '业务类型', '节目/内容ID', '节目/内容名称', '内容访问来源', '设备ID',
                 '终端IP', '计费类型', '费用', '用户使用的流量']
operate_columns = ['UserID', '用户地市', '用户操作时间', '结束时间', '操作对象类型', '操作对象ID', '内容ID', '内容名称', '操作类型',
                   '书签断点', '设备ID', '终端IP']
user_columns = ['宽带账号', '地市', '机顶盒串号', 'MAC地址', 'UserID', '年龄', '性别', 'dou', 'arpu', '带宽（M）', '终端品牌']
data_path = r'E:\zhengyaolin\互联网电视分析模型\data'
#view_data_path = r'E:\zhengyaolin\互联网电视分析模型\data\银河\view'
view_data_path = r'E:\互联网电视分析模型\data\AH_LOG_20160624_20160630'
operate_data_path = r'E:\zhengyaolin\互联网电视分析模型\data\银河\operate'
#fig_savepath = r'E:\zhengyaolin\互联网电视分析模型\用户行为分析结果'
fig_savepath = r'E:\互联网电视分析模型\用户行为分析结果'
hour = ['0' + str(i) +'0000' for i in range(10)] + [str(i) + '0000' for i in range(10,24)]
content_type = ['体育', '其他', '动漫', '娱乐', '搞笑', '教育', '时尚', '游戏', '片花', '电影', '电视剧', '纪录片', '综艺', '音乐']
pre_type = ['动漫', '电视剧', '电影', '综艺', '音乐']

#柱状图添加高度值标签
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        plt.text(rect.get_x(), 500 + height, "%s" % int(height))
        
def autolabelh(rects):
    for rect in rects:
        width = rect.get_width()
        plt.text(500 + width, rect.get_y() + rect.get_height()/2, "%s" % int(width))
        
def draw_bar(title, xlabel, ylabel, xy, labels, h, w, name):
    '''
    绘制柱状图
    
    Parameters
    ----------
    title：图标题
    xlabel,ylabel：轴名
    xy: [xmin, xmax, ymin, ymax] 轴刻度取值范围
    labels：x轴标签
    h：柱高
    w：柱宽
    name：图保存名称
    '''
    title = plt.title(title, fontproperties = yh)
    title.set_fontsize(15)
    title.set_position((0.5, 1.05))
    print(title.get_position())
    plt.xlabel(xlabel, fontproperties = yh)
    plt.ylabel(ylabel, fontproperties = yh)
    plt.axis(xy)
    plt.xticks([i for i in range(len(labels))], labels, fontproperties = yh)
    chart = plt.bar(left = [i for i in range(len(labels))], height = h, width = w, align = 'center')
    autolabel(chart)
    plt.savefig(os.path.join(fig_savepath, os.path.normpath(name)))

def draw_barh(title, xlabel, ylabel, xy, labels, h, w, name):
    '''
    绘制水平柱状图
    
    Parameters
    ----------
    title：图标题
    xlabel,ylabel：轴名
    xy: [xmin, xmax, ymin, ymax] 轴刻度取值范围
    labels：x轴标签
    h：柱高
    w：柱宽
    name：图保存名称
    '''
    title = plt.title(title, fontproperties = yh)
    title.set_fontsize(15)
    title.set_position((0.5, 1.05))
    print(title.get_position())
    plt.xlabel(xlabel, fontproperties = yh)
    plt.ylabel(ylabel, fontproperties = yh)
    plt.axis(xy)
    plt.yticks(np.arange(len(labels)), labels, fontproperties = yh)
    chart = plt.barh(bottom = np.arange(len(labels)), left = 0, height = h, width = w, align = 'center')
    autolabelh(chart)
    plt.savefig(os.path.join(fig_savepath, os.path.normpath(name)))
    
def draw_pie(title, labels, x, name):
    '''
    绘制饼状图
    
    Parameters
    ----------
    title：图标题
    labels：标签
    x：array of every patches
    name：图保存名称
    '''
    title = plt.title(title, fontproperties = yh)
    title.set_fontsize(15)
    title.set_position((0.5, 1.05))
    color = [colors[i % len(colors)] for i in range(len(labels))]
    patches, l_text , p_text = plt.pie(x, radius = 1, colors = color, labels = labels, labeldistance = 1.05, autopct = '%1.2f%%', pctdistance = 0.75)    
    for p in patches:
        p.set_lw(0)
    for t in l_text:
        t.set_fontproperties(yh)
    plt.axis('equal')
    plt.savefig(os.path.join(fig_savepath, os.path.normpath(name)))

def draw_line(title, xlabel, ylabel, x, y, name, labels = None, xy = None, bar = False):
    '''
    绘制折线图
    
    Parameters
    ----------
    title：图标题
    xlabel,ylabel：轴名
    x：x轴坐标
    y：y轴坐标
    name：图保存名称
    xy: [xmin, xmax, ymin, ymax] 轴刻度取值范围
    '''
    if xy is not None:
        plt.axis(xy)
    if labels is not None:
        plt.xticks([i for i in range(len(labels))], labels, fontproperties = yh)
    title = plt.title(title, fontproperties = yh)
    title.set_fontsize(15)
    title.set_position((0.5, 1.05))
    plt.xlabel(xlabel, fontproperties = yh)
    plt.ylabel(ylabel, fontproperties = yh)
    plt.plot(x, y, '-xr')
    if bar is True:
        plt.bar(left = [i for i in range(len(labels))], height = y, width = 0.2, align = 'center')
    plt.savefig(os.path.join(fig_savepath, os.path.normpath(name)))

def user_watch(is_weekday = True, type_code = '1'):
    '''
    统计在工作日/周末每天每个时间段观看点播/回看/直播节目的用户数（平均）
    Parameters
    ----------
    is_weekday : bool, True if weekday, or weekend
    
    type_code：type of content
            1：点播 2：回看 3：直播
    '''
    print(is_weekday, type_code)
    yadd = 0
    if is_weekday is True:
        days = weekday
        title = '用户工作日观看时间偏好图'
        name = '银河_互联网电视用户工作日观看时间偏好图'
    elif is_weekday is False:
        #周末
        days = weekend
        title = '用户周末观看时间偏好图'
        name = '银河_互联网电视用户周末观看时间偏好图'
        yadd = 1000
    else:
        raise ValueError('invalid value: is_weekday must be bool')
        
    if type_code == '1':
        subpath = '_gitv_ottuserviewdata_vod.dat'
        ymax = 25000 + yadd
        title += '(点播)'
        name += '_点播.png'
    elif type_code == '2':
        subpath = '_gitv_ottuserviewdata_livod.dat'
        ymax = 8000 + yadd
        title += '(回看)'
        name += '_回看.png'
    elif type_code == '3':
        subpath = '_gitv_ottuserviewdata_livod.dat'
        ymax = 10000 + yadd
        title += '(直播)'
        name += '_直播.png'
    else:
        if type(type_code) == int:
            raise  ValueError('invalid type value: type_code must be str')
        raise  ValueError('invalid type value: %s' % type_code)
        
    user_info = pd.read_csv(os.path.join(root, os.path.normpath('data\gitv_user_info_detail.csv')), sep = '|', dtype = str)
    user_id = sorted(user_info['UserID'].unique())
    count = []
    for d in days:
        path = os.path.join(view_data_path, os.path.normpath(d + subpath))
        df = pd.read_csv(path, names = watch_columns, sep = '|', dtype = str)
        df['id'] = df['UserID'].apply(lambda x : x[:14])
        df = df[df['id'].isin(user_id)][df['业务类型'] == type_code]
        count.append(user_watch_day(d, df))
        print(d + subpath)
    count_mean = np.array(count).mean(axis = 0).astype(int)
    labels = [str(i) + 'h' for i in range(24)]
    draw_bar(title = title, xlabel = '时间段', ylabel = '用户数', xy = [-1, 24, 0, ymax], labels = labels, h = count_mean, w = 0.5, name = name)
    
def user_watch_day(day, df):
    '''
    统计一天24小时，每个时间段[a,b)观看节目的用户数
    
    Parameters
    ------------
    day：统计的日期 格式:'yyyymmdd'
    
    df: 统计的行为表格
    
    Returns
    -------
    count：24小时，每个时间段观看的用户数
    '''
    count = []
    d_hour = [day + i for i in hour]
    for i in range(24):
        a = d_hour[i]
        b = d_hour[(i + 1) % 24]
        n = len(df[~((df['开始时间'] >= b) | (df['结束时间'] < a))]['UserID'].unique())
        count.append(n)
    return count

def content_type_count(vod):
    '''
    计算每种类型节目的观看次数
    
    Parameters
    ----------
    vod：观看记录 [n_records, n_features]
         features = ['UserID', '开始时间', '结束时间', '内容ID', '名称', '类型']
    
    Returns
    -------
    count：各类型节目观看次数
    '''
    count = []
    for t in content_type:
        count.append(vod[vod['类型'] == t].shape[0])
    return count

def content_info():
    '''
    生成有效的内容信息
    '''
    content_info = pd.read_csv(os.path.join(data_path, os.path.normpath('银河/基础内容数据.csv')), sep = '|', dtype = str)
    #df.to_csv(path, sep = '|', index = False, encoding = 'utf-8')
    #df.dropna(axis = 1, how = 'all', inplace = True)
    content_info.drop_duplicates(inplace = True)
    #有效节目类型
    content_info = content_info[content_info['类型'].isin(content_type)]
    null_columns = []
    for i in content_info.columns:
        n = len(content_info[content_info[i].isnull()])
        p = n / 483477 * 100
        if p > 90:
            null_columns.append(i)
        #print(i, str(p) + '%')
    content_info.drop(null_columns, axis = 1, inplace = True)
    content_info.to_csv(os.path.join(root, os.path.normpath('data/银河_基础内容信息.csv')), sep = '|', encoding = 'utf-8', index = False)
    
def content_prefer():
    '''
    各类型电视节目偏好分析(点播才有内容id)
    '''
    content_info = pd.read_csv(os.path.join(root, os.path.normpath('data/银河_基础内容信息.csv')), sep = '|', dtype = str)
    days = weekday + weekend
    count = [] #每种类型的观看次数
    for d in days:
        path = os.path.join(view_data_path, os.path.normpath(d + '_gitv_ottuserviewdata_vod.dat'))
        df = pd.read_csv(path, names = watch_columns, sep = '|', dtype = str)
        df = df[df['业务类型'] == '1'][df['节目/内容ID'].notnull()]
        record = pd.merge(df[['UserID', '开始时间', '结束时间', '节目/内容ID']], content_info[['内容ID', '名称', '类型']], left_on = '节目/内容ID', right_on = '内容ID')
        record.drop('节目/内容ID', axis = 1, inplace = True)   #去除重复字段
        count.append(content_type_count(record))
        record.to_csv(os.path.join(root, os.path.normpath('data/' + d + '_gitv_ottuserviewdata_vod.csv')), sep = '|', encoding = 'utf-8', index = False)
        print(d)
    count_sum = np.array(count).sum(axis = 0, dtype = int)
    #print(count_sum)
    draw_pie('用户节目类型偏好图', content_type, count_sum, '银河_互联网电视用户观看节目类型偏好饼状图.png')
    plt.clf()
    draw_bar('用户节目类型偏好图', '类型', '观看次数', [-1,14,0,1500000], content_type, count_sum, 0.5, '银河_互联网电视用户观看节目类型偏好柱状图.png')  

def vod_record_all():
    '''
    合并七天有效的观看记录（点播）
    '''
    days = weekday + weekend
    data = pd.DataFrame()
    for d in days:
        path = os.path.join(root, os.path.normpath('data/' + d + '_gitv_ottuserviewdata_vod.csv'))
        df = pd.read_csv(path, sep = '|', dtype = str)
        data = pd.concat([data, df])
        print(d)
    data.to_csv(os.path.join(root, os.path.normpath('data/gitv_ottuserviewdata_vod.csv')), index = False, sep = '|', encoding = 'utf-8')
    
def favorite_program(topN):
    '''
    统计每种受欢迎类型的节目的排行
     Parameters
    ----------
    topN：top N programs (int)
    '''
    df = pd.read_csv(os.path.join(root, os.path.normpath('data/gitv_ottuserviewdata_vod.csv')), sep = '|', dtype = str)
    for t in pre_type:
        data = df[df['类型'] == t]
        top = data.groupby('名称').size().sort_values(ascending = False)[:topN]
        labels = list(top.index.values)
        n = list(top.values)
        draw_barh('用户观看' + t + '排行', '观看次数', '节目名称', [0, (int(n[0]/5000)+1)*5000, -1, topN], labels, 0.5, n, '银河_用户观看' + t + '排行_top' + str(topN) + '.png')
        plt.clf()

def operate_record_all():
    '''
    合并七天的操作记录，匹配内容信息
    '''
    content_info = pd.read_csv(os.path.join(root, os.path.normpath('data/银河_基础内容信息.csv')), sep = '|', dtype = str)
    days = weekday + weekend
    data = pd.DataFrame()
    for d in days:
        path = os.path.join(operate_data_path, os.path.normpath(d + '_gitv_ottuseroperatedata_vod.csv'))
        df = pd.read_csv(path, sep = ',', dtype = str, encoding = 'gbk')
        data = pd.concat([data, df])
        print(d)
    data.to_csv(os.path.join(root, os.path.normpath('data/gitv_ottuseroperatedata_vod.csv')), index = False, sep = '|', encoding = 'utf-8')
    data = data[(data['操作对象类型'] == '1') & (data['操作类型'] == '1')]
    collect = pd.merge(data[['UserID', '用户操作时间', '结束时间', '内容ID']], content_info[['内容ID', '名称', '类型']], on = '内容ID', how = 'inner')
    collect.to_csv(os.path.join(root, os.path.normpath('data/gitv_collect_vod.csv')), index = False, sep = '|', encoding = 'utf-8')
    
def collect_program():
    '''
    用户收藏节目类型
    '''
    collect = pd.read_csv(os.path.join(root, os.path.normpath('data/gitv_collect_vod.csv')), sep = '|', dtype = str)
    count = content_type_count(collect)
    draw_pie('用户收藏节目类型偏好图', content_type, count, '银河_互联网电视用户收藏节目偏好饼状图.png')
    plt.clf()
    draw_bar('用户收藏节目类型偏好图', '类型', '收藏次数', [-1,14,0,22000], content_type, count, 0.5, '银河_互联网电视用户收藏节目类型偏好柱状图.png')  

app_10086 = ['咪咕音乐', '和视频', '和地图', '和天气', '和动漫', '和游戏', '和冲浪', '和阅读']
def popular_app():
    '''
    统计用户使用最多的app的分布情况
    '''
    #用户
    gitv_user_path = os.path.join(root, os.path.normpath('data/gitv_user_all.csv'))
    gitv_user_df = pd.read_csv(gitv_user_path, sep = '|', dtype = 'str')
    users = gitv_user_df['宽带账号'].unique()
    #使用app数据
    app_path = os.path.join(data_path, os.path.normpath('互联网电视用户top20应用\fangchao_tvuser_export.csv'))
    app_names = ['UserID', '宽带账号'] + [i for i in range(1,21)]
    app_df = pd.read_csv(app_path, names = app_names, dtype = str)
    app_df.drop('UserID', axis = 1, inplace = True)
    user_app = app_df[app_df['宽带账号'].isin(users)]
    user_app.drop_duplicates(inplace = True)
    user_app.replace(['\\N', 'unknown'], '未知', inplace = True)
    #user_app.to_csv(os.path.join(root, os.path.normpath('data/gitv_user_app.csv')), sep = '|', index = False, header = False)
    #匹配全量应用名称、业务大类 —— 取交集
    app_info = pd.read_csv(os.path.join(data_path, os.path.normpath('应用列表.csv')), dtype = str)
    df = pd.merge(user_app[['宽带账号', 1]], app_info[['应用列表', '应用名称', '应用大类']], left_on = 1, right_on = '应用列表')
    #用户使用app最多的各应用占比
    app_rank = df.groupby('应用名称').count()['宽带账号'].sort_values(ascending = False)
    top = app_rank.drop(['HTTP','HTTP_FileAccess', 'HTTPS', 'Tencent_Common'])[:20]
    labels = top.index.tolist()
    count = list(top)
    draw_barh('最受用户欢迎的应用top20', '用户数', 'APP', [0, (int(count[0]/5000)+1)*5000, -1, 20], labels, 0.5, count, '银河_最受用户欢迎的APP排行_top20.png')
    plt.clf()    
    labels = labels[:10]
    labels.append('其他')
    count = count[:10]
    count.append(app_rank.sum() -  sum(count))
    draw_pie('最受用户欢迎的应用分布图', labels, count, '银河_最受用户欢迎的APP分布饼状图.png')

def app_distribution():
    '''
    用户使用应用top20各应用的分布情况
    '''
    app_names = ['UserID', '宽带账号'] + [i for i in range(1,21)]
    user_app = pd.read_csv(os.path.join(root, os.path.normpath('data/gitv_user_app.csv')), sep = '|', names = app_names, dtype = str)
    app = user_app.groupby(1).count()['宽带账号']
    for i in range(2,21):
        app = pd.concat([app, user_app.groupby(i).count()['宽带账号']], axis = 1, join = 'outer')
    app.fillna(0, inplace = True)
    app.to_csv(os.path.join(root, os.path.normpath('data/gitv_user_app_count_top20.csv')), sep = '|', encoding = 'utf-8', float_format = '%d', header = False)
    all_count = pd.DataFrame(app.sum(axis = 1).sort_values(ascending = False), dtype = int)
    app_info = pd.read_csv(os.path.join(data_path, os.path.normpath('应用列表.csv')), dtype = str)
    df = pd.merge(all_count, app_info[['应用列表', '应用名称', '应用大类']], left_index = True, right_index = False, right_on = '应用列表')
    #用户使用应用分类情况
    grouped = df.groupby('应用大类')[0].sum()
    draw_pie('用户喜欢使用APP分布图', grouped.index.tolist(), list(grouped), '银河_用户喜欢使用APP类型分布饼状图.png')
    plt.clf()
    #df.to_csv(os.path.join(root, os.path.normpath('data/gitv_user_app_count.csv')), sep = '|', encoding = 'utf-8', index = False, header = False)
    #应用列表对应应用名称汇总使用用户数    
    count = df.groupby('应用名称')[0].sum().sort_values(ascending = False)    
    count.drop(['HTTP', 'HTTP_FileAccess', 'HTTPS', 'Tencent_Common', 'DNS', 'SSL', 'Behavior_TransferFile'], inplace = True)
    top = count[:20]
    labels = top.index.tolist()
    n = list(top)
    draw_bar('用户使用应用Top20', 'APP', '用户数', [-1,20,0,(int(n[0]/1000)+1)*1000], labels, n, 0.5, '银河_互联网电视用户使用应用top20.png')  
    plt.clf()    
    #用户使用自有产品情况    
    labels = count[app_10086].index.tolist()
    n = list(count[app_10086])
    draw_bar('用户使用自有产品情况', 'APP', '用户数', [-1,len(app_10086),0, max(n) + 500], labels, n, 0.5, '银河_互联网电视用户使用移动自有应用柱状图.png')  
    plt.clf()
    #计算自有产品同类的应用使用情况
    app_count = pd.DataFrame([count.index.tolist(), list(count)]).T
    app_count.columns = ['应用名称', 'count']
    app_type_df = app_info[['应用名称', '应用大类']]
    app_type_df.drop_duplicates(inplace = True)
    df = pd.merge(app_count, app_type_df, on = '应用名称', how = 'inner') #有序 降序
    for i in app_10086:
        record =  df[df['应用名称'] == i]
        app_type = record['应用大类'].unique()[0]
        group = df[df['应用大类'] == app_type]
        labels = list(group['应用名称'][:5])
        n = list(group['count'][:5])
        #前五无移动自有产品
        if i not in list(labels):
            labels.append(i)
            n.append(list(record['count'])[0])
            n.append(group['count'].sum() - sum(n)- record['count'].sum())
        else:
            n.append(group['count'].sum() - sum(n))
        labels.append('其他')
        draw_pie('用户使用' + app_type + '类APP分布图', labels, n, '银河_用户使用' + app_type + '类APP分布饼状图.png')
        plt.clf()

def all_action(watch = False):
    '''
    汇总每天的活跃行为：直播、点播、回看、操作（收藏、书签）
    
    Parameters
    ----------
    watch : bool, True if watch action, or all action
            default False 汇总所有活跃行为
    '''
    user_info = pd.read_csv(os.path.join(root, os.path.normpath('data\gitv_user_info_detail.csv')), sep = '|', dtype = str)
    user_id = sorted(user_info['UserID'].unique())
    view_type = ['_gitv_ottuserviewdata_livod.dat', '_gitv_ottuserviewdata_vod.dat']
    for d in all_day:
        print(d)
        data = pd.DataFrame()        
        #观看行为
        for t in view_type:
            path = os.path.join(view_data_path, os.path.normpath(d + t))
            df = pd.read_csv(path, names = watch_columns, sep = '|', dtype = str)
            df['id'] = df['UserID'].apply(lambda x : x[:14])
            df = df[df['id'].isin(user_id)][['id', '开始时间', '结束时间']]
            data = pd.concat([data, df])
            
        if watch is False:
            #添加操作行为
            path = path = os.path.join(operate_data_path, os.path.normpath(d + '_gitv_ottuseroperatedata_vod.csv'))
            df = pd.read_csv(path, sep = ',', dtype = str, encoding = 'gbk')
            df['id'] = df['UserID'].apply(lambda x : x[:14])
            df = df[df['id'].isin(user_id)][['id', '用户操作时间', '结束时间']]
            df.columns = ['id', '开始时间', '结束时间']
            data = pd.concat([data, df])
            output = os.path.join(root, os.path.normpath('data/' + d + '_action.csv'))
        elif watch is True:
            #只有所有观看行为
            output = os.path.join(root, os.path.normpath('data/' + d + '_watch_action.csv'))
        else:
            raise ValueError('invalid value: watch must be bool')
        data.to_csv(output, sep = '|', encoding = 'utf-8', index = False)
                
def day_active():
    '''
    统计日活跃率、活跃频次
    活跃率: 活跃用户/总用户
    活跃频次：每天活跃的记录数
    '''
    user_info = pd.read_csv(os.path.join(root, os.path.normpath('data\gitv_user_info_detail.csv')), sep = '|', dtype = str)
    user_all = len(user_info['UserID'].unique())
    print('users:', user_all)
    active_users = []
    action_count = []
    for d in all_day:
        path = os.path.join(root, os.path.normpath('data/' + d + '_action.csv'))
        df = pd.read_csv(path, sep = '|', dtype = str)
        #活跃用户
        active_users.append(len(df['id'].unique()))
        #活跃频次
        action_count.append(df.shape[0])
    #活跃率 百分比
    p_active = [round(x * 100 / user_all, 2) for x in active_users]
    #折线图
    draw_line('用户活跃率日变化图', '日期', '百分比', [i for i in range(len(all_day))], p_active, '银河_用户活跃率日变化折线图.png', all_day, [0, len(all_day)-1, 0, 100])  
    plt.clf()
    draw_line('用户活跃频次日变化图', '日期', '频次', [i for i in range(len(all_day))], action_count, '银河_用户活跃频次日变化折线图.png', all_day, [-0.5, len(all_day)-0.5, 0, (int(max(action_count)/100000)+1)*100000], True)       
    
def watch_time():
    '''
    统计工作日/周末用户观看时长
    
    Parameters
    ----------
    is_weekday : bool, True if weekday, or weekend
    '''
    #汇总所有观看行为
    data = pd.DataFrame()
    for d in all_day:
        path = os.path.join(root, os.path.normpath('data/' + d + '_watch_action.csv'))
        df = pd.read_csv(path, sep = '|', dtype = str)
        data = pd.concat([data, df])
    data.to_csv(os.path.join(root, os.path.normpath('data/watch_action_all.csv')), sep = '|', index = False, encoding = 'utf-8')
    data['day1'] = data['开始时间'].apply(lambda x : x[:8]) 
    data['day2'] = data['结束时间'].apply(lambda x : x[:8])  
    
    for d in all_day:
        #d当天用户观看时长
        df = data[(data['day1'] == d) | (data['day2'] == d)]   #开始时间在当天/结束时间在当天
        info = ''
        for u, group in df.groupby('id'):
            time = 0
            for i, row in group.iterrows():
                if row['day2'] == d:
                    #结束时间在当天
                    end = row['结束时间'][-6:]
                    time2 = int(end[:2])*60*60 + int(end[2:4])*60 + int(end[-2:])
                    if row['开始时间'][:8] == d:
                        #开始时间在当天
                        begin = row['开始时间'][-6:]
                        time1 = int(begin[:2])*60*60 + int(begin[2:4])*60 + int(begin[-2:])
                    else:
                        #开始时间不在当天
                        time1 = 0
                else:
                    #结束时间不在当天，开始时间在当天
                    begin = row['开始时间'][-6:]
                    time1 = int(begin[:2])*60*60 + int(begin[2:4])*60 + int(begin[-2:])
                    time2 = 24*60*60
                time += time2 - time1
            info += str(u) + '|' + str(time) + '\n'
        with open(os.path.join(root, os.path.normpath('data/' + d + '_user_watch_time.csv')), 'a') as f:
            f.write(info)

def use_watch_time(is_weekday = True):
    '''
    统计工作日/周末用户平均观看时长
    
    Parameters
    ----------
    is_weekday : bool, True if weekday, or weekend
    '''
    if is_weekday is True:
        days = weekday
        title = '用户工作日观看时长分布图'
        name = '银河_互联网电视用户工作日观看时长分布图'
        n = 5
    elif is_weekday is False:
        days = weekend
        title = '用户周末观看时长分布图'
        name = '银河_互联网电视用户周末观看时长分布图'
        n = 2
    else:
        raise ValueError('invalid value: is_weekday must be bool')
        
    data = pd.DataFrame()
    for d in days:
        path = os.path.join(root, os.path.normpath('data/' + d + '_user_watch_time.csv'))
        df = pd.read_csv(path, names = ['UserID', 'time'], sep = '|', dtype = str)
        data = data.append(df)
    data['time'] = data['time'].apply(np.int64)
    result = data.groupby('UserID')['time'].sum()
    result = result.div(60*60*n)
    len_time = [i*2 for i in range(12)]
    count = []
    for i in range(len(len_time)):
        a = len_time[i]
        b = a + 2
        count.append(len(result[(result >= a) & (result < b)]))
    labels = ['[' + str(i) + ',' + str(i+2) + ')' for i in len_time]
    draw_bar(title, '时长/h', '用户数', [-1, len(labels), 0, (int(max(count)/1000)+1)*1000], labels, count, 0.5, name)
     
#测试入口        
def test():
    user_watch(is_weekday = False, type_code = '3')
    #plt.clf()
    #content_prefer()
    #vod_record_all()
    #favorite_program(10)
    #collect_program()
    #all_action(watch = True)
    #watch_time()
    #use_watch_time(False)
    pass

if __name__ == "__main__":  
    test()          
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    