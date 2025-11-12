"""
Trie (Prefix Tree) Data Structure
==================================
A tree structure for storing strings where each node represents a character.

Time Complexity:
- Insert: O(m) where m is length of word
- Search: O(m)
- StartsWith: O(m)
- Delete: O(m)

Space Complexity: O(ALPHABET_SIZE * m * n) where n is number of words

Use Cases:
- Autocomplete
- Spell checker
- IP routing (longest prefix matching)
- Dictionary implementation
- Pattern matching
"""


class TrieNode:
    """Node for Trie"""
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.word_count = 0  # Number of words ending at this node


class Trie:
    """Trie (Prefix Tree) implementation"""
    
    def __init__(self):
        self.root = TrieNode()
        self.word_count = 0
    
    def insert(self, word):
        """Insert a word into the trie"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        
        if not node.is_end_of_word:
            self.word_count += 1
        node.is_end_of_word = True
        node.word_count += 1
    
    def search(self, word):
        """Search for exact word in trie"""
        node = self._find_node(word)
        return node is not None and node.is_end_of_word
    
    def starts_with(self, prefix):
        """Check if any word starts with given prefix"""
        return self._find_node(prefix) is not None
    
    def _find_node(self, prefix):
        """Helper to find node for given prefix"""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return None
            node = node.children[char]
        return node
    
    def delete(self, word):
        """Delete a word from trie"""
        def _delete_recursive(node, word, index):
            if index == len(word):
                if not node.is_end_of_word:
                    return False
                
                node.is_end_of_word = False
                node.word_count -= 1
                return len(node.children) == 0
            
            char = word[index]
            if char not in node.children:
                return False
            
            child = node.children[char]
            should_delete_child = _delete_recursive(child, word, index + 1)
            
            if should_delete_child:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end_of_word
            
            return False
        
        if _delete_recursive(self.root, word, 0):
            self.word_count -= 1
    
    def get_all_words(self):
        """Get all words in trie"""
        words = []
        self._collect_words(self.root, "", words)
        return words
    
    def _collect_words(self, node, prefix, words):
        """Helper to collect all words"""
        if node.is_end_of_word:
            words.append(prefix)
        
        for char, child in node.children.items():
            self._collect_words(child, prefix + char, words)
    
    def autocomplete(self, prefix):
        """Get all words with given prefix"""
        node = self._find_node(prefix)
        if node is None:
            return []
        
        words = []
        self._collect_words(node, prefix, words)
        return words
    
    def count_words_with_prefix(self, prefix):
        """Count words starting with prefix"""
        return len(self.autocomplete(prefix))
    
    def longest_common_prefix(self):
        """Find longest common prefix of all words"""
        if not self.root.children:
            return ""
        
        prefix = []
        node = self.root
        
        while len(node.children) == 1 and not node.is_end_of_word:
            char = next(iter(node.children))
            prefix.append(char)
            node = node.children[char]
        
        return ''.join(prefix)
    
    def __len__(self):
        return self.word_count
    
    def __str__(self):
        return f"Trie({self.get_all_words()})"


class TrieWithWildcard:
    """Trie with wildcard search support"""
    
    def __init__(self):
        self.root = TrieNode()
    
    def insert(self, word):
        """Insert a word"""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
    
    def search(self, word):
        """Search with '.' as wildcard for any character"""
        return self._search_recursive(self.root, word, 0)
    
    def _search_recursive(self, node, word, index):
        """Helper for wildcard search"""
        if index == len(word):
            return node.is_end_of_word
        
        char = word[index]
        
        if char == '.':
            # Wildcard: try all children
            for child in node.children.values():
                if self._search_recursive(child, word, index + 1):
                    return True
            return False
        else:
            # Regular character
            if char not in node.children:
                return False
            return self._search_recursive(node.children[char], word, index + 1)


# Practical applications
def find_longest_word_with_all_prefixes(words):
    """Find longest word such that all its prefixes are also words"""
    trie = Trie()
    for word in words:
        trie.insert(word)
    
    longest = ""
    
    def has_all_prefixes(word):
        """Check if all prefixes of word exist"""
        for i in range(1, len(word) + 1):
            if not trie.search(word[:i]):
                return False
        return True
    
    for word in words:
        if has_all_prefixes(word):
            if len(word) > len(longest) or (len(word) == len(longest) and word < longest):
                longest = word
    
    return longest


def word_break(s, word_dict):
    """Check if string can be segmented into words from dictionary"""
    trie = Trie()
    for word in word_dict:
        trie.insert(word)
    
    n = len(s)
    dp = [False] * (n + 1)
    dp[0] = True
    
    for i in range(1, n + 1):
        for j in range(i):
            if dp[j] and trie.search(s[j:i]):
                dp[i] = True
                break
    
    return dp[n]


def replace_words(dictionary, sentence):
    """Replace words in sentence with their roots from dictionary"""
    trie = Trie()
    for root in dictionary:
        trie.insert(root)
    
    def find_root(word):
        """Find shortest root for word"""
        node = trie.root
        prefix = []
        
        for char in word:
            if char not in node.children:
                return word
            node = node.children[char]
            prefix.append(char)
            
            if node.is_end_of_word:
                return ''.join(prefix)
        
        return word
    
    words = sentence.split()
    return ' '.join(find_root(word) for word in words)


# Example usage
if __name__ == "__main__":
    print("=== Trie Basic Operations ===")
    trie = Trie()
    
    # Insert words
    words = ["apple", "app", "apricot", "banana", "band", "bandana"]
    for word in words:
        trie.insert(word)
    
    print(f"Words in trie: {trie.get_all_words()}")
    print(f"Total words: {len(trie)}")
    
    # Search
    print(f"\nSearch 'app': {trie.search('app')}")
    print(f"Search 'appl': {trie.search('appl')}")
    print(f"Search 'application': {trie.search('application')}")
    
    # Starts with
    print(f"\nStarts with 'app': {trie.starts_with('app')}")
    print(f"Starts with 'ban': {trie.starts_with('ban')}")
    print(f"Starts with 'cat': {trie.starts_with('cat')}")
    
    # Autocomplete
    print(f"\nAutocomplete 'app': {trie.autocomplete('app')}")
    print(f"Autocomplete 'ban': {trie.autocomplete('ban')}")
    
    # Count with prefix
    print(f"\nWords starting with 'app': {trie.count_words_with_prefix('app')}")
    print(f"Words starting with 'ban': {trie.count_words_with_prefix('ban')}")
    
    # Longest common prefix
    trie2 = Trie()
    for word in ["flower", "flow", "flight"]:
        trie2.insert(word)
    print(f"\nLongest common prefix of {trie2.get_all_words()}: '{trie2.longest_common_prefix()}'")
    
    # Delete
    print(f"\nDeleting 'app'...")
    trie.delete("app")
    print(f"Search 'app' after deletion: {trie.search('app')}")
    print(f"Search 'apple' after deletion: {trie.search('apple')}")
    print(f"Words in trie: {trie.get_all_words()}")
    
    print("\n=== Wildcard Trie ===")
    wildcard_trie = TrieWithWildcard()
    for word in ["bad", "dad", "mad"]:
        wildcard_trie.insert(word)
    
    print(f"Search 'pad': {wildcard_trie.search('pad')}")
    print(f"Search 'bad': {wildcard_trie.search('bad')}")
    print(f"Search '.ad': {wildcard_trie.search('.ad')}")
    print(f"Search 'b..': {wildcard_trie.search('b..')}")
    
    print("\n=== Word Break ===")
    s = "leetcode"
    word_dict = ["leet", "code"]
    print(f"Can '{s}' be segmented using {word_dict}? {word_break(s, word_dict)}")
    
    s = "applepenapple"
    word_dict = ["apple", "pen"]
    print(f"Can '{s}' be segmented using {word_dict}? {word_break(s, word_dict)}")
    
    print("\n=== Replace Words ===")
    dictionary = ["cat", "bat", "rat"]
    sentence = "the cattle was rattled by the battery"
    print(f"Original: {sentence}")
    print(f"Replaced: {replace_words(dictionary, sentence)}")
    
    print("\n=== Longest Word with All Prefixes ===")
    words = ["w", "wo", "wor", "worl", "world"]
    print(f"Words: {words}")
    print(f"Longest with all prefixes: {find_longest_word_with_all_prefixes(words)}")
