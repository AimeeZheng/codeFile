package zyl.leetCode;

import java.util.HashMap;

class TrieNode {
	// Initialize your data structure here.
	public char value;

	public boolean flag = false;

	public HashMap<Character, TrieNode> children = new HashMap<Character, TrieNode>();
	
	public TrieNode() {
	}

	public TrieNode(char c) {
		this.value = c;
	}
}

public class Trie {
    private TrieNode root;

    public Trie() {
        root = new TrieNode();
    }

    // Inserts a word into the trie.
    public void insert(String word) {
		TrieNode node = this.root;
		for (int i = 0; i < word.length(); i++) {
			Character c = word.charAt(i);
			if (!node.children.containsKey(c)) {
				TrieNode child = new TrieNode(c);
				node.children.put(c, child);
				node = child;
			} else {
				node = node.children.get(c);
			}
		}
		node.flag = true;
    }

    // Returns if the word is in the trie.
    public boolean search(String word) {
		TrieNode node = this.root;
		for (int i = 0; i < word.length(); i++) {
			Character c = word.charAt(i);
			if (!node.children.containsKey(c)) {
				return false;
			} else {
				node = node.children.get(c);
			}
		}
		return node.flag;
    }

    // Returns if there is any word in the trie
    // that starts with the given prefix.
    public boolean startsWith(String prefix) {
		TrieNode node = this.root;
		for (int i = 0; i < prefix.length(); i++) {
			Character c = prefix.charAt(i);
			if (!node.children.containsKey(c)) {
				return false;
			} else {
				node = node.children.get(c);
			}
		}
		return true;
	}

	public static void main(String[] args) {
		Trie tree = new Trie();
		tree.insert("hello");
		tree.insert("a");
		System.out.println(tree.search("a"));
	}
}
