# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 13:48:34 2016

@author: zhengyaolin
"""
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
        
class Solution(object):
    def inorderTraversal(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """
        stack = []
        result = []
        while root is not None:
            stack.append(root)
            root = root.left
        
        while len(stack) > 0:
            tmp = stack.pop()
            result.append(tmp.val)
            node = tmp.right
            while node is not None:
                stack.append(node)
                node = node.left
                
        return result
    