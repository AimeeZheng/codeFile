# -*- coding: utf-8 -*-
"""
Created on Mon Mar 20 15:46:39 2017

@author: zhengyaolin
"""

def compare_pattern_prefix(P):
    """
    generate pi[]
    """
    len_p = len(P)
    pi = [0] * len_p
    pi[0] = -1
    j = -1
    for i in range(1, len_p):
        while j >= 0 and P[i] != P[j + 1]:
            j = pi[j]
        if P[i] == P[j + 1]:
            j += 1
        pi[i] = j
    return pi
    
def KMP_matcher(S, P):
    """
    The Knuth-Morris-Pratt Algorithm
    O(m + n)
    """
    pi = compare_pattern_prefix(P)
    n = len(S)
    m = len(P)
    j = -1
    for i in range(n):
        while j >= 0 and S[i] != P[j + 1]:
            j = pi[j]
        if S[i] == P[j + 1]:
            j += 1
        if j == m - 1:
            return i - j
    return -1