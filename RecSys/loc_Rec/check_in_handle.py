# -*- coding: utf-8 -*-
"""
Created on Wed Nov 30 14:50:42 2016

@author: zhengyaolin
"""
import pandas as pd
import os
path = os.getcwd()

city = 'NY'
#city = 'CA'
names2 = ['user_id', 'venue_id', 'time']

def checkins_city():
    venue_info = pd.read_csv(os.path.join(path, os.path.normpath('data/venue_info_' + city + '.csv')), sep = '|', dtype = str)
    checkins = pd.read_csv(os.path.join(path, os.path.normpath('data/checkins.csv')), dtype = str)
    venue_ids = venue_info['venue_id'].unique()
    checkins = checkins[checkins['venue_id'].isin(venue_ids)]
    checkins = checkins_city[['user_id', 'venue_id', 'checkin_time_utc']]
    checkins.to_csv(os.path.join(path, os.path.normpath('data/checkins_' + city + '.csv')), sep = '|', index = False, encoding = 'utf-8')

    
def user_checkins_merge():
    '''
    merge user checkins
    
    Input
    -------------
    data: user_id|venue_id|checkin_time
    
    Note
    -------------
    merge check in the same place in an hour
    
    '''
    checkins = pd.read_csv(os.path.join(path, os.path.normpath('data/checkins_' + city + '.csv')), sep = '|', dtype = str)
    checkins['day'] = checkins['checkin_time_utc'].apply(lambda x : x[:10])
    checkins['hour'] = checkins['checkin_time_utc'].apply(lambda x : x[11:13])
    for (user, venue, day, hour), group in checkins.groupby(['user_id', 'venue_id', 'day', 'hour']):
        info = str(user) + '|' + str(venue) + '|' + str(group['checkin_time_utc'].unique()[0]) + '\n'
        #print(info)
        with open(os.path.join(path, os.path.normpath('data/checkins_merged_' + city + '.csv')), 'a') as f:
            f.write(info)

def checkins_choose():
    '''
    2012.10 - 2012.5
    8 months check in data
    
    '''
    checkins = pd.read_csv(os.path.join(path, os.path.normpath('data/checkins_merged_' + city + '.csv')), names = names2, sep = '|', dtype = str)
    checkins['year'] = checkins['time'].apply(lambda x : x[:4])
    checkins['month'] = checkins['time'].apply(lambda x : x[5:7])
    checkins_p1 = checkins[(checkins['year'] == '2012') & (checkins['month'].isin(['10','11','12']))]
    checkins_p2 = checkins[(checkins['year'] == '2013') & (checkins['month'].isin(['01','02','03','04','05']))]
    checkins_sample = pd.concat([checkins_p1, checkins_p2])
    checkins_sample = checkins_sample[names2]
    checkins_sample.to_csv(os.path.join(path, os.path.normpath('data/checkins_sample_' + city + '.csv')), index = False, header = False, sep = '|', encoding = 'utf-8')
    
def user_venue_filter(fre = 32):
    '''
    filt user checkins
    
    Input
    -------------
    data: user_id|venue_id|checkin_time
    
    Note
    -------------
    checkins > fre
    
    '''
    checkins = pd.read_csv(os.path.join(path, os.path.normpath('data/checkins_sample_' + city + '.csv')), names = names2, sep = '|', dtype = str)
    private_venue =  pd.read_csv(os.path.join(path, os.path.normpath('data/venue_private_' + city + '.csv')),header = None, sep = '|', dtype = str)
    private = list(private_venue[0])
    checkins = checkins[~checkins['venue_id'].isin(private)]    
    checkin_count = checkins.groupby('user_id').count()['venue_id']
    users_active = checkin_count[checkin_count > fre].index.tolist()
    checkins_active = checkins[checkins['user_id'].isin(users_active)]
    active_users = pd.DataFrame(users_active)
    active_users.to_csv(os.path.join(path, os.path.normpath('data/active_users.csv')), sep = '|', index = False, header = False, encoding = 'utf-8')
    checkins_active.to_csv(os.path.join(path, os.path.normpath('data/checkins_filtered_' + city + '.csv')), sep = '|', index = False, encoding = 'utf-8')

