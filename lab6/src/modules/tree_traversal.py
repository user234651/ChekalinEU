def inorder_rec(node, result=None):
    """
    Рекурсивный in-order обход (лево-корень-право).
    Сложность: O(n)
    """
    if result is None:
        result = []

    if node:
        inorder_rec(node.left, result)
        result.append(node.value)
        inorder_rec(node.right, result)

    return result

def preorder_rec(node, result=None):
    """
    Рекурсивный pre-order обход (корень-лево-право).
    Сложность: O(n)
    """
    if result is None:
        result = []

    if node:
        result.append(node.value)
        preorder_rec(node.left, result)
        preorder_rec(node.right, result)

    return result

def postorder_rec(node, result=None):
    """
    Рекурсивный post-order обход (лево-право-корень).
    Сложность: O(n)
    """
    if result is None:
        result = []

    if node:
        postorder_rec(node.left, result)
        postorder_rec(node.right, result)
        result.append(node.value)

    return result

def inorder_iter(root):
    """
    Итеративный in-order (стек).
    Сложность: O(n)
    """
    result = []
    stack = []
    current = root

    while current or stack:
        while current:
            stack.append(current)
            current = current.left

        current = stack.pop()
        result.append(current.value)
        current = current.right

    return result

def level_order(root):
    """
    Обход по уровням (BFS).
    Сложность: O(n)
    """
    if not root:
        return []

    result = []
    queue = [root]

    while queue:
        current = queue.pop(0)
        result.append(current.value)

        if current.left:
            queue.append(current.left)
        if current.right:
            queue.append(current.right)

    return result
