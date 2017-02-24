# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 17:43:25 2017

@author: zhengyaolin
"""
        
def left(i):
    return 2 * i
    
def right(i):
    return 2 * i + 1

def parent(i):
    return i // 2
    
def max_heapify(A, i):
    l = left(i)
    r = right(i)
    if l <= heap_size and A[i] < A[l]:
        largest = l
    else:
        largest = i
    if r <= heap_size and A[r] > A[largest]:
        largest = r
    # parent < children => exchange
    if largest != i:
        tmp = A[i]
        A[i] = A[largest]
        A[largest] = tmp
        max_heapify(A, largest)
        
def build_max_heap(A):
    #A[1:l] start from 1
    mid = (len(A) - 1) // 2
    for i in range(mid, 0, -1):
        max_heapify(A, i)
    
def heapSort(A):
    #build
    build_max_heap(A)
    #exchange A[1] with A[size]
    for i in range(len(A)-1, 1, -1):
        last = A[1]
        A[1] = A[i]
        A[i] = last
        global heap_size
        heap_size -= 1
        max_heapify(A, 1)

A = [4,1,3,2,16,9,10,14,8,7]
heap_size = len(A)
A.insert(0, 0)  
heapSort(A)
print(A[1:])
