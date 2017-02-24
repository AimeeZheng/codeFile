# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 10:32:36 2017

@author: zhengyaolin
"""

def merge(A, p, q, r):
    # merge A[p:q] and A[q+1:r]
    L = A[p:q+1]
    R = A[q+1:r+1]
    # guard
    L.append(float('inf'))
    R.append(float('inf'))
    i = 0
    j = 0
    for k in range(p, r+1):
        if L[i] <= R[j]:
            A[k] = L[i]
            i += 1
        elif j <= r:
            A[k] = R[j]
            j += 1
    
def mergeSort(A, p, r):
    if p < r: 
        q = (p + r) // 2
        mergeSort(A, p, q)
        mergeSort(A, q+1, r)
        merge(A, p, q, r)
        
A = [2,4,5,7,1,2,3,6]
mergeSort(A, 0, 7)
print(A)