# -*- coding: utf-8 -*-
"""
Created on Fri Sep 16 07:52:57 2016

@author: zhengyaolin
"""
import re

class Solution(object):
    def calculate(self, s):
        """
        :type s: str
        :rtype: int
        """
        s = s.replace(' ', '')
        s = s + 'x'
        nums = []
        num = ''
        op = '+'
        for c in s:
            if self.isDigit(c):
                num += c
            else:
                if op == '+':
                    nums.append(int(num))
                elif op == '-':
                    nums.append(-int(num))
                elif op == '*':
                    nums.append(int(num) * nums.pop())
                elif op == '/':
                    tmp = nums.pop()
                    if tmp//int(num) < 0 and tmp % int(num) != 0:
                        nums.append(tmp // int(num)+1)
                    else:
                        nums.append(tmp // int(num))
                    #nums.append(nums.pop() / int(num))
                op = c
                num = ''
        result = 0
        for n in nums:
            result += n
        return result
        
    def isDigit(self, c):
        if re.match('[0-9]', c) is None:
            return False
        return True
        
