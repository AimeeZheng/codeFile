# -*- coding: utf-8 -*-
"""
Created on Sat Sep 17 09:57:12 2016

@author: zhengyaolin
"""

'''
def maxProfit(prices):
    """
    :type prices: List[int]
    :rtype: int
    """
    tmp = sorted(prices)
    tmp.reverse()
    if tmp == prices:
        return 0
    result = 0
    for i in range(len(prices)-1):
        p = prices[i]
        max_p = max(prices[i+1:])
        if max_p > p:
            result = max(result, max_p - p)
    return result
'''
       
def maxProfit1(prices):
    """
    :type prices: List[int]
    :rtype: int
    """
    if len(prices) < 2:
        return 0
    min_p = prices[0]
    profit = []
    for p in prices:
        profit.append(p - min_p)
        if p < min_p:
            min_p = p
    max_p = max(profit)
    if max_p < 0:
        return 0
    return max_p

def maxProfit2(prices):
    """
    :type prices: List[int]
    :rtype: int
    """
    if len(prices) < 2:
        return 0
    p_ = prices[0]
    result = 0
    for p in prices[1:]:
        if p > p_:
           result += p - p_
        p_ = p
    return result
    
def maxProfit3(prices):
    """
    :type prices: List[int]
    :rtype: int
    """
    if len(prices) < 2:
        return 0
    n = len(prices)
    preProfit = [0 for i in range(n)]
    postProfit = [0 for i in range(n)]
    
    curMin = prices[0]
    for i in range(1, n):
        preProfit[i] = max(preProfit[i - 1], prices[i] - curMin)
        if prices[i] < curMin:
            curMin = prices[i]
    
    curMax = prices[-1]
    for i in range(n-2, -1, -1):
        postProfit[i] = max(postProfit[i + 1], curMax - prices[i])
        if prices[i] > curMax:
            curMax = prices[i]
    
    max_p = 0
    for i in range(n):
        max_p = max(max_p, preProfit[i] + postProfit[i])
        
    return max_p

def maxProfit4(k, prices):
    """
    :type k: int
    :type prices: List[int]
    :rtype: int
    """
    if len(prices) < 2 or k < 1:
        return 0
    n = len(prices)
    if k >= n:
        p_ = prices[0]
        result = 0
        for p in prices[1:]:
            if p > p_:
               result += p - p_
            p_ = p
        return result
    l = [0 for i in range(n+1)]
    g = [0 for i in range(n+1)]
    for i in range(n-1):
        diff = prices[i + 1] - prices[i]
        for j in range(k, 0, -1):
            l[j] = max(g[j - 1] + max(diff, 0), l[j] + diff)
            g[j] = max(g[j], l[j])
    return g[k]

        