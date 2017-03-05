# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 11:20:46 2017

@author: zhengyaolin
"""
class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None
        
        
def levelOrder(root):
    result = []
    queue = []
    queue.append(root)
    while len(queue) > 0:
        node = queue[0]
        result.append(node.val)
        queue = queue[1:]
        if node.left:
            queue.append(node.left)
        if node.right:
            queue.append(node.right)
    return result
    
            
                
        
        