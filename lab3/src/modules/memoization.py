from functools import lru_cache
import timeit

_naive_call_count = 0

def fibonacci_naive_counted(n: int) -> int:
    """Наивная фиб с подсчётом рекурсивных вызовов (глобальный счётчик)."""
    global _naive_call_count
    _naive_call_count += 1
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_naive_counted(n - 1) + fibonacci_naive_counted(n - 2)

def reset_naive_counter():
    global _naive_call_count
    _naive_call_count = 0

def get_naive_count() -> int:
    return _naive_call_count

def make_memoized_fib():
    calls = {'count': 0}
    cache = {}

    def fib(n: int) -> int:
        calls['count'] += 1
        if n in cache:
            return cache[n]
        if n == 0:
            cache[0] = 0
            return 0
        if n == 1:
            cache[1] = 1
            return 1
        val = fib(n - 1) + fib(n - 2)
        cache[n] = val
        return val

    def get_count():
        return calls['count']

    def reset():
        calls['count'] = 0
        cache.clear()

    return fib, get_count, reset

# Сравнение времени и числа вызовов для n
def compare_naive_and_memo(n: int, repeat: int = 3):
    import time
    reset_naive_counter()
    t0 = timeit.default_timer()
    res_naive = fibonacci_naive_counted(n)
    t1 = timeit.default_timer()
    time_naive = t1 - t0
    calls_naive = get_naive_count()

    fib_mem, get_count, reset_mem = make_memoized_fib()
    reset_mem()
    t0 = timeit.default_timer()
    res_mem = fib_mem(n)
    t1 = timeit.default_timer()
    time_memo = t1 - t0
    calls_memo = get_count()

    return {
        'n': n,
        'naive': {'value': res_naive, 'time': time_naive, 'calls': calls_naive},
        'memo': {'value': res_mem, 'time': time_memo, 'calls': calls_memo},
    }
