# -*- coding: utf-8 -*-
"""
Created on Mon Sep 26 17:06:04 2016

@author: zhengyaolin
"""

def getHint(secret, guess):
    """
    :type secret: str
    :type guess: str
    :rtype: str
    """
    A = 0
    B = 0
    secret_tmp = ''    
    guess_tmp = ''
    for i in range(len(secret)):
        if secret[i] == guess[i]:
            A += 1
        else:
            secret_tmp += secret[i]
            guess_tmp += guess[i]
            
    for i in set(secret_tmp):
        if i in secret_tmp:
            B += min(secret_tmp.count(i), guess_tmp.count(i))
    return "%dA%dB" % (A, B)
    
