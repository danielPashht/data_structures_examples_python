# Data Structures Examples for Python Backend Developers

A comprehensive collection of data structure implementations in Python, designed for backend developers. Each file contains clear, well-documented examples with practical use cases and complexity analysis.

## 📚 Contents

### Linear Data Structures
- **[linked_list.py](linked_list.py)** - Singly and doubly linked lists with common operations
- **[stack_queue.py](stack_queue.py)** - Stack, Queue, Circular Queue, Priority Queue, and Deque implementations

### Hash-Based Structures
- **[hash_table.py](hash_table.py)** - Hash table with chaining and open addressing, plus hash set implementation

### Tree Structures
- **[basic_tree.py](basic_tree.py)** - Basic tree implementation (already in repo)
- **[binary_search_tree.py](binary_search_tree.py)** - Binary Search Tree with traversals and operations
- **[heap.py](heap.py)** - Min/Max heap, heap sort, and priority queue applications
- **[trie.py](trie.py)** - Prefix tree for string operations and autocomplete

### Graph Structures
- **[graph.py](graph.py)** - Graph representations (adjacency list/matrix) with BFS, DFS, Dijkstra, and more

### Advanced Structures
- **[advanced_structures.py](advanced_structures.py)** - Union-Find, LRU Cache, Bloom Filter, and Segment Tree

### Other
- **[game_of_life.py](game_of_life.py)** - Conway's Game of Life implementation (already in repo)

## 🚀 Quick Start

Each file is standalone and can be run directly:

```bash
python linked_list.py
python stack_queue.py
python hash_table.py
# ... and so on
```

## 📖 Overview by Data Structure

### Linked List
**Time Complexity:**
- Access: O(n)
- Search: O(n)
- Insert at head: O(1)
- Delete: O(n)

**Use Cases:** Dynamic memory allocation, implementing stacks/queues, undo functionality

```python
from linked_list import SinglyLinkedList

ll = SinglyLinkedList()
ll.append(1)
ll.append(2)
ll.prepend(0)
print(ll)  # 0 -> 1 -> 2
```

### Stack & Queue
**Time Complexity:** All operations O(1)

**Use Cases:**
- Stack: Function calls, undo/redo, expression evaluation
- Queue: Task scheduling, BFS, message queues

```python
from stack_queue import Stack, Queue

stack = Stack()
stack.push(1)
print(stack.pop())

queue = Queue()
queue.enqueue('task1')
print(queue.dequeue())
```

### Hash Table
**Time Complexity (Average):** O(1) for insert, search, delete

**Use Cases:** Caching, frequency counting, fast lookups, deduplication

```python
from hash_table import HashTableChaining

ht = HashTableChaining()
ht.put("name", "Alice")
print(ht.get("name"))  # Alice
```

### Binary Search Tree
**Time Complexity (Average):** O(log n) for insert, search, delete

**Use Cases:** Sorted data storage, range queries, database indexing

```python
from binary_search_tree import BinarySearchTree

bst = BinarySearchTree()
bst.insert(5)
bst.insert(3)
bst.insert(7)
print(bst.inorder_traversal())  # [3, 5, 7]
```

### Heap
**Time Complexity:** O(log n) insert/extract, O(1) peek

**Use Cases:** Priority queues, finding k largest/smallest, heap sort, scheduling

```python
from heap import MinHeap

heap = MinHeap()
heap.insert(5)
heap.insert(3)
heap.insert(7)
print(heap.extract_min())  # 3
```

### Trie
**Time Complexity:** O(m) where m is word length

**Use Cases:** Autocomplete, spell checker, IP routing, dictionary

```python
from trie import Trie

trie = Trie()
trie.insert("apple")
trie.insert("app")
print(trie.autocomplete("app"))  # ['app', 'apple']
```

### Graph
**Time Complexity:** Varies by algorithm
- BFS/DFS: O(V + E)
- Dijkstra: O((V + E) log V)

**Use Cases:** Social networks, maps, routing, dependencies

```python
from graph import Graph

g = Graph()
g.add_edge('A', 'B')
g.add_edge('B', 'C')
print(g.bfs('A'))  # ['A', 'B', 'C']
```

### Union-Find
**Time Complexity:** O(α(n)) ≈ O(1) amortized

**Use Cases:** Connected components, cycle detection, Kruskal's MST

```python
from advanced_structures import UnionFind

uf = UnionFind(10)
uf.union(0, 1)
print(uf.connected(0, 1))  # True
```

### LRU Cache
**Time Complexity:** O(1) for get and put

**Use Cases:** Caching, memory management, database query cache

```python
from advanced_structures import LRUCache

cache = LRUCache(2)
cache.put(1, "one")
cache.put(2, "two")
print(cache.get(1))  # "one"
```

### Bloom Filter
**Properties:** No false negatives, possible false positives

**Use Cases:** Membership testing, avoiding expensive lookups, spell checkers

```python
from advanced_structures import BloomFilter

bf = BloomFilter()
bf.add("apple")
print(bf.contains("apple"))  # True
print(bf.contains("banana"))  # Probably False
```

