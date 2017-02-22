# -*- coding: utf-8 -*-
"""
Created on Mon Dec  5 16:26:00 2016

@author: zhengyaolin
"""

import pandas as pd
import os
import nltk
from nltk.corpus import stopwords
import matplotlib.pyplot as plt

colors = ['b', 'g', 'r', 'c', 'm', 'y']
plt.style.use('ggplot')

path = os.getcwd()
city = 'CA'
#city = 'NY'
english_stopwords = stopwords.words('english')
senti_dict_names = ['word', 'POS', 'SentiScore', 'ObjScore']
# n/a/r/v
valid_senti_words = ['NN', 'NNS', 'NNP', 'NNPS', 'VBG', 'JJ', 'JJR', 'JJS', 'RB', 'RBR', 'RBS', 'MD', 'VB', 'VBD', 'VBP', 'VBZ']
pos_dict = {'NN':'n', 'NNS':'n', 'NNP':'n', 'NNPS':'n', 'VBG':'n', 'JJ':'a', 'JJR':'a', 'JJS':'a', 'RB':'r', 'RBR':'r', 'RBS':'r', 'MD':'v', 'VB':'v', 'VBD':'v', 'VBP':'v', 'VBZ':'v'}

def tips_filtering():
    tips_df = pd.read_csv(os.path.join(path, os.path.normpath('data/venue_tips_' + city + '.csv')), sep = '|', dtype = str)
    tips_df.drop_duplicates(inplace = True)
    users_df = pd.read_csv(os.path.join(path, os.path.normpath('data/active_users.csv')), sep = '|', names = ['user_id'], dtype = str)
    active_usr = list(users_df['user_id'])
    tips = tips_df[['user_id','venue_id', 'tips']]
    tips = tips[tips['user_id'].isin(active_usr)]
    tips.to_csv(os.path.join(path, os.path.normpath('data/active_user_tips_' + city + '.csv')), index = False, sep = '|', encoding = 'utf-8')
    
def senti_analysis():
    tips = pd.read_csv(os.path.join(path, os.path.normpath('data/active_user_tips_' + city + '.csv')), sep = '|', dtype = str)
    senti_df = pd.read_csv(os.path.join(path, os.path.normpath('data/SentiWordDict_merged.csv')), sep = '|', dtype = str, names = senti_dict_names)
    senti_score_dict = dict()
    obj_score_dict = dict()
    for i, row in senti_df.iterrows():
        senti_score_dict[tuple([row['word'], row['POS']])] = float(row['SentiScore'])
        obj_score_dict[tuple([row['word'], row['POS']])] = float(row['ObjScore'])

    for i, row in tips.iterrows():
        tip = row['tips']
        pos_tagged_tokens = []
        # sentences split
        sentences = nltk.sent_tokenize(tip)
        for s in sentences:
            tokens = nltk.word_tokenize(s)
            tokens = [w.lower() for w in tokens]
            pos_tagged_tokens.extend(nltk.pos_tag(tokens))
        # stopwords filter
        pos_tagged_tokens = [w for w in pos_tagged_tokens if w[0] not in english_stopwords]
        # n,r,a,v filtering 
        pos_tagged_tokens = [w for w in pos_tagged_tokens if w[1] in valid_senti_words]
        
        pos_tagged_words = []
        for w in pos_tagged_tokens:
            pos_tagged_words.append((w[0], pos_dict[w[1]]))
            
        senti_score = 0
        obj_score = 0
        for w in pos_tagged_words:
            if w in senti_score_dict.keys():
                senti_score += senti_score_dict[w]
                obj_score += obj_score_dict[w]
        #print(senti_score, obj_score) 
        
        info = str(row['user_id']) + '|' + str(row['venue_id']) + '|' + str(senti_score) + '|' + str(obj_score) + '\n'
        with open(os.path.join(path, os.path.normpath('data/active_user_tips_senti_analysis_' + city + '.csv')), 'a') as f:
            f.write(info)


def senti_dict():
    '''
    senti-score = pos - neg
    
    output
    ---------------
    word|POS|SentiScore|ObjScore
    
    Note
    ---------------
    SentiScore = PosScore - NegScore
    ObjScore = 1 - (PosScore + NegScore)
    
    '''
    senti_df = pd.read_csv(os.path.join(path, os.path.normpath('data/SentiWordNet_3.0.0.txt')), skiprows = 27, sep = '\t', header = None, dtype = str)
    senti_df.dropna(inplace = True)    
    senti_df.drop_duplicates(inplace = True)
    for i, row in senti_df.iterrows():
        try:
            POS = row[0]
            p = float(row[2])
            n = float(row[3])
            senti_score = str(p - n)
            obj_score = str(1 - p - n)
            words = row[4].split(' ')
            for w in words:
                info = w.split('#')[0] + '|' +  POS + '|' + senti_score + '|' + obj_score + '\n'
                with open(os.path.join(path, os.path.normpath('data/SentiWordDict.csv')), 'a') as f:
                    f.write(info)
        except TypeError as e:
            print(w, POS, p, n)
            print('**********************', e)
                
                
def senti_dict_merge():
    '''
    Merge same word with same POS
    
    Output
    -------------
    (word, POS)|SentiScore|ObjScore
    '''
    senti_df = pd.read_csv(os.path.join(path, os.path.normpath('data/SentiWordDict.csv')), sep = '|', dtype = str, names = senti_dict_names)
    senti_df['SentiScore'] = senti_df['SentiScore'].apply(float)
    senti_df['ObjScore'] = senti_df['ObjScore'].apply(float)

    for w, group in senti_df.groupby(['word', 'POS']):
        '''
        max_score = group['SentiScore'].max()
        min_score = group['SentiScore'].min()
        if max_score <= 0:
            senti_score = group[group['SentiScore'] != max_score]['SentiScore'].mean()
        elif min_score >= 0:
            senti_score = group[group['SentiScore'] != min_score]['SentiScore'].mean()
        else:
        '''
        senti_score = group['SentiScore'].mean()
        obj_score = group['ObjScore'].mean()
        info = w[0] + ',' + w[1] + '|' + str(senti_score) + '|' + str(obj_score) + '\n'
        with open(os.path.join(path, os.path.normpath('data/SentiWordDict_merged.csv')), 'a') as f:
            f.write(info)
           
def normalize(x, max_p, max_n):
    if x >= 0:
        return x / max_p
    else:
        return x / max_n
        
def senti_score_norm():
    senti_df = pd.read_csv(os.path.join(path, os.path.normpath('data/active_user_tips_senti_analysis_' + city + '.csv')), names = ['user_id', 'venue_id', 'senti_score', 'obj_score'], sep = '|', dtype = str)
    senti_df['senti_score'] = senti_df['senti_score'].apply(float)
    max_p = senti_df['senti_score'].max()
    max_n = - senti_df['senti_score'].min()
    senti_df['ss_norm'] = senti_df['senti_score'].apply(normalize, args = (max_p, max_n))
    df = senti_df[['user_id', 'venue_id', 'ss_norm']]
    df_ = df.groupby(['user_id','venue_id']).mean()
    df_.to_csv(os.path.join(path, os.path.normpath('data/sentiment_score_norm_' + city + '.csv')), header = False, sep = '|', encoding = 'utf-8')
    
    
    
    
    
    