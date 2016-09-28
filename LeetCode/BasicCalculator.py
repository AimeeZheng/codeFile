# -*- coding: utf-8 -*-
"""
Created on Thu Sep 15 08:20:25 2016

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
        if len(s) == 0:
            return 0
        s = list(s)
        stack = []
        i = 0
        while i < len(s):
            if self.isDigit(s[i]):
                num = s[i]
                while i + 1 < len(s) and self.isDigit(s[i + 1]):
                    num += s[i + 1]
                    i += 1
                stack.append(num)
            elif s[i] == ')':
                pop = []
                x = stack.pop()
                while  x != '(':
                    pop.append(x)
                    x = stack.pop()
                pop.reverse()
                stack.append(self.cal(pop))
            else:
                stack.append(s[i])
            i += 1
        if len(stack) != 1:
            return(int(self.cal(stack)))
        else:
            return int(stack[0])
        
    def isDigit(self, c):
        if re.match('[0-9]', c) is None:
            return False
        return True
    
    def cal(self, s):
        result = 0
        x = 0
        plus = True
        for i in s:
            if i == '+':
                plus = True
            elif i == '-':
                plus = False
            else:
                x = int(i)
                if plus:
                    result += x
                else:
                    result -= x
        return str(result)
        