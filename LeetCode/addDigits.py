# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 19:31:17 2016

@author: zhengyaolin
"""

class Solution(object):
    def addDigits(self, num):
        """
        :type num: int
        :rtype: int
        """
        #return self.do_add(str(num))
        if num == 0:
            return 0
        return (num - 1) % 9 + 1       
  