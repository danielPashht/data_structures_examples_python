"""
Binary Search Tree (BST) Data Structure
========================================
A tree data structure where each node has at most two children,
and for each node: left subtree < node < right subtree

Time Complexity (Average):
- Search: O(log n)
- Insert: O(log n)
- Delete: O(log n)

Time Complexity (Worst - unbalanced):
- Search: O(n)
- Insert: O(n)
- Delete: O(n)

Use Cases:
- Sorted data storage
- Database indexing
- Implementing maps and sets
- Expression parsing
- Range queries
"""


class TreeNode:
    """Node for Binary Search Tree"""
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None


class BinarySearchTree:
    """Binary Search Tree implementation"""
    
    def __init__(self):
        self.root = None
        self.size = 0
    
    def insert(self, value):
        """Insert a value into the BST"""
        if self.root is None:
            self.root = TreeNode(value)
            self.size += 1
        else:
            self._insert_recursive(self.root, value)
    
    def _insert_recursive(self, node, value):
        """Helper method to insert recursively"""
        if value < node.value:
            if node.left is None:
                node.left = TreeNode(value)
                self.size += 1
            else:
                self._insert_recursive(node.left, value)
        elif value > node.value:
            if node.right is None:
                node.right = TreeNode(value)
                self.size += 1
            else:
                self._insert_recursive(node.right, value)
        # If value == node.value, don't insert (no duplicates)
    
    def search(self, value):
        """Search for a value in the BST"""
        return self._search_recursive(self.root, value)
    
    def _search_recursive(self, node, value):
        """Helper method to search recursively"""
        if node is None:
            return False
        if value == node.value:
            return True
        elif value < node.value:
            return self._search_recursive(node.left, value)
        else:
            return self._search_recursive(node.right, value)
    
    def delete(self, value):
        """Delete a value from the BST"""
        self.root = self._delete_recursive(self.root, value)
    
    def _delete_recursive(self, node, value):
        """Helper method to delete recursively"""
        if node is None:
            return None
        
        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node to be deleted found
            self.size -= 1
            
            # Case 1: No children
            if node.left is None and node.right is None:
                return None
            
            # Case 2: One child
            if node.left is None:
                return node.right
            if node.right is None:
                return node.left
            
            # Case 3: Two children
            # Find inorder successor (smallest in right subtree)
            successor = self._find_min(node.right)
            node.value = successor.value
            node.right = self._delete_recursive(node.right, successor.value)
            self.size += 1  # Compensate for decrement above
        
        return node
    
    def _find_min(self, node):
        """Find minimum value node in subtree"""
        current = node
        while current.left:
            current = current.left
        return current
    
    def find_min(self):
        """Find minimum value in tree"""
        if self.root is None:
            return None
        return self._find_min(self.root).value
    
    def find_max(self):
        """Find maximum value in tree"""
        if self.root is None:
            return None
        current = self.root
        while current.right:
            current = current.right
        return current.value
    
    def height(self):
        """Get height of tree"""
        return self._height_recursive(self.root)
    
    def _height_recursive(self, node):
        """Helper method to calculate height"""
        if node is None:
            return -1
        return 1 + max(self._height_recursive(node.left), 
                      self._height_recursive(node.right))
    
    def inorder_traversal(self):
        """Inorder traversal (Left, Root, Right) - gives sorted order"""
        result = []
        self._inorder_recursive(self.root, result)
        return result
    
    def _inorder_recursive(self, node, result):
        """Helper for inorder traversal"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)
    
    def preorder_traversal(self):
        """Preorder traversal (Root, Left, Right)"""
        result = []
        self._preorder_recursive(self.root, result)
        return result
    
    def _preorder_recursive(self, node, result):
        """Helper for preorder traversal"""
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)
    
    def postorder_traversal(self):
        """Postorder traversal (Left, Right, Root)"""
        result = []
        self._postorder_recursive(self.root, result)
        return result
    
    def _postorder_recursive(self, node, result):
        """Helper for postorder traversal"""
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)
    
    def level_order_traversal(self):
        """Level order traversal (BFS)"""
        if self.root is None:
            return []
        
        result = []
        queue = [self.root]
        
        while queue:
            node = queue.pop(0)
            result.append(node.value)
            
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        
        return result
    
    def is_valid_bst(self):
        """Check if tree is a valid BST"""
        return self._is_valid_bst_recursive(self.root, float('-inf'), float('inf'))
    
    def _is_valid_bst_recursive(self, node, min_val, max_val):
        """Helper to validate BST property"""
        if node is None:
            return True
        
        if node.value <= min_val or node.value >= max_val:
            return False
        
        return (self._is_valid_bst_recursive(node.left, min_val, node.value) and
                self._is_valid_bst_recursive(node.right, node.value, max_val))
    
    def range_query(self, low, high):
        """Find all values in range [low, high]"""
        result = []
        self._range_query_recursive(self.root, low, high, result)
        return result
    
    def _range_query_recursive(self, node, low, high, result):
        """Helper for range query"""
        if node is None:
            return
        
        if low < node.value:
            self._range_query_recursive(node.left, low, high, result)
        
        if low <= node.value <= high:
            result.append(node.value)
        
        if node.value < high:
            self._range_query_recursive(node.right, low, high, result)
    
    def __len__(self):
        return self.size
    
    def __str__(self):
        """String representation using inorder traversal"""
        return f"BST({self.inorder_traversal()})"


# Practical applications
def find_kth_smallest(bst, k):
    """Find kth smallest element in BST"""
    inorder = bst.inorder_traversal()
    if k < 1 or k > len(inorder):
        return None
    return inorder[k - 1]


def find_common_ancestor(bst, v1, v2):
    """Find lowest common ancestor of two values"""
    node = bst.root
    
    while node:
        if v1 < node.value and v2 < node.value:
            node = node.left
        elif v1 > node.value and v2 > node.value:
            node = node.right
        else:
            return node.value
    
    return None


def is_balanced(node):
    """Check if BST is height-balanced"""
    def check_height(n):
        if n is None:
            return 0
        
        left_height = check_height(n.left)
        if left_height == -1:
            return -1
        
        right_height = check_height(n.right)
        if right_height == -1:
            return -1
        
        if abs(left_height - right_height) > 1:
            return -1
        
        return max(left_height, right_height) + 1
    
    return check_height(node) != -1


# Example usage
if __name__ == "__main__":
    print("=== Binary Search Tree ===")
    bst = BinarySearchTree()
    
    # Insert elements
    values = [50, 30, 70, 20, 40, 60, 80]
    for val in values:
        bst.insert(val)
    
    print(f"BST: {bst}")
    print(f"Size: {len(bst)}")
    print(f"Height: {bst.height()}")
    
    # Search
    print(f"\nSearch 40: {bst.search(40)}")
    print(f"Search 25: {bst.search(25)}")
    
    # Min and Max
    print(f"\nMin value: {bst.find_min()}")
    print(f"Max value: {bst.find_max()}")
    
    # Traversals
    print(f"\nInorder (sorted): {bst.inorder_traversal()}")
    print(f"Preorder: {bst.preorder_traversal()}")
    print(f"Postorder: {bst.postorder_traversal()}")
    print(f"Level order: {bst.level_order_traversal()}")
    
    # Range query
    print(f"\nRange [30, 60]: {bst.range_query(30, 60)}")
    
    # Kth smallest
    print(f"\n3rd smallest: {find_kth_smallest(bst, 3)}")
    
    # Common ancestor
    print(f"\nLowest common ancestor of 20 and 40: {find_common_ancestor(bst, 20, 40)}")
    
    # Validation
    print(f"\nIs valid BST: {bst.is_valid_bst()}")
    print(f"Is balanced: {is_balanced(bst.root)}")
    
    # Delete
    print(f"\nDeleting 30...")
    bst.delete(30)
    print(f"BST after deletion: {bst}")
    
    print(f"\nDeleting 50...")
    bst.delete(50)
    print(f"BST after deletion: {bst}")
