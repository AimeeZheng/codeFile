# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 15:43:47 2016

@author: zhengyaolin
"""

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
        
class Solution(object):
    def preorderTraversal(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """
        self.nodes = []
        result = []
        if root is not None:
            self.nodes.append(root)
            self.pre_traverse(root)
        for i in self.nodes:
            result.append(i.val)
        return result
    
    def pre_traverse(self, node):
        if node.left is None and node.right is None:
            return
        if node.left is not None:
            self.nodes.append(node.left)
            self.pre_traverse(node.left)
        if node.right is not None:
            self.nodes.append(node.right)
            self.pre_traverse(node.right)

