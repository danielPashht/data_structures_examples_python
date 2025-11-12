"""
Advanced Data Structures
=========================
Collection of specialized data structures for specific use cases.
"""

from collections import OrderedDict
import hashlib


class UnionFind:
    """
    Union-Find (Disjoint Set Union) Data Structure
    
    Time Complexity (with path compression and union by rank):
    - Find: O(α(n)) ≈ O(1) amortized
    - Union: O(α(n)) ≈ O(1) amortized
    where α is the inverse Ackermann function
    
    Use Cases:
    - Kruskal's MST algorithm
    - Detecting cycles in undirected graphs
    - Connected components
    - Network connectivity
    - Image processing (connected regions)
    """
    
    def __init__(self, n):
        """Initialize n disjoint sets"""
        self.parent = list(range(n))
        self.rank = [0] * n
        self.count = n  # Number of disjoint sets
    
    def find(self, x):
        """Find root of element x with path compression"""
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # Path compression
        return self.parent[x]
    
    def union(self, x, y):
        """Unite sets containing x and y using union by rank"""
        root_x = self.find(x)
        root_y = self.find(y)
        
        if root_x == root_y:
            return False  # Already in same set
        
        # Union by rank
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_y] = root_x
            self.rank[root_x] += 1
        
        self.count -= 1
        return True
    
    def connected(self, x, y):
        """Check if x and y are in the same set"""
        return self.find(x) == self.find(y)
    
    def get_count(self):
        """Get number of disjoint sets"""
        return self.count


class LRUCache:
    """
    Least Recently Used (LRU) Cache
    
    Time Complexity:
    - Get: O(1)
    - Put: O(1)
    
    Space Complexity: O(capacity)
    
    Use Cases:
    - Web browser cache
    - Database query caching
    - CDN caching
    - Memory management
    """
    
    def __init__(self, capacity):
        """Initialize LRU cache with given capacity"""
        self.capacity = capacity
        self.cache = OrderedDict()
    
    def get(self, key):
        """Get value for key, return -1 if not found"""
        if key not in self.cache:
            return -1
        
        # Move to end to mark as recently used
        self.cache.move_to_end(key)
        return self.cache[key]
    
    def put(self, key, value):
        """Put key-value pair into cache"""
        if key in self.cache:
            # Update and move to end
            self.cache.move_to_end(key)
        
        self.cache[key] = value
        
        # Remove least recently used if over capacity
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
    
    def __str__(self):
        return f"LRUCache({dict(self.cache)})"


class LRUCacheManual:
    """
    LRU Cache implemented manually with doubly linked list and hash map
    More educational version showing the actual implementation
    """
    
    class Node:
        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.prev = None
            self.next = None
    
    def __init__(self, capacity):
        self.capacity = capacity
        self.cache = {}  # key -> Node
        
        # Dummy head and tail
        self.head = self.Node(0, 0)
        self.tail = self.Node(0, 0)
        self.head.next = self.tail
        self.tail.prev = self.head
    
    def _remove(self, node):
        """Remove node from linked list"""
        node.prev.next = node.next
        node.next.prev = node.prev
    
    def _add_to_head(self, node):
        """Add node right after head"""
        node.next = self.head.next
        node.prev = self.head
        self.head.next.prev = node
        self.head.next = node
    
    def get(self, key):
        """Get value for key"""
        if key not in self.cache:
            return -1
        
        node = self.cache[key]
        self._remove(node)
        self._add_to_head(node)
        return node.value
    
    def put(self, key, value):
        """Put key-value pair"""
        if key in self.cache:
            self._remove(self.cache[key])
        
        node = self.Node(key, value)
        self.cache[key] = node
        self._add_to_head(node)
        
        if len(self.cache) > self.capacity:
            # Remove LRU (node before tail)
            lru = self.tail.prev
            self._remove(lru)
            del self.cache[lru.key]


class BloomFilter:
    """
    Bloom Filter - Probabilistic data structure
    
    Properties:
    - Can have false positives (says element exists when it doesn't)
    - Cannot have false negatives (if it says no, it's definitely no)
    - Space efficient
    
    Time Complexity:
    - Add: O(k) where k is number of hash functions
    - Contains: O(k)
    
    Use Cases:
    - Checking if username exists (before DB query)
    - Spell checkers
    - Network routers
    - Avoiding expensive lookups
    - Cache filtering
    """
    
    def __init__(self, size=1000, hash_count=3):
        """Initialize bloom filter"""
        self.size = size
        self.hash_count = hash_count
        self.bit_array = [False] * size
    
    def _hash(self, item, seed):
        """Generate hash value for item with seed"""
        h = hashlib.md5((str(item) + str(seed)).encode())
        return int(h.hexdigest(), 16) % self.size
    
    def add(self, item):
        """Add item to bloom filter"""
        for i in range(self.hash_count):
            index = self._hash(item, i)
            self.bit_array[index] = True
    
    def contains(self, item):
        """Check if item might be in set"""
        for i in range(self.hash_count):
            index = self._hash(item, i)
            if not self.bit_array[index]:
                return False
        return True
    
    def __contains__(self, item):
        return self.contains(item)


