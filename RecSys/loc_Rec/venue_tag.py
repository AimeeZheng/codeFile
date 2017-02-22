# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 15:19:02 2016

@author: zhengyaolin
"""

import pandas as pd
import numpy as np
import os
import re
import nltk
from nltk.corpus import stopwords

path = os.getcwd()
english_stopwords = stopwords.words('english')
valid_tag = ['NN', 'NNS', 'NNP', 'NNPS', 'VBG']
porter = nltk.PorterStemmer()
features = ['categories', 'tags']
bad_tag = ['home']
#city = 'NY'
city = 'CA'

def save(info, city):
    '''
    Save files
    
    input
    --------------------------
    info: str
    city: venue of the city
    
    '''
    with open(os.path.join(path, os.path.normpath('data/venue_tag_orig_' + city + '.csv')), 'a') as f:
        f.write(info)
    
def tag_generate(df):
    '''
    Extract tag from venue info
    
    input
    -------------------------
    df: venue info df
    city: venue of the city
    
    @features
    venue_id|name|latitude|longitude|categories|country|city|venue_descript|tags
    @popularity
    rating|likes_count|tips_count|checkins_count|users_Count|visits_Count
    
    Note:
        tags: categories + tags
    '''
    for i, row in df.iterrows():
        info = str(row['venue_id']) + ',' + str(row['name']) + ','
        tag_set = set()
        if row['categories'] is not np.nan and row['categories'] != '':
            categories = str(row['categories']).lower()
            for t in categories.split():
                tag_set.add(t)
        if row['tags'] is not np.nan and row['tags'] != '':
            tags = str(row['tags']).lower()
            for t in tags.split():
                tag_set.add(t)
        if len(tag_set) == 0:
            continue
        #if 'home' in tag_set or 'private' in tag_set:
            #return
        for t in tag_set:
            info += str(t) + '|'
        info = info[:-1] +  '\n'
        save(info, city)
     
def city_venue():
    venue_info = pd.read_csv(os.path.join(path, os.path.normpath('data/venue_info_' + city + '.csv')), sep = '|', dtype = str)
    tag_generate(venue_info) 
    
names1 = ['venue_id', 'venue_name', 'tags']

def venue_tag_split():
    '''
    item-tag
    
    input
    ----------------------------
    venue_id, venue_name, tag(|)
    
    ouput
    ----------------------------
    venue_id|tag
    
    '''
    item_tag = pd.read_csv(os.path.join(path, os.path.normpath('data/venue_tag_orig_' + city + '.csv')), names = names1, dtype = str)
    item_tag.drop('venue_name', axis = 1, inplace = True)
    for i, row in item_tag.iterrows():
        info = ''
        tags = str(row['tags']).split('|')
        if len(tags) == 0:
            continue
        for t in tags:
            info += str(row['venue_id']) + '|' + str(t) + '\n'
        with open(os.path.join(path, os.path.normpath('data/venue_tag_split_' + city + '.csv')), 'a') as f:
            f.write(info)

def isValid(x):
    '''
    all letter
    with number or '-'
    '''
    tag = re.compile('^[a-z\-]+$')
    match = tag.match(x)
    if match and len(x) > 2:
        return True
    else:
        return False

def isNumber(x):
    num = re.compile('^[0-9\.\-]+$')
    match = num.match(x)
    if match:
        return True
    else:
        return False

def dotEnd(x):
    dot = re.compile('.+\.+$')
    match = dot.match(x)
    if match:
        return True
    else:
        return False
        
def possTrans(x):
    s = re.compile(".+'s+$")
    match = s.match(x)
    if match:
        return x[:-2]
    else:
        return x

#filter_tag = ['nyc']
private_tag = ['home', 'private']
    
def venue_tag_filtering():
    '''
    keep all valid tag
    
    filter
    -------------------
    1.not letter
    2.stop words
    3.not noun
    
    '''
    item_tag = pd.read_csv(os.path.join(path, os.path.normpath('data/venue_tag_split_' + city + '.csv')), sep = '|', names = ['item', 'tag'], dtype = str) 
    private_venue = item_tag[item_tag['tag'].isin(private_tag)]['item']
    private_venue.to_csv(os.path.join(path, os.path.normpath('data/venue_private_' + city + '.csv')), sep = '|', index = False, encoding = 'utf-8')
        
    item_tag = item_tag[item_tag['tag'].notnull()]
    #item_tag = item_tag[~item_tag['tag'].apply(isNumber)]
    # tranformation
    item_tag = item_tag[~item_tag['tag'].apply(dotEnd)]
    dot_end = item_tag[item_tag['tag'].apply(dotEnd)]
    dot_end['tag'] = dot_end['tag'].apply(lambda x : x.replace('.', ''))
    item_tag = pd.concat([item_tag, dot_end])
    item_tag['tag'] = item_tag['tag'].apply(possTrans)
    # filtering
    item_tag.drop_duplicates(inplace = True)
    item_tag = item_tag[item_tag['tag'].apply(isValid)] 
    item_tag = item_tag[~item_tag['tag'].isin(english_stopwords)]
    item_tag = item_tag[~item_tag['tag'].isin(private_tag)]
    item_tag.sort_index(by = 'item', inplace = True)
    '''
    tags = list(item_tag['tag'])
    pos = [p[1] for p in nltk.pos_tag(tags)]
    item_tag['pos'] = pos
    item_tag = item_tag[item_tag['pos'].isin(valid_tag)]
    item_tag.drop('pos', axis = 1, inplace = True)
    '''
    # stemming
    item_tag['tag'] = item_tag['tag'].apply(porter.stem)
    item_tag.drop_duplicates(inplace = True)
    item_tag.to_csv(os.path.join(path, os.path.normpath('data/venue_tag_filtered_' + city + '.csv')), sep = '|', index = False, header = False, encoding = 'utf-8')
    

    
    
           