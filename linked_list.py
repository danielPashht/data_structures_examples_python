"""
Linked List Data Structure
===========================
A linear data structure where elements are stored in nodes, each pointing to the next node.

Time Complexity:
- Access: O(n)
- Search: O(n)
- Insert at head: O(1)
- Insert at tail: O(n) for singly linked, O(1) for doubly linked with tail pointer
- Delete: O(n)

Use Cases:
- Dynamic memory allocation
- Implementing stacks and queues
- Undo functionality
- Browser history
"""


class Node:
    """Node for singly linked list"""
    def __init__(self, data):
        self.data = data
        self.next = None


class SinglyLinkedList:
    """Singly Linked List implementation"""
    
    def __init__(self):
        self.head = None
        self.size = 0
    
    def is_empty(self):
        """Check if list is empty"""
        return self.head is None
    
    def append(self, data):
        """Add element at the end"""
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1
    
    def prepend(self, data):
        """Add element at the beginning"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
    
    def insert_after(self, prev_data, data):
        """Insert element after a specific node"""
        current = self.head
        while current and current.data != prev_data:
            current = current.next
        
        if current is None:
            raise ValueError(f"Node with data {prev_data} not found")
        
        new_node = Node(data)
        new_node.next = current.next
        current.next = new_node
        self.size += 1
    
    def delete(self, data):
        """Delete first occurrence of element"""
        if self.is_empty():
            raise ValueError("List is empty")
        
        # If head needs to be deleted
        if self.head.data == data:
            self.head = self.head.next
            self.size -= 1
            return
        
        current = self.head
        while current.next and current.next.data != data:
            current = current.next
        
        if current.next is None:
            raise ValueError(f"Node with data {data} not found")
        
        current.next = current.next.next
        self.size -= 1
    
    def search(self, data):
        """Search for an element"""
        current = self.head
        position = 0
        while current:
            if current.data == data:
                return position
            current = current.next
            position += 1
        return -1
    
    def reverse(self):
        """Reverse the linked list in-place"""
        prev = None
        current = self.head
        while current:
            next_node = current.next
            current.next = prev
            prev = current
            current = next_node
        self.head = prev
    
    def get_middle(self):
        """Get middle element using slow and fast pointer"""
        if self.is_empty():
            return None
        
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow.data
    
    def has_cycle(self):
        """Detect cycle using Floyd's algorithm"""
        if self.is_empty():
            return False
        
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                return True
        return False
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        if self.is_empty():
            return "[]"
        
        result = []
        current = self.head
        while current:
            result.append(str(current.data))
            current = current.next
        return " -> ".join(result)


class DoublyNode:
    """Node for doubly linked list"""
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None


class DoublyLinkedList:
    """Doubly Linked List implementation"""
    
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0
    
    def is_empty(self):
        return self.head is None
    
    def append(self, data):
        """Add element at the end - O(1)"""
        new_node = DoublyNode(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node
        self.size += 1
    
    def prepend(self, data):
        """Add element at the beginning"""
        new_node = DoublyNode(data)
        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        self.size += 1
    
    def delete(self, data):
        """Delete first occurrence of element"""
        if self.is_empty():
            raise ValueError("List is empty")
        
        current = self.head
        while current and current.data != data:
            current = current.next
        
        if current is None:
            raise ValueError(f"Node with data {data} not found")
        
        if current.prev:
            current.prev.next = current.next
        else:
            self.head = current.next
        
        if current.next:
            current.next.prev = current.prev
        else:
            self.tail = current.prev
        
        self.size -= 1
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        if self.is_empty():
            return "[]"
        
        result = []
        current = self.head
        while current:
            result.append(str(current.data))
            current = current.next
        return " <-> ".join(result)


# Example usage and demonstrations
if __name__ == "__main__":
    print("=== Singly Linked List ===")
    sll = SinglyLinkedList()
    
    # Adding elements
    sll.append(1)
    sll.append(2)
    sll.append(3)
    sll.prepend(0)
    print(f"List: {sll}")
    print(f"Size: {len(sll)}")
    
    # Searching
    print(f"Position of 2: {sll.search(2)}")
    
    # Insert after
    sll.insert_after(2, 2.5)
    print(f"After inserting 2.5 after 2: {sll}")
    
    # Get middle
    print(f"Middle element: {sll.get_middle()}")
    
    # Reverse
    sll.reverse()
    print(f"Reversed list: {sll}")
    
    # Delete
    sll.delete(2.5)
    print(f"After deleting 2.5: {sll}")
    
    print("\n=== Doubly Linked List ===")
    dll = DoublyLinkedList()
    
    # Adding elements
    dll.append(10)
    dll.append(20)
    dll.append(30)
    dll.prepend(5)
    print(f"List: {dll}")
    print(f"Size: {len(dll)}")
    
    # Delete
    dll.delete(20)
    print(f"After deleting 20: {dll}")
