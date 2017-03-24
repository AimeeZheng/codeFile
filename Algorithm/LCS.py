# -*- coding: utf-8 -*-
"""
Created on Fri Mar 24 10:06:43 2017

@author: zhengyaolin
"""

def LCS(x, y):
    """
    Longest common sequence of x and y
    """
    m = len(x) + 1
    n = len(y) + 1
    c = [[0] * n] * m
    for i in range(1, m):
        for j in range(1, n):
            if x[i - 1] == y[j - 1]:
                c[i][j] = c[i - 1][j - 1] + 1
            else:
                c[i][j] = max(c[i - 1][j], c[i][j - 1])
    return c[m - 1][n - 1]
    
