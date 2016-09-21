# -*- coding: utf-8 -*-
"""
Created on Mon Sep 19 14:13:11 2016

@author: zhengyaolin
"""

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
    
class Solution:
    # @param {TreeNode} root
    # @return {string[]}
    def binaryTreePaths(self, root):
        self.paths = []
        if root is not None:
            self.get_path(root, str(root.val))
        return self.paths
            
    def get_path(self, node, path):
        if node.left is None and node.right is None:
            self.paths.append(path)
        if node.left is not None:
            self.get_path(node.left, path + "->" + str(node.left.val))
        if node.right is not None:
            self.get_path(node.right, path + "->" + str(node.right.val))