"""
Stack and Queue Data Structures
================================

Stack: Last-In-First-Out (LIFO) data structure
Queue: First-In-First-Out (FIFO) data structure

Time Complexity (both):
- Push/Enqueue: O(1)
- Pop/Dequeue: O(1)
- Peek: O(1)
- Search: O(n)

Use Cases:
Stack:
- Function call stack
- Undo/Redo operations
- Expression evaluation
- Backtracking algorithms
- Browser back button

Queue:
- Task scheduling
- Breadth-first search
- Message queues
- Printer queue
- Asynchronous data processing
"""

from collections import deque


class Stack:
    """Stack implementation using Python list"""
    
    def __init__(self):
        self._items = []
    
    def push(self, item):
        """Add item to top of stack"""
        self._items.append(item)
    
    def pop(self):
        """Remove and return top item"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items.pop()
    
    def peek(self):
        """Return top item without removing"""
        if self.is_empty():
            raise IndexError("Stack is empty")
        return self._items[-1]
    
    def is_empty(self):
        """Check if stack is empty"""
        return len(self._items) == 0
    
    def size(self):
        """Return number of items"""
        return len(self._items)
    
    def __str__(self):
        return f"Stack({self._items})"


class Queue:
    """Queue implementation using collections.deque for efficiency"""
    
    def __init__(self):
        self._items = deque()
    
    def enqueue(self, item):
        """Add item to rear of queue"""
        self._items.append(item)
    
    def dequeue(self):
        """Remove and return front item"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items.popleft()
    
    def front(self):
        """Return front item without removing"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items[0]
    
    def is_empty(self):
        """Check if queue is empty"""
        return len(self._items) == 0
    
    def size(self):
        """Return number of items"""
        return len(self._items)
    
    def __str__(self):
        return f"Queue({list(self._items)})"


class CircularQueue:
    """Circular Queue with fixed size"""
    
    def __init__(self, capacity):
        self.capacity = capacity
        self._items = [None] * capacity
        self._front = 0
        self._rear = -1
        self._size = 0
    
    def enqueue(self, item):
        """Add item to queue"""
        if self.is_full():
            raise OverflowError("Queue is full")
        self._rear = (self._rear + 1) % self.capacity
        self._items[self._rear] = item
        self._size += 1
    
    def dequeue(self):
        """Remove and return front item"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        item = self._items[self._front]
        self._items[self._front] = None
        self._front = (self._front + 1) % self.capacity
        self._size -= 1
        return item
    
    def front(self):
        """Return front item"""
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._items[self._front]
    
    def is_empty(self):
        return self._size == 0
    
    def is_full(self):
        return self._size == self.capacity
    
    def size(self):
        return self._size
    
    def __str__(self):
        if self.is_empty():
            return "CircularQueue([])"
        items = []
        idx = self._front
        for _ in range(self._size):
            items.append(self._items[idx])
            idx = (idx + 1) % self.capacity
        return f"CircularQueue({items})"


class PriorityQueue:
    """Priority Queue using min-heap (lower value = higher priority)"""
    
    def __init__(self):
        self._heap = []
    
    def enqueue(self, item, priority):
        """Add item with priority"""
        import heapq
        heapq.heappush(self._heap, (priority, item))
    
    def dequeue(self):
        """Remove and return highest priority item"""
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        import heapq
        return heapq.heappop(self._heap)[1]
    
    def peek(self):
        """Return highest priority item without removing"""
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        return self._heap[0][1]
    
    def is_empty(self):
        return len(self._heap) == 0
    
    def size(self):
        return len(self._heap)
    
    def __str__(self):
        return f"PriorityQueue({[(p, i) for p, i in self._heap]})"


