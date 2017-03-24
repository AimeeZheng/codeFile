# -*- coding: utf-8 -*-
"""
Created on Thu Mar 16 14:59:48 2017

@author: zhengyaolin
"""

def Hanoi(n, a = 'A', b = 'B', c = 'C'):
    if n == 1:
        print(n, 'from', a, 'to', c)
    else:
        Hanoi(n - 1, a, c, b)
        print(n, 'from', a, 'to', c)
        Hanoi(n - 1, b, a, c)
        