def user_venue_divide(p = 0.8):
    '''
    user-item
    
    divide data into 2 sets: train-set and test-set
    
    Input
    -----------------
    user_id|venue_id|time
    
    Output
    -----------------
    item|user
    
    user|item|count
    
    Attributes
    -----------------
    p: percentage of training set
    
    '''
    checkins = pd.read_csv(os.path.join(path, os.path.normpath('data/checkins_filtered_' + city + '.csv')), names = names2, sep = '|', dtype = str)
    checkins.sort_index(by = ['user_id', 'time'], inplace = True)
    # train + test 
    train_df = pd.DataFrame(columns = names2)
    test_df = pd.DataFrame(columns = names2)
    for user, group in checkins.groupby('user_id'):
        l = len(group)
        train = group[:int(l*p)]
        test = group[int(l*p):]
        train_df = train_df.append(train, ignore_index = True)
        if len(test) > 0:
            test_df = test_df.append(test, ignore_index = True)
    test_df.to_csv(os.path.join(path, os.path.normpath('data/user_venue_' + city + '_test.csv')), sep = '|', index = False, header = False, encoding = 'utf-8')
    user_item = train_df.groupby(['user_id', 'venue_id']).count()
    user_item.to_csv(os.path.join(path, os.path.normpath('data/user_venue_orig_' + city + '_train.csv')), sep = '|', header = False, encoding = 'utf-8')
    user_item = pd.read_csv(os.path.join(path, os.path.normpath('data/user_venue_orig_' + city + '_train.csv')), sep = '|', names = names2, dtype = str)
    item_user = user_item[['venue_id', 'user_id']]
    item_user.to_csv(os.path.join(path, os.path.normpath('data/user_venue_' + city + '_train.csv')), sep = '|', header = False, index = False, encoding = 'utf-8')

def test_checkins():
    '''
    Input: user_id|venue_id|time
    Output: user_id, venue_id|...
    '''
    test = pd.read_csv(os.path.join(path, os.path.normpath('data/user_venue_' + city + '_test.csv')), sep = '|', names = names2, dtype = str)
    for u, group in test.groupby('user_id'):
        #print(len(group))
        info = str(u) + '|'
        for v in list(group['venue_id']):
            info += v + ','
        info = info[:-1] + '\n'
        with open(os.path.join(path, os.path.normpath('data/user_venues_test_' + city + '.csv')), 'a') as f:
            f.write(info)

def checkin_score(x):
    if x < 4:
        return x + 1
    else:
        return 5
    
def checkin_prefer():
    check_df = pd.read_csv(os.path.join(path, os.path.normpath('data/user_venue_orig_' + city + '_train.csv')), names = ['user','venue','checkin'], sep = '|', dtype = str)   
    check_df['checkin'] = check_df['checkin'].apply(int)
    check_df['checkin_score'] = check_df['checkin'].apply(lambda x : x+1)
#    check_df['checkin_score'] = check_df['checkin'].apply(checkin_score)
    checkin_pre = check_df[['user','venue','checkin_score']]
    checkin_pre.to_csv(os.path.join(path, os.path.normpath('data/user_venue_checkin_score_' + city + '.csv')), sep = '|', header = False, index = False, encoding = 'utf-8')

def merge_prefer():
    checkin_pre = pd.read_csv(os.path.join(path, os.path.normpath('data/user_venue_checkin_score_' + city + '.csv')), sep = '|', names = ['user','venue','ch_score'], dtype = str)
    checkin_pre['ch_score'] = checkin_pre['ch_score'].apply(int)   
    senti_pre = pd.read_csv(os.path.join(path, os.path.normpath('data/sentiment_score_norm_' + city + '.csv')), sep = '|', names = ['user','venue','ss_score'], dtype = str)
    senti_pre['ss_score'] = senti_pre['ss_score'].apply(float) 
    df = pd.merge(checkin_pre, senti_pre, how = 'outer', on = ['user', 'venue'])
    #df[df['ss_score'].notnull()]
    df.fillna(0, inplace = True)
    df_1 = df[df['ch_score'] <= 2]
    df_2 = df[df['ch_score'] > 2]
    df_1['score'] = df_1['ss_score'].apply(lambda x : 2 + 2*x)
    df_2['score'] = df_2['ch_score'] + df_2['ss_score']
    df = pd.concat([df_1, df_2])
    df = df[['user','venue','score']]
    df.to_csv(os.path.join(path, os.path.normpath('data/user_venue_score_' + city + '.csv')), sep = '|', header = False, index = False, encoding = 'utf-8')
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    