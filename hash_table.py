"""
Hash Table / Hash Map Data Structure
=====================================
A data structure that maps keys to values using a hash function.

Time Complexity (Average):
- Access: N/A
- Search: O(1)
- Insert: O(1)
- Delete: O(1)

Time Complexity (Worst - many collisions):
- Search: O(n)
- Insert: O(n)
- Delete: O(n)

Use Cases:
- Caching and memoization
- Database indexing
- Symbol tables in compilers
- Counting frequency of elements
- Finding duplicates
- Implementing sets and dictionaries
"""


class HashTableChaining:
    """Hash Table using separate chaining for collision resolution"""
    
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]
    
    def _hash(self, key):
        """Hash function using built-in hash"""
        return hash(key) % self.capacity
    
    def put(self, key, value):
        """Insert or update key-value pair"""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        # Update if key exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                return
        
        # Add new key-value pair
        bucket.append((key, value))
        self.size += 1
        
        # Resize if load factor > 0.7
        if self.size / self.capacity > 0.7:
            self._resize()
    
    def get(self, key):
        """Get value for key"""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for k, v in bucket:
            if k == key:
                return v
        
        raise KeyError(f"Key {key} not found")
    
    def delete(self, key):
        """Delete key-value pair"""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket.pop(i)
                self.size -= 1
                return
        
        raise KeyError(f"Key {key} not found")
    
    def contains(self, key):
        """Check if key exists"""
        try:
            self.get(key)
            return True
        except KeyError:
            return False
    
    def _resize(self):
        """Resize hash table when load factor is high"""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        
        for bucket in old_buckets:
            for key, value in bucket:
                self.put(key, value)
    
    def keys(self):
        """Return all keys"""
        result = []
        for bucket in self.buckets:
            for key, _ in bucket:
                result.append(key)
        return result
    
    def values(self):
        """Return all values"""
        result = []
        for bucket in self.buckets:
            for _, value in bucket:
                result.append(value)
        return result
    
    def items(self):
        """Return all key-value pairs"""
        result = []
        for bucket in self.buckets:
            for key, value in bucket:
                result.append((key, value))
        return result
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        items = ', '.join(f'{k}: {v}' for k, v in self.items())
        return f"{{{items}}}"


class HashTableOpenAddressing:
    """Hash Table using open addressing (linear probing) for collision resolution"""
    
    DELETED = object()  # Sentinel for deleted entries
    
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.keys = [None] * capacity
        self.values = [None] * capacity
    
    def _hash(self, key):
        """Hash function"""
        return hash(key) % self.capacity
    
    def _probe(self, key):
        """Linear probing to find slot"""
        index = self._hash(key)
        original_index = index
        
        while True:
            if self.keys[index] is None or self.keys[index] == self.DELETED:
                return index, False
            if self.keys[index] == key:
                return index, True
            
            index = (index + 1) % self.capacity
            
            # Full table
            if index == original_index:
                raise OverflowError("Hash table is full")
    
    def put(self, key, value):
        """Insert or update key-value pair"""
        if self.size / self.capacity > 0.7:
            self._resize()
        
        index, exists = self._probe(key)
        
        if not exists and self.keys[index] != self.DELETED:
            self.size += 1
        
        self.keys[index] = key
        self.values[index] = value
    
    def get(self, key):
        """Get value for key"""
        index = self._hash(key)
        original_index = index
        
        while self.keys[index] is not None:
            if self.keys[index] != self.DELETED and self.keys[index] == key:
                return self.values[index]
            
            index = (index + 1) % self.capacity
            
            if index == original_index:
                break
        
        raise KeyError(f"Key {key} not found")
    
    def delete(self, key):
        """Delete key-value pair"""
        index = self._hash(key)
        original_index = index
        
        while self.keys[index] is not None:
            if self.keys[index] != self.DELETED and self.keys[index] == key:
                self.keys[index] = self.DELETED
                self.values[index] = None
                self.size -= 1
                return
            
            index = (index + 1) % self.capacity
            
            if index == original_index:
                break
        
        raise KeyError(f"Key {key} not found")
    
    def contains(self, key):
        """Check if key exists"""
        try:
            self.get(key)
            return True
        except KeyError:
            return False
    
    def _resize(self):
        """Resize hash table"""
        old_keys = self.keys
        old_values = self.values
        old_capacity = self.capacity
        
        self.capacity *= 2
        self.keys = [None] * self.capacity
        self.values = [None] * self.capacity
        self.size = 0
        
        for i in range(old_capacity):
            if old_keys[i] is not None and old_keys[i] != self.DELETED:
                self.put(old_keys[i], old_values[i])
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        items = []
        for i in range(self.capacity):
            if self.keys[i] is not None and self.keys[i] != self.DELETED:
                items.append(f'{self.keys[i]}: {self.values[i]}')
        return f"{{{', '.join(items)}}}"