class Deque:
    """Double-ended Queue (Deque) - can add/remove from both ends"""
    
    def __init__(self):
        self._items = deque()
    
    def add_front(self, item):
        """Add item to front"""
        self._items.appendleft(item)
    
    def add_rear(self, item):
        """Add item to rear"""
        self._items.append(item)
    
    def remove_front(self):
        """Remove and return front item"""
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self._items.popleft()
    
    def remove_rear(self):
        """Remove and return rear item"""
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self._items.pop()
    
    def peek_front(self):
        """Return front item"""
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self._items[0]
    
    def peek_rear(self):
        """Return rear item"""
        if self.is_empty():
            raise IndexError("Deque is empty")
        return self._items[-1]
    
    def is_empty(self):
        return len(self._items) == 0
    
    def size(self):
        return len(self._items)
    
    def __str__(self):
        return f"Deque({list(self._items)})"


# Practical applications
def is_balanced_parentheses(expression):
    """Check if parentheses are balanced using stack"""
    stack = Stack()
    pairs = {'(': ')', '[': ']', '{': '}'}
    
    for char in expression:
        if char in pairs:
            stack.push(char)
        elif char in pairs.values():
            if stack.is_empty() or pairs[stack.pop()] != char:
                return False
    
    return stack.is_empty()


def evaluate_postfix(expression):
    """Evaluate postfix expression using stack"""
    stack = Stack()
    
    for token in expression.split():
        if token.isdigit():
            stack.push(int(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.push(a + b)
            elif token == '-':
                stack.push(a - b)
            elif token == '*':
                stack.push(a * b)
            elif token == '/':
                stack.push(a // b)
    
    return stack.pop()


def reverse_string_with_stack(text):
    """Reverse string using stack"""
    stack = Stack()
    for char in text:
        stack.push(char)
    
    result = []
    while not stack.is_empty():
        result.append(stack.pop())
    
    return ''.join(result)


# Example usage
if __name__ == "__main__":
    print("=== Stack ===")
    stack = Stack()
    stack.push(1)
    stack.push(2)
    stack.push(3)
    print(f"Stack: {stack}")
    print(f"Pop: {stack.pop()}")
    print(f"Peek: {stack.peek()}")
    print(f"Size: {stack.size()}")
    
    print("\n=== Balanced Parentheses ===")
    print(f"{{[()]}}: {is_balanced_parentheses('{[()]}')}") 
    print(f"{{[(]]}}: {is_balanced_parentheses('{[(]]}')}") 
    
    print("\n=== Postfix Evaluation ===")
    print(f"'3 4 + 2 *' = {evaluate_postfix('3 4 + 2 *')}")  # (3+4)*2 = 14
    
    print("\n=== String Reversal ===")
    print(f"Reverse 'hello': {reverse_string_with_stack('hello')}")
    
    print("\n=== Queue ===")
    queue = Queue()
    queue.enqueue(10)
    queue.enqueue(20)
    queue.enqueue(30)
    print(f"Queue: {queue}")
    print(f"Dequeue: {queue.dequeue()}")
    print(f"Front: {queue.front()}")
    print(f"Size: {queue.size()}")
    
    print("\n=== Circular Queue ===")
    cq = CircularQueue(3)
    cq.enqueue('A')
    cq.enqueue('B')
    cq.enqueue('C')
    print(f"Circular Queue: {cq}")
    print(f"Dequeue: {cq.dequeue()}")
    cq.enqueue('D')
    print(f"After enqueue 'D': {cq}")
    
    print("\n=== Priority Queue ===")
    pq = PriorityQueue()
    pq.enqueue("Low priority task", 3)
    pq.enqueue("High priority task", 1)
    pq.enqueue("Medium priority task", 2)
    print(f"Priority Queue: {pq}")
    print(f"Dequeue (highest priority): {pq.dequeue()}")
    print(f"Dequeue: {pq.dequeue()}")
    
    print("\n=== Deque ===")
    dq = Deque()
    dq.add_rear(1)
    dq.add_rear(2)
    dq.add_front(0)
    print(f"Deque: {dq}")
    print(f"Remove front: {dq.remove_front()}")
    print(f"Remove rear: {dq.remove_rear()}")
    print(f"Deque: {dq}")
