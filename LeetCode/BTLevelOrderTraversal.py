# -*- coding: utf-8 -*-
"""
Created on Sun Sep 18 13:38:47 2016

@author: zhengyaolin
"""

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
        
class Solution(object):
    def levelOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """
        self.level = []
        if root is not None:
            self.search([root])
        return self.level
        
    def search(self, nodes):
        children = []
        val = []
        for node in nodes:
            val.append(node.val)
            left = node.left
            right = node.right
            if left is not None:
                children.append(left)
            if right is not None:
                children.append(right)
        self.level.append(val)
        if len(children) != 0:
            self.search(children)
        
    def levelOrderBottom(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """
        self.level = []
        if root is not None:
            self.search([root])
        self.level.reverse()
        return self.level
            
        
        
        