class HashSet:
    """Hash Set implementation - stores unique elements"""
    
    def __init__(self, capacity=10):
        self.capacity = capacity
        self.size = 0
        self.buckets = [[] for _ in range(capacity)]
    
    def _hash(self, key):
        return hash(key) % self.capacity
    
    def add(self, key):
        """Add element to set"""
        if self.contains(key):
            return False
        
        index = self._hash(key)
        self.buckets[index].append(key)
        self.size += 1
        
        if self.size / self.capacity > 0.7:
            self._resize()
        
        return True
    
    def remove(self, key):
        """Remove element from set"""
        index = self._hash(key)
        bucket = self.buckets[index]
        
        if key in bucket:
            bucket.remove(key)
            self.size -= 1
            return True
        return False
    
    def contains(self, key):
        """Check if element exists"""
        index = self._hash(key)
        return key in self.buckets[index]
    
    def _resize(self):
        """Resize hash set"""
        old_buckets = self.buckets
        self.capacity *= 2
        self.buckets = [[] for _ in range(self.capacity)]
        self.size = 0
        
        for bucket in old_buckets:
            for key in bucket:
                self.add(key)
    
    def to_list(self):
        """Convert to list"""
        result = []
        for bucket in self.buckets:
            result.extend(bucket)
        return result
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        return f"{{{', '.join(str(x) for x in self.to_list())}}}"


# Practical applications
def count_frequency(items):
    """Count frequency of items using hash table"""
    freq = HashTableChaining()
    for item in items:
        if freq.contains(item):
            freq.put(item, freq.get(item) + 1)
        else:
            freq.put(item, 1)
    return freq


def find_first_unique(text):
    """Find first unique character in string"""
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1
    
    for char in text:
        if freq[char] == 1:
            return char
    return None


def two_sum(nums, target):
    """Find two numbers that sum to target using hash map"""
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return None


# Example usage
if __name__ == "__main__":
    print("=== Hash Table with Chaining ===")
    ht = HashTableChaining()
    ht.put("name", "Alice")
    ht.put("age", 30)
    ht.put("city", "New York")
    print(f"Hash Table: {ht}")
    print(f"Get 'name': {ht.get('name')}")
    print(f"Contains 'age': {ht.contains('age')}")
    print(f"Keys: {ht.keys()}")
    
    ht.delete("age")
    print(f"After deleting 'age': {ht}")
    
    print("\n=== Hash Table with Open Addressing ===")
    ht2 = HashTableOpenAddressing()
    ht2.put("x", 10)
    ht2.put("y", 20)
    ht2.put("z", 30)
    print(f"Hash Table: {ht2}")
    print(f"Get 'y': {ht2.get('y')}")
    
    print("\n=== Hash Set ===")
    hs = HashSet()
    hs.add(1)
    hs.add(2)
    hs.add(3)
    hs.add(2)  # Duplicate
    print(f"Hash Set: {hs}")
    print(f"Contains 2: {hs.contains(2)}")
    print(f"Size: {len(hs)}")
    
    hs.remove(2)
    print(f"After removing 2: {hs}")
    
    print("\n=== Frequency Counter ===")
    words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
    freq = count_frequency(words)
    print(f"Word frequencies: {freq}")
    
    print("\n=== First Unique Character ===")
    text = "leetcode"
    print(f"First unique in '{text}': {find_first_unique(text)}")
    
    print("\n=== Two Sum Problem ===")
    nums = [2, 7, 11, 15]
    target = 9
    result = two_sum(nums, target)
    print(f"Two sum indices for {target} in {nums}: {result}")
