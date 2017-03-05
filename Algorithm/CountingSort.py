# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 10:38:07 2017

@author: zhengyaolin
"""

def countingSort(A, k):
    l = len(A)
    C = []
    # initialize C[0...k]
    C = [0 for i in range(k + 1)]
    # counting
    for i in A:
        C[i] += 1
    # counting <=
    for i in range(1, k + 1):
        C[i] = C[i] + C[i - 1]
    # result
    B = [0 for i in range(l)]
    for i in range(l - 1, -1, -1):
        B[C[A[i]] - 1] = A[i]
        C[A[i]] -= 1
    return B

A = [2,5,3,0,2,3,0,3]
B = countingSort(A, 5)
print(B)