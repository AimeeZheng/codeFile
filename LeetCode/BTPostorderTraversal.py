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
    def postorderTraversal(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        """
        self.nodes = []
        result = []
        if root is not None:
            self.post(root)
            result = [n.val for n in self.nodes]
        return result
        
    
    def post(self, node):
        """
        Recursive solution 
        """
        if node.left is not None:
            self.post(node.left)
        if node.right is not None:
            self.post(node.right)
        self.nodes.append(node)


    def iter_postorderTraversal(self, root):
        """
        :type root: TreeNode
        :rtype: List[int]
        note: Iterative solution
        """
        result = []
        if root is None:
            return result
        stack = []
        stack.append(root)
        stack.append(root)
        while len(stack) > 0:
            node = stack.pop()
            if len(stack) > 0 and node == stack[-1]: #未访问过
                if node.right:
                    stack.append(node.right)
                    stack.append(node.right)
                if node.left:
                    stack.append(node.left)
                    stack.append(node.left)
            else:
                result.append(node.val)
        return result    
                