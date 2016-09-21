# -*- coding: utf-8 -*-
"""
Created on Wed Aug 31 15:33:45 2016

@author: zhengyaolin
"""

class Node(object):
    '''Node of Trie
    
    Attributes
    ----------
    value: character in Node 
    children: children of Node dict {c: Node}
    flag: a string if True
    '''
    def __init__(self):
        self.value = None
        self.children = {}   
        self.flag = False
        
        
class WordDictionary(object):
    def __init__(self):
        """
        initialize your data structure here.
        """
        self.root = Node()        

    def addWord(self, word):
        """
        Adds a word into the data structure.
        :type word: str
        :rtype: void
        """
        node = self.root
        for c in word:
            if c not in node.children:
                child = Node()
                child.value = c
                node.children[c] = child
                node = child
            else:
                node = node.children[c]
        node.flag = True
     

    def search(self, word):
        """
        Returns if the word is in the data structure. A word could
        contain the dot character '.' to represent any one letter.
        :type word: str
        :rtype: bool
        """
        return self.find(self.root, word)
        
                    
    def find(self, node, word):
        #print('node:', node.value)
        #print('search word:', word)
        if word == '':
            return node.flag
        for c in word:
            #print('search char', c)
            if c == '.':
                for child in node.children.values():
                    if self.find(child, word[1:]) is True:
                        return True
                return False
            else:
                if c in node.children:
                    child = node.children[c]
                    if self.find(child, word[1:]) is True:
                        return True
                return False
         
# Your WordDictionary object will be instantiated and called as such:
# wordDictionary = WordDictionary()
# wordDictionary.addWord("word")
# wordDictionary.search("pattern")