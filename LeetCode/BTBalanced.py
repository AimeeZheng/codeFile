# -*- coding: utf-8 -*-
"""
Created on Fri Sep  2 11:14:09 2016

@author: zhengyaolin
"""

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):        
    def isBalanced(self, root):
        """
        :type root: TreeNode
        :rtype: bool
        """
        if root is None:
            return True
        left = root.left
        right = root.right
        if abs(self.height(left) - self.height(right)) <= 1:
            return self.isBalanced(left) and self.isBalanced(right)
        return False
    
    def height(self, node):
        if node is None:
            return 0
        return max(self.height(node.left), self.height(node.right)) + 1
        
            
        
        