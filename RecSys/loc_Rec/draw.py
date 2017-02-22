# -*- coding: utf-8 -*-
"""
Created on Wed Dec  7 14:14:24 2016

@author: zhengyaolin
"""
import matplotlib.pyplot as plt
import os
import pandas as pd

path = os.getcwd()

#颜色
colors = ['b', 'g', 'r', 'c', 'm', 'y']
plt.style.use('ggplot')

def senti_dis():
    senti_df = pd.read_csv(os.path.join(path, os.path.normpath('data/sentiment_score_norm_NY.csv')), names = ['user_id', 'venue_id', 'ss_norm'], sep = '|', dtype = str)
    senti_df['ss_norm'] = senti_df['ss_norm'].apply(float)
    labels = [-1, -0.5, 0, 0.5, 1]
    count = []
    i = 0
    while i < 20:
        count.append(len(senti_df[(senti_df['ss_norm'] >= (-1 + i * 0.1)) & (senti_df['ss_norm'] <= (-0.9 + i * 0.1))]))
        i += 1
    title = plt.title("Sentiment score for all tips")
    title.set_fontsize(15)
    title.set_position((0.5, 1.05))
    plt.xlabel("Sentiment Score")
    plt.ylabel("Tip Number Count")
    plt.xticks([i * 5 - 0.5 for i in range(5)], labels)
    plt.bar(left = [i for i in range(20)], height = count, width = 1, align = 'center')
    


    