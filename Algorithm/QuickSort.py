# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 17:06:12 2017

@author: zhengyaolin
"""

def quickSort(A, p, r):
    if p < r:
        q = partition(A, p, r)
        quickSort(A, p, q-1)
        quickSort(A, q+1, r)
    
def partition(A, p, r):
    #pivot
    x = A[r]
    i = p - 1
    #compare
    for j in range(p, r):
        if A[j] <= x:
            i += 1
            #exchange
            tmp = A[j]
            A[j] = A[i]
            A[i] = tmp
    q = i + 1
    A[r] = A[q]
    A[q] =  x
    return q
    
A = [2,8,7,1,3,5,6,4]
quickSort(A, 0, 7)
print(A)
    