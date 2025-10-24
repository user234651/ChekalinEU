import timeit
import collections
from .linked_list import LinkedList

def compare_insertion_performance():

    print("Сравнение вставки в начало:")
    print("Кол-во элементов\tlist.insert(0)\tLinkedList.insert_at_start")
    
    sizes = [100, 500, 1000, 2000, 5000]
    list_times = []
    linked_list_times = []
    
    for size in sizes:
        def test_list_insert():
            lst = list(range(size))
            for i in range(100):
                lst.insert(0, i)
        
        list_time = timeit.timeit(test_list_insert, number=10)

        def test_linked_list_insert():
            ll = LinkedList()
            for i in range(size):
                ll.insert_at_start(i)
            for i in range(100):
                ll.insert_at_start(i)
        
        linked_list_time = timeit.timeit(test_linked_list_insert, number=10)
        
        list_times.append(list_time)
        linked_list_times.append(linked_list_time)
        print(f"{size}\t\t\t{list_time:.6f}\t\t{linked_list_time:.6f}")
    
    return sizes, list_times, linked_list_times

def compare_queue_performance():

    print("\nСравнение операций очереди:")
    print("Кол-во операций\t\tlist.pop(0)\tdeque.popleft()")
    
    sizes = [100, 500, 1000, 2000, 5000]
    list_times = []
    deque_times = []
    
    for size in sizes:
        # Тест для list
        def test_list_pop():
            lst = list(range(size))
            for _ in range(100):
                if lst:
                    lst.pop(0)
        
        list_time = timeit.timeit(test_list_pop, number=10)
        
        # Тест для deque
        def test_deque_popleft():
            deq = collections.deque(range(size))
            for _ in range(100):
                if deq:
                    deq.popleft()
        
        deque_time = timeit.timeit(test_deque_popleft, number=10)
        
        list_times.append(list_time)
        deque_times.append(deque_time)
        print(f"{size}\t\t\t{list_time:.6f}\t\t{deque_time:.6f}")
    
    return sizes, list_times, deque_times

def run_performance_analysis():
    
    insertion_results = compare_insertion_performance()
    queue_results = compare_queue_performance()
    
    return insertion_results, queue_results