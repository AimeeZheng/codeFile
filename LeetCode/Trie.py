# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 09:31:02 2016

@author: zhengyaolin
"""
class TrieNode(object):
    '''前缀树节点
    
    Attributes
    ----------
    value：节点存储的字符
    children：节点的子节点 dict {ch: TrieNode}
    '''
    def __init__(self):
        """
        Initialize your data structure here.
        """
        self.value = None
        self.flag = False
        self.children = {}
        

class Trie(object):

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        """
        Inserts a word into the trie.
        :type word: str
        :rtype: void
        """
        node = self.root
        for ch in word:
            if ch not in node.children:
                child = TrieNode()
                child.value = ch
                node.children[ch] = child
                node = child
            else:
                node = node.children[ch]
        node.flag = True
            

    def search(self, word):
        """
        Returns if the word is in the trie.
        :type word: str
        :rtype: bool
        """
        node = self.root
        for ch in word:
            if ch not in node.children:
                return False
            else:
                node = node.children[ch]
        return node.flag
        
    def startsWith(self, prefix):
        """
        Returns if there is any word in the trie
        that starts with the given prefix.
        :type prefix: str
        :rtype: bool
        """
        node = self.root
        for ch in prefix:
            if ch not in node.children:
                return False
            else:
                node = node.children[ch]
        return True
            
            
# Your Trie object will be instantiated and called as such:
# trie = Trie()
# trie.insert("somestring")
# trie.search("key")



