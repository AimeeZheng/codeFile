# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 11:01:17 2016

@author: zhengyaolin
@description: contextual feature generation
@Note: 
    Extract feature from venue description and tips
    
    n-sentences < 3 ——> POS filter
    n-sentences >= 3 ——> TF and POS 

"""

import pandas as pd
import os
import re
# import package of natural language toolkit
import nltk
from nltk.corpus import stopwords
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

#city = 'NY'
city = 'CA'
path = os.getcwd()
desc_name = ['venue_id', 'desc']
tag_name = ['venue_id', 'tag']
english_punctuations = [',', '.', ':', ';', '?', '(', ')', '[', ']', '&', '!', '*', '@', '#', '$', '%', '+', '-', '=']
english_stopwords = stopwords.words('english')
porter = nltk.PorterStemmer()
# wnl = nltk.WordNetLemmatizer()
noun_tag = ['NN', 'NNS', 'NNP', 'NNPS', 'VBG']
adj_tag = ['JJ', 'JJR', 'JJS']
collocations = dict()
#dict([[i[0],1] for i in np.array(pd.read_csv(os.path.join(path, os.path.normpath('data/venue_tags_collocations.csv')), header = None, dtype = str))]) 
useless_tag = ['nyc', 'new york', 'home', 'private'] 

def isNull(x):
    noLetter = re.compile("^[0-9\']+$")
    match = noLetter.match(x)
    if x.strip() == '' or match:
        return True
    return False

def venue_tips_city():
    tips = pd.read_csv(os.path.join(path, os.path.normpath("data/user_tips.csv")), sep = '|', dtype = str)
    venue_info = pd.read_csv(os.path.join(path, os.path.normpath('data/venue_info_' + city + '.csv')), sep = '|', dtype = str)
    venue_ids = venue_info['venue_id'].unique()
    tips_city = tips[tips['venue_id'].isin(venue_ids)]
    tips_city = tips_city[['user_id', 'venue_id', 'tips']]
    tips_city.to_csv(os.path.join(path, os.path.normpath('data/venue_tips_' + city + '.csv')), sep = '|', encoding = 'utf-8', index = False)
    

def merge_desc_tips():
    venue_info = pd.read_csv(os.path.join(path, os.path.normpath('data/venue_info_' + city + '.csv')), sep = '|', dtype = str)
    desc = venue_info[['venue_id', 'venue_descript']]
    desc.dropna(how = 'any', inplace = True)
    desc.columns = desc_name
    venue_tips = pd.read_csv(os.path.join(path, os.path.normpath('data/venue_tips_' + city + '.csv')), sep = '|', dtype = str)
    venue_tips = venue_tips[['venue_id', 'tips']]
    venue_tips.dropna(how = 'any', inplace = True)
    venue_tips.columns = desc_name
    desc = pd.concat([desc, venue_tips], ignore_index = True)
    desc.sort_index(by = 'venue_id', inplace = True)
    desc = desc[~desc['desc'].apply(isNull)]
    desc.to_csv(os.path.join(path, os.path.normpath('data/venue_desc_merge_' + city + '.csv')), sep = '|', index = False, header = False, encoding = 'utf-8')

def bigram_word_find(words, score_fn = BigramAssocMeasures.likelihood_ratio, n = 10):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return bigrams

def isValid(x):
    '''
    number or symbol
    '''
    regex = re.compile('^[a-z\-]+$')
    match = regex.match(x)
    if match:
        return True
    else:
        return False

def generate():
    '''
    Extract tag from venue description
    '''
    venue_desc = pd.read_csv(os.path.join(path, os.path.normpath('data/venue_desc_merge_' + city + '.csv')), sep = '|', names = desc_name, dtype = str)
    for venue, group in venue_desc.groupby('venue_id'):
        desc = group['desc']
        sentences = []
        words = []
        # sentences split
        for d in desc:
            sentences.extend(nltk.sent_tokenize(d))
        # words split
        for s in sentences:
            words.extend(nltk.word_tokenize(s))
        # lower
        words = [w.lower() for w in words]
        # words filter
        words = [w for w in words if len(w) >= 3 and isValid(w)]
        # stopwords filter
        words = [w for w in words if w not in english_stopwords]
        # punctuations filter
        words = [w for w in words if w not in english_punctuations]
        # stemming
        words = [porter.stem(w) for w in words]
        # lemmatize
        # words = [wnl.lemmatize(w) for w in words]
        
        # extract tag
        tags = []
        if len(sentences) < 3:
            pos_tagged_words = nltk.pos_tag(words)
            tags = [i[0] for i in pos_tagged_words if i[1] in noun_tag]
        else:
            tagged_words_dict = dict(nltk.pos_tag(words))
            freqdist = nltk.FreqDist(words)
            try:
                bigrams = bigram_word_find(words, n = 10)
                for bi in bigrams:
                    f1 = freqdist[bi[0]]
                    f2 = freqdist[bi[1]]
                    p1 = tagged_words_dict[bi[0]]
                    p2 = tagged_words_dict[bi[1]]
                    if bi[0] ==  bi[1]:
                        continue
                    bi_str = bi[0] + ' ' + bi[1]
                    if bi_str in collocations.keys() or (f1 >= 3 and f2 >= 3 and f1 == f2) or (f1 >= 3 and f2 >= 3 and (p1 in noun_tag or p1 in adj_tag) and p2 in noun_tag):
                        print(bi_str)
                        tags.append(bi_str)
                        if bi_str not in collocations.keys():
                            collocations[bi_str] = 1
                        if bi[0] in freqdist.keys():
                            freqdist.pop(bi[0])
                        if bi[1] in freqdist.keys():
                            freqdist.pop(bi[1])
            except ValueError as e:
                print(e)
            for i in freqdist.items():
                if i[1] >= 3:
                    tags.append(i[0])
        
        # saving 
        info = ''
        if len(tags) > 0:
            for t in tags:
                info += str(venue) + '|' + str(t) + '\n'
        with open(os.path.join(path, os.path.normpath('data/venue_tags_extrat_' + city + '.csv')), 'a') as f:
            f.write(info)

def tag_filter():
    venue_tag = pd.read_csv(os.path.join(path, os.path.normpath('data/venue_tags_extrat_' + city + '.csv')), names = tag_name, sep = '|', dtype = str)
    venue_tag_filter = venue_tag[~venue_tag['tag'].isin(useless_tag)]
    private_venue =  pd.read_csv(os.path.join(path, os.path.normpath('data/venue_private_' + city + '.csv')),header = None, sep = '|', dtype = str)
    private = list(private_venue[0])
    venue_tag_filter = venue_tag[~venue_tag['venue_id'].isin(private)]
    venue_tag_filter.drop_duplicates(inplace = True)
    venue_tag_filter.to_csv(os.path.join(path, os.path.normpath('data/venue_tags_extrat_filtered_' + city + '.csv')), index = False, header = False, sep = '|', encoding = 'utf-8')
        
def tag_merge():
    venue_tag_extract = pd.read_csv(os.path.join(path, os.path.normpath('data/venue_tags_extrat_filtered_' + city + '.csv')), header = None, sep = '|', dtype = str)
    venue_tag = pd.read_csv(os.path.join(path, os.path.normpath('data/venue_tag_filtered_' + city + '.csv')), header = None, sep = '|', dtype = str)
    #venue_tag = venue_tag[~venue_tag[1].isin(english_stopwords)]
    #venue_tag = venue_tag[~venue_tag[1].apply(lambda x : len(x) < 3)]
    #venue_tag = venue_tag[venue_tag[1].apply(isValid)]
    #venue_tag[1] = venue_tag[1].apply(lambda x : porter.stem(x))
    venue_tag.drop_duplicates(inplace = True)
    df = pd.concat([venue_tag_extract, venue_tag])
    df.drop_duplicates(inplace = True)
    df.sort_index(by = 0, inplace = True)
    df.to_csv(os.path.join(path, os.path.normpath('data/venue_tags_merged_' + city + '.csv')), index = False, header = False, sep = '|', encoding = 'utf-8')
    
    
if __name__ == "__main__": 
    pass

    
