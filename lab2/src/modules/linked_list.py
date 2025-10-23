class Node:

    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    
    def __init__(self):
        self.head = None
        self.tail = None
    
    def insert_at_start(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
        # Общая сложность: O(1)
    
    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        # Общая сложность: O(1)
    
    def delete_from_start(self):
        if self.head is None:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return data
        # Общая сложность: O(1)
    
    def traversal(self):
        current = self.head
        elements = []
        while current:
            elements.append(current.data)
            current = current.next
        return elements
        # Общая сложность: O(n)
    
    def is_empty(self):
        return self.head is None
        # Общая сложность: O(1)