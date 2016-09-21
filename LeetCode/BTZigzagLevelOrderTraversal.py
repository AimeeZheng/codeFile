# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 15:47:19 2016

@author: zhengyaolin
"""

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Solution(object):
    def zigzagLevelOrder(self, root):
        """
        :type root: TreeNode
        :rtype: List[List[int]]
        """
        result = []
        if not root:
            return result
        nodes = [root]
        flag = True
        while len(nodes) > 0:
            if flag:
                tmp = [n.val for n in nodes]
            else:
                nodes.reverse()
                tmp = [n.val for n in nodes]
                nodes.reverse()
            result.append(tmp)
            next_level = []
            for node in nodes:
                if node.left:
                    next_level.append(node.left)
                if node.right:
                    next_level.append(node.right)
            flag = not flag
            nodes = next_level
        return result
    
