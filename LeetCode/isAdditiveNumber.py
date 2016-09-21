# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 19:32:02 2016

@author: zhengyaolin
"""
import itertools

class Solution(object):   
    def isAdditiveNumber(self, num):
        """
        :type num: str
        :rtype: bool
        """
        #迭代
        n = len(num)
        for i, j in itertools.combinations(range(1, n), 2):
            num1 = num[:i]
            num2 = num[i:j]
            if num1 != str(int(num1)) or num2 != str(int(num2)):
                continue
            while j < n:
                print('num1, num2:', num1, num2)
                num3 = str(int(num1) + int(num2))
                print('num3:', num3)
                if not num.startswith(num3, j):
                    break
                j += len(num3)
                num1, num2 = num2, num3
            if j == n:
                return True
        return False
        
        
    def isAdditiveNumber_(self, num):
        """
        :type num: str
        :rtype: bool
        """    
        #递归
        def notValid(x):
            return len(x) != 1 and x[0] == '0'
        
        def search(a, b, c):
            d = str(int(a) + int(b))
            if not c.startswith(d):
                return False
            if c == d:
                return True
            return search(b, d, c[len(d):])
                
        n = len(num)
        for i in range(1, int(n/2) + 1):
            for j in range(i + 1, n):
                a, b, c = num[:i], num[i:j], num[j:]
                if notValid(a) or notValid(b):
                    continue
                if search(a, b, c):
                    return True
        return False
        