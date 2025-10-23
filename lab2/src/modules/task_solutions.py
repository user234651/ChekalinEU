import collections

def is_balanced_brackets(expression):

    stack = []
    brackets = {')': '(', '}': '{', ']': '['}
    
    for char in expression:
        if char in '({[':
            stack.append(char)
        elif char in ')}]':
            if not stack or stack[-1] != brackets[char]:
                return False
            stack.pop()
    
    return len(stack) == 0

def simulate_print_queue(num_tasks, processing_time=1):

    queue = collections.deque(range(1, num_tasks + 1))
    completion_times = []
    current_time = 0
    
    while queue:
        task = queue.popleft()
        current_time += processing_time
        completion_times.append((task, current_time))
        
        # С вероятностью 20% добавляем новую задачу
        import random
        if random.random() < 0.2 and num_tasks < 100:  # Ограничиваем общее количество
            new_task = num_tasks + len(completion_times) + 1
            queue.append(new_task)
    
    return completion_times

def is_palindrome_deque(sequence):

    deq = collections.deque(sequence)
    
    while len(deq) > 1:
        if deq.popleft() != deq.pop():
            return False
    
    return True

def demonstrate_solutions():
    print("=== Проверка сбалансированности скобок ===")
    test_cases = [
        "({[]})",
        "({[}])",
        "((()))",
        "({[)]}",
        ""
    ]
    
    for test in test_cases:
        result = is_balanced_brackets(test)
        print(f"'{test}': {result}")
    
    print("\n=== Симуляция очереди печати ===")
    completion_times = simulate_print_queue(5)
    for task, time in completion_times[:10]:  # Показываем первые 10
        print(f"Задача {task} завершена в время {time}")
    
    print("\n=== Проверка палиндромов ===")
    palindromes = [
        "racecar",
        "level",
        "hello",
        "a",
        "12321",
        "12345"
    ]
    
    for test in palindromes:
        result = is_palindrome_deque(test)
        print(f"'{test}': {result}")