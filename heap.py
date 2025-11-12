"""
Heap Data Structure (Priority Queue)
=====================================
A complete binary tree that satisfies the heap property.
Min Heap: parent ≤ children
Max Heap: parent ≥ children

Time Complexity:
- Insert: O(log n)
- Extract min/max: O(log n)
- Peek min/max: O(1)
- Heapify: O(n)

Use Cases:
- Priority queues
- Heap sort
- Finding k largest/smallest elements
- Median maintenance
- Task scheduling
- Dijkstra's algorithm
"""

import heapq


class MinHeap:
    """Min Heap implementation using array"""
    
    def __init__(self):
        self.heap = []
    
    def parent(self, i):
        """Get parent index"""
        return (i - 1) // 2
    
    def left_child(self, i):
        """Get left child index"""
        return 2 * i + 1
    
    def right_child(self, i):
        """Get right child index"""
        return 2 * i + 2
    
    def insert(self, value):
        """Insert value into heap"""
        self.heap.append(value)
        self._bubble_up(len(self.heap) - 1)
    
    def _bubble_up(self, i):
        """Move element up to maintain heap property"""
        parent = self.parent(i)
        if i > 0 and self.heap[i] < self.heap[parent]:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            self._bubble_up(parent)
    
    def extract_min(self):
        """Remove and return minimum element"""
        if self.is_empty():
            raise IndexError("Heap is empty")
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        min_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bubble_down(0)
        return min_val
    
    def _bubble_down(self, i):
        """Move element down to maintain heap property"""
        min_index = i
        left = self.left_child(i)
        right = self.right_child(i)
        
        if left < len(self.heap) and self.heap[left] < self.heap[min_index]:
            min_index = left
        
        if right < len(self.heap) and self.heap[right] < self.heap[min_index]:
            min_index = right
        
        if min_index != i:
            self.heap[i], self.heap[min_index] = self.heap[min_index], self.heap[i]
            self._bubble_down(min_index)
    
    def peek(self):
        """Return minimum element without removing"""
        if self.is_empty():
            raise IndexError("Heap is empty")
        return self.heap[0]
    
    def is_empty(self):
        """Check if heap is empty"""
        return len(self.heap) == 0
    
    def size(self):
        """Return size of heap"""
        return len(self.heap)
    
    def __str__(self):
        return f"MinHeap({self.heap})"


class MaxHeap:
    """Max Heap implementation using array"""
    
    def __init__(self):
        self.heap = []
    
    def parent(self, i):
        return (i - 1) // 2
    
    def left_child(self, i):
        return 2 * i + 1
    
    def right_child(self, i):
        return 2 * i + 2
    
    def insert(self, value):
        """Insert value into heap"""
        self.heap.append(value)
        self._bubble_up(len(self.heap) - 1)
    
    def _bubble_up(self, i):
        """Move element up to maintain heap property"""
        parent = self.parent(i)
        if i > 0 and self.heap[i] > self.heap[parent]:
            self.heap[i], self.heap[parent] = self.heap[parent], self.heap[i]
            self._bubble_up(parent)
    
    def extract_max(self):
        """Remove and return maximum element"""
        if self.is_empty():
            raise IndexError("Heap is empty")
        
        if len(self.heap) == 1:
            return self.heap.pop()
        
        max_val = self.heap[0]
        self.heap[0] = self.heap.pop()
        self._bubble_down(0)
        return max_val
    
    def _bubble_down(self, i):
        """Move element down to maintain heap property"""
        max_index = i
        left = self.left_child(i)
        right = self.right_child(i)
        
        if left < len(self.heap) and self.heap[left] > self.heap[max_index]:
            max_index = left
        
        if right < len(self.heap) and self.heap[right] > self.heap[max_index]:
            max_index = right
        
        if max_index != i:
            self.heap[i], self.heap[max_index] = self.heap[max_index], self.heap[i]
            self._bubble_down(max_index)
    
    def peek(self):
        """Return maximum element without removing"""
        if self.is_empty():
            raise IndexError("Heap is empty")
        return self.heap[0]
    
    def is_empty(self):
        return len(self.heap) == 0
    
    def size(self):
        return len(self.heap)
    
    def __str__(self):
        return f"MaxHeap({self.heap})"


def heapify(arr):
    """Convert array to min heap in-place"""
    n = len(arr)
    # Start from last non-leaf node
    for i in range(n // 2 - 1, -1, -1):
        _heapify_down(arr, n, i)
    return arr


def _heapify_down(arr, n, i):
    """Helper for heapify"""
    smallest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] < arr[smallest]:
        smallest = left
    
    if right < n and arr[right] < arr[smallest]:
        smallest = right
    
    if smallest != i:
        arr[i], arr[smallest] = arr[smallest], arr[i]
        _heapify_down(arr, n, smallest)


