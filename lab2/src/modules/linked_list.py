class Node:
    """Узел связного списка"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Односвязный список"""
    def __init__(self):
        self.head = None
        self.tail = None
    
    def insert_at_start(self, data):
        """Вставка элемента в начало списка - O(1)"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head = new_node
    
    def insert_at_end(self, data):
        """Вставка элемента в конец списка - O(1) с хвостом"""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
    
    def delete_from_start(self):
        """Удаление элемента из начала списка - O(1)"""
        if self.head is None:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        return data
    
    def traversal(self):
        """Обход всех элементов списка - O(n)"""
        current = self.head
        elements = []
        while current:
            elements.append(current.data)
            current = current.next
        return elements
    
    def is_empty(self):
        """Проверка на пустоту - O(1)"""
        return self.head is None