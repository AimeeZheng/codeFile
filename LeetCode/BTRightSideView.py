# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 15:25:52 2016

@author: zhengyaolin
"""

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def rightSideView(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """
        result = []
        if not root:
            return result
        nodes = [root]
        while len(nodes) > 0:
            children = []
            for node in nodes:
                if node.left:
                    children.append(node.left)
                if node.right:
                    children.append(node.right)
            result.append(nodes[-1].val)
            nodes = children
        return result
       
            