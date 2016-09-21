# -*- coding: utf-8 -*-
"""
@description Binary Tree inorder/preorder/postorder traversal
@author: zhengyaolin
"""
_result = []

class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

#中序遍历        
def inorderTraversal(root):
    """
    iterative solution
    left -> root -> right
    
    :type root: TreeNode
    :rtype: List[int]
    """
    result = []
    if root is None:
        return result
    stack = []
    node = root
    while len(stack) > 0 or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        result.append(node.val)
        node = node.right
    return result

def inorderTraversal2(root):
    """
    recursive solution
    left -> root -> right
    
    :type root: TreeNode
    :rtype: List[int]
    """
    if root is None:
        return _result
    inorder(root)
    return _result
    
def inorder(node):
    if node.left:
        inorder(node.left)
    _result.append(node.val)
    if node.right:
        inorder(node.right)
  
#先序遍历  
def preorderTraversal(root):
    """
    iterative solution
    root -> left -> right
    
    :type root: TreeNode
    :rtype: List[int]
    """
    result = []
    if root is None:
        return result
    stack = []
    node = root
    while len(stack) > 0 or node:
        while node:
            stack.append(node)
            result.append(node.val)
            node = node.left
        node = stack.pop()
        node = node.right
    return result
    
def preorderTraversal2(root):
    """
    iterative solution
    root -> left -> right
    
    :type root: TreeNode
    :rtype: List[int]
    """
    if root is None:
        return _result
    preorder(root)
    return _result    
    
def preorder(node):
    _result.append(node.val)
    if node.left:
        preorder(node.left)
    if node.right:
        preorder(node.right)

#后序遍历        
def postorderTraversal(root):
    """
    iterative solution
    left -> right -> root 
    
    :type root: TreeNode
    :rtype: List[int]
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
    
def postorderTraversal2(root):
    """
    iterative solution
    left -> right -> root
    
    :type root: TreeNode
    :rtype: List[int]
    """
    if root is None:
        return _result
    postorder(root)
    return _result    
    
def postorder(node):
    if node.left:
        postorder(node.left)
    if node.right:
        postorder(node.right)
    _result.append(node.val)
    
#test   
        