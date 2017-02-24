# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 11:02:47 2017

@author: zhengyaolin
"""

def insertionSort(A):
    for j in range(1, len(A)):
        key = A[j]
        i = j - 1   
        while i >= 0 and A[i] > key:
            A[i + 1] = A[i]
            i -= 1
        A[i + 1] = key
        
A = [5,2,4,6,1,3]
insertionSort(A)
print(A)