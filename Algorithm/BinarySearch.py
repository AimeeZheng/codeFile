# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 14:54:44 2017

@author: zhengyaolin
"""

def binarySearch(A, x):
    if len(A) < 1:
        return False
    mid = len(A) // 2
    if x == A[mid]:
        return True
    elif x < A[mid]:
        return binarySearch(A[:mid], x)
    else:
        return binarySearch(A[mid + 1:], x)
    