class SegmentTree:
    """
    Segment Tree for range queries
    
    Time Complexity:
    - Build: O(n)
    - Query: O(log n)
    - Update: O(log n)
    
    Use Cases:
    - Range sum/min/max queries
    - Range updates
    - Computational geometry
    """
    
    def __init__(self, arr):
        """Build segment tree from array"""
        self.n = len(arr)
        self.tree = [0] * (4 * self.n)
        if arr:
            self._build(arr, 0, 0, self.n - 1)
    
    def _build(self, arr, node, start, end):
        """Build tree recursively"""
        if start == end:
            self.tree[node] = arr[start]
            return
        
        mid = (start + end) // 2
        self._build(arr, 2 * node + 1, start, mid)
        self._build(arr, 2 * node + 2, mid + 1, end)
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]
    
    def query(self, left, right):
        """Query sum in range [left, right]"""
        return self._query(0, 0, self.n - 1, left, right)
    
    def _query(self, node, start, end, left, right):
        """Query helper"""
        if right < start or left > end:
            return 0
        
        if left <= start and end <= right:
            return self.tree[node]
        
        mid = (start + end) // 2
        left_sum = self._query(2 * node + 1, start, mid, left, right)
        right_sum = self._query(2 * node + 2, mid + 1, end, left, right)
        return left_sum + right_sum
    
    def update(self, index, value):
        """Update value at index"""
        self._update(0, 0, self.n - 1, index, value)
    
    def _update(self, node, start, end, index, value):
        """Update helper"""
        if start == end:
            self.tree[node] = value
            return
        
        mid = (start + end) // 2
        if index <= mid:
            self._update(2 * node + 1, start, mid, index, value)
        else:
            self._update(2 * node + 2, mid + 1, end, index, value)
        
        self.tree[node] = self.tree[2 * node + 1] + self.tree[2 * node + 2]


# Example usage
if __name__ == "__main__":
    print("=== Union-Find ===")
    uf = UnionFind(10)
    
    # Connect some elements
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(3, 4)
    uf.union(5, 6)
    
    print(f"0 and 2 connected: {uf.connected(0, 2)}")
    print(f"0 and 3 connected: {uf.connected(0, 3)}")
    print(f"Number of disjoint sets: {uf.get_count()}")
    
    uf.union(2, 3)
    print(f"After union(2, 3), 0 and 4 connected: {uf.connected(0, 4)}")
    print(f"Number of disjoint sets: {uf.get_count()}")
    
    print("\n=== LRU Cache ===")
    cache = LRUCache(3)
    
    cache.put(1, "one")
    cache.put(2, "two")
    cache.put(3, "three")
    print(f"Cache: {cache}")
    
    print(f"Get 1: {cache.get(1)}")
    print(f"Cache after get(1): {cache}")
    
    cache.put(4, "four")  # This will evict key 2
    print(f"Cache after put(4, 'four'): {cache}")
    print(f"Get 2: {cache.get(2)}")  # Should return -1
    
    print("\n=== LRU Cache (Manual Implementation) ===")
    cache2 = LRUCacheManual(2)
    cache2.put(1, 1)
    cache2.put(2, 2)
    print(f"Get 1: {cache2.get(1)}")
    cache2.put(3, 3)  # Evicts key 2
    print(f"Get 2 (should be -1): {cache2.get(2)}")
    cache2.put(4, 4)  # Evicts key 1
    print(f"Get 1 (should be -1): {cache2.get(1)}")
    print(f"Get 3: {cache2.get(3)}")
    print(f"Get 4: {cache2.get(4)}")
    
    print("\n=== Bloom Filter ===")
    bf = BloomFilter(size=100, hash_count=3)
    
    # Add some elements
    words = ["apple", "banana", "cherry"]
    for word in words:
        bf.add(word)
    
    # Check membership
    print(f"'apple' in filter: {bf.contains('apple')}")
    print(f"'banana' in filter: {bf.contains('banana')}")
    print(f"'grape' in filter: {bf.contains('grape')}")  # Definitely not
    print(f"'orange' in filter: {bf.contains('orange')}")  # Might be false positive
    
    print("\n=== Segment Tree ===")
    arr = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(arr)
    
    print(f"Array: {arr}")
    print(f"Sum of range [1, 3]: {st.query(1, 3)}")  # 3 + 5 + 7 = 15
    print(f"Sum of range [0, 5]: {st.query(0, 5)}")  # 1 + 3 + 5 + 7 + 9 + 11 = 36
    
    st.update(2, 10)  # Change arr[2] from 5 to 10
    print(f"\nAfter updating index 2 to 10:")
    print(f"Sum of range [1, 3]: {st.query(1, 3)}")  # 3 + 10 + 7 = 20
    print(f"Sum of range [0, 5]: {st.query(0, 5)}")  # 1 + 3 + 10 + 7 + 9 + 11 = 41
