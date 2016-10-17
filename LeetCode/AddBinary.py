# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 19:30:18 2016

@author: zhengyaolin
"""
class Solution(object):
    def addBinary(self, a, b):
        """
        :type a: str
        :type b: str
        :rtype: str
        """
        print('a:', a, 'b', b)
        len_a = len(a)
        len_b = len(b)
        if len_a > len_b:
            n = len_a
            num1 = [int(i) for i in a]   
            num2 = [0 for i in range(n - len_b)] + [int(i) for i in b]
        else:
            n = len_b
            num1 = [0 for i in range(n - len_a)] + [int(i) for i in a]   
            num2 = [int(i) for i in b]
            
        print('num1, num2', num1, num2)
        num1.reverse()
        num2.reverse()        
        carry = 0
        sum_2 = []
        for i in range(n):
            num = (num1[i] ^ num2[i]) ^ carry
            sum_tmp = num1[i] + num2[i] + carry
            sum_2.append(num)
            carry = 0
            if sum_tmp >= 2:
                carry = 1
        if carry == 1:
            sum_2.append(1)
        sum_2.reverse()
        result = ''.join([str(i) for i in sum_2])
        return result