def heap_sort(arr):
    """Sort array using heap sort"""
    n = len(arr)
    result = arr.copy()
    
    # Build max heap
    for i in range(n // 2 - 1, -1, -1):
        _heapify_down_max(result, n, i)
    
    # Extract elements one by one
    for i in range(n - 1, 0, -1):
        result[0], result[i] = result[i], result[0]
        _heapify_down_max(result, i, 0)
    
    return result


def _heapify_down_max(arr, n, i):
    """Helper for max heapify"""
    largest = i
    left = 2 * i + 1
    right = 2 * i + 2
    
    if left < n and arr[left] > arr[largest]:
        largest = left
    
    if right < n and arr[right] > arr[largest]:
        largest = right
    
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        _heapify_down_max(arr, n, largest)


# Practical applications
def find_k_largest(arr, k):
    """Find k largest elements using min heap"""
    if k > len(arr):
        return arr
    
    # Use Python's heapq for efficiency
    return heapq.nlargest(k, arr)


def find_k_smallest(arr, k):
    """Find k smallest elements using max heap"""
    if k > len(arr):
        return arr
    
    return heapq.nsmallest(k, arr)


def merge_k_sorted_lists(lists):
    """Merge k sorted lists using min heap"""
    heap = []
    result = []
    
    # Initialize heap with first element from each list
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))
    
    # Extract min and add next element from same list
    while heap:
        val, list_idx, element_idx = heapq.heappop(heap)
        result.append(val)
        
        if element_idx + 1 < len(lists[list_idx]):
            next_val = lists[list_idx][element_idx + 1]
            heapq.heappush(heap, (next_val, list_idx, element_idx + 1))
    
    return result


class MedianFinder:
    """Find median in a stream of numbers using two heaps"""
    
    def __init__(self):
        self.max_heap = []  # Left half (negated for max heap)
        self.min_heap = []  # Right half
    
    def add_num(self, num):
        """Add number to data structure"""
        # Add to max heap (left half)
        heapq.heappush(self.max_heap, -num)
        
        # Balance: move largest from left to right
        heapq.heappush(self.min_heap, -heapq.heappop(self.max_heap))
        
        # Balance sizes: left should have at most 1 more than right
        if len(self.max_heap) < len(self.min_heap):
            heapq.heappush(self.max_heap, -heapq.heappop(self.min_heap))
    
    def find_median(self):
        """Return median of all numbers added so far"""
        if len(self.max_heap) > len(self.min_heap):
            return -self.max_heap[0]
        return (-self.max_heap[0] + self.min_heap[0]) / 2.0


# Example usage
if __name__ == "__main__":
    print("=== Min Heap ===")
    min_heap = MinHeap()
    
    values = [5, 3, 8, 1, 9, 2]
    for val in values:
        min_heap.insert(val)
    
    print(f"Min Heap: {min_heap}")
    print(f"Peek: {min_heap.peek()}")
    print(f"Extract min: {min_heap.extract_min()}")
    print(f"After extraction: {min_heap}")
    
    print("\n=== Max Heap ===")
    max_heap = MaxHeap()
    
    for val in values:
        max_heap.insert(val)
    
    print(f"Max Heap: {max_heap}")
    print(f"Peek: {max_heap.peek()}")
    print(f"Extract max: {max_heap.extract_max()}")
    print(f"After extraction: {max_heap}")
    
    print("\n=== Heapify ===")
    arr = [9, 5, 6, 2, 3]
    print(f"Original: {arr}")
    heapified = heapify(arr.copy())
    print(f"Heapified: {heapified}")
    
    print("\n=== Heap Sort ===")
    arr = [12, 11, 13, 5, 6, 7]
    print(f"Original: {arr}")
    sorted_arr = heap_sort(arr)
    print(f"Sorted: {sorted_arr}")
    
    print("\n=== K Largest Elements ===")
    arr = [3, 2, 1, 5, 6, 4]
    k = 3
    print(f"Array: {arr}")
    print(f"{k} largest: {find_k_largest(arr, k)}")
    
    print("\n=== K Smallest Elements ===")
    print(f"{k} smallest: {find_k_smallest(arr, k)}")
    
    print("\n=== Merge K Sorted Lists ===")
    lists = [[1, 4, 5], [1, 3, 4], [2, 6]]
    print(f"Lists: {lists}")
    merged = merge_k_sorted_lists(lists)
    print(f"Merged: {merged}")
    
    print("\n=== Median Finder (Stream) ===")
    mf = MedianFinder()
    stream = [1, 2, 3, 4, 5]
    print(f"Stream: {stream}")
    for num in stream:
        mf.add_num(num)
        print(f"After adding {num}, median: {mf.find_median()}")