## 🎯 Choosing the Right Data Structure

| Need | Best Choice | Why |
|------|-------------|-----|
| Fast lookups by key | Hash Table | O(1) average time |
| Sorted data with range queries | BST or Heap | O(log n) operations |
| LIFO operations | Stack | O(1) push/pop |
| FIFO operations | Queue | O(1) enqueue/dequeue |
| Top K elements | Heap | Efficient min/max |
| String prefix matching | Trie | O(m) search where m = word length |
| Network/graph problems | Graph | BFS, DFS, shortest path |
| Connected components | Union-Find | Near O(1) operations |
| Recent items with cap | LRU Cache | O(1) access and updates |
| Probabilistic membership | Bloom Filter | Space-efficient |

## 💡 Backend Developer Tips

### When to use each structure in backend development:

1. **Hash Tables** - Most common for:
   - Caching responses
   - Session storage
   - Indexing database results
   - Rate limiting (token buckets)

2. **Queues** - Essential for:
   - Background job processing
   - Message queues (RabbitMQ, Kafka)
   - Request buffering
   - Event-driven architectures

3. **Tries** - Perfect for:
   - API route matching
   - Autocomplete endpoints
   - IP routing tables
   - URL shortener services

4. **Graphs** - Used in:
   - Social network features
   - Recommendation engines
   - Dependency resolution
   - Service mesh routing

5. **LRU Cache** - Implement for:
   - Database query caching
   - API response caching
   - Session management
   - Resource pooling

6. **Union-Find** - Helpful for:
   - User group management
   - Network topology
   - Detecting duplicate accounts
   - Clustering algorithms

## 🔧 Common Patterns

### Frequency Counter Pattern
```python
from hash_table import HashTableChaining

def count_frequencies(items):
    freq = HashTableChaining()
    for item in items:
        if freq.contains(item):
            freq.put(item, freq.get(item) + 1)
        else:
            freq.put(item, 1)
    return freq
```

### Two Pointer Pattern (Linked List)
```python
def find_middle(linked_list):
    slow = fast = linked_list.head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow
```

### Sliding Window (with Deque)
```python
from collections import deque

def max_in_sliding_window(arr, k):
    dq = deque()
    result = []
    for i, num in enumerate(arr):
        while dq and arr[dq[-1]] < num:
            dq.pop()
        dq.append(i)
        if dq[0] <= i - k:
            dq.popleft()
        if i >= k - 1:
            result.append(arr[dq[0]])
    return result
```

## 📊 Space-Time Tradeoffs

| Data Structure | Time (Search) | Time (Insert) | Space | Notes |
|----------------|---------------|---------------|-------|-------|
| Array | O(n) | O(n) | O(n) | Simple, cache-friendly |
| Hash Table | O(1) avg | O(1) avg | O(n) | Fast but no ordering |
| BST | O(log n) | O(log n) | O(n) | Ordered, can be unbalanced |
| Heap | O(n) | O(log n) | O(n) | Fast min/max |
| Trie | O(m) | O(m) | O(ALPHABET*m*n) | Great for prefixes |
| Graph (Adj List) | O(V) | O(1) | O(V+E) | Sparse graphs |
| Bloom Filter | O(k) | O(k) | O(m) | Probabilistic, space-efficient |

## 🧪 Testing

Each implementation includes example usage at the bottom. Run the files to see demonstrations:

```bash
# Test all structures
python linked_list.py
python stack_queue.py
python hash_table.py
python binary_search_tree.py
python heap.py
python trie.py
python graph.py
python advanced_structures.py
```

## 📝 Code Style

All implementations follow:
- Clear, descriptive variable names
- Comprehensive docstrings
- Type hints where appropriate
- Complexity analysis in comments
- Practical examples and use cases

## 🎓 Learning Path

Recommended order for learning:

1. **Start with basics**: Stack, Queue, Linked List
2. **Move to search**: Hash Table, BST
3. **Understand recursion**: Tree traversals, DFS
4. **Learn graph algorithms**: BFS, DFS, Dijkstra
5. **Master advanced**: Trie, Heap, Union-Find
6. **Optimize**: LRU Cache, Bloom Filter, Segment Tree

## 🔗 Related Topics

- **Algorithms**: Sorting, searching, dynamic programming
- **System Design**: Distributed caching, load balancing
- **Database Internals**: B-trees, LSM trees, indexes
- **Concurrency**: Thread-safe data structures

## 📚 References

- [Introduction to Algorithms (CLRS)](https://mitpress.mit.edu/books/introduction-algorithms-third-edition)
- [Python Data Structures Documentation](https://docs.python.org/3/tutorial/datastructures.html)
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)

## 🤝 Contributing

These implementations are designed for learning. Feel free to:
- Add more examples
- Improve documentation
- Optimize implementations
- Add unit tests

## 📄 License

Free to use for learning and development purposes.

---

**Happy coding!** 🚀

For questions or suggestions, feel free to open an issue or contribute to the repository.
