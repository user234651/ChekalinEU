def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0 or n == 1:
        return 1
    return n * factorial(n - 1)

# Complexity: O(n) time.
# Max recursion depth: n (calls along a chain of length n).


def fibonacci_naive(n: int) -> int:
    if n < 0:
        raise ValueError("n must be >= 0")
    if n == 0:
        return 0
    if n == 1:
        return 1
    return fibonacci_naive(n - 1) + fibonacci_naive(n - 2)

# Time complexity: O(phi^n) exponential (~1.618^n).
# Max recursion depth: n (the longest chain is fib(n)->fib(n-1)->...)


def pow_fast(a: float, n: int) -> float:
    if n < 0:
        return 1.0 / pow_fast(a, -n)
    if n == 0:
        return 1.0
    if n == 1:
        return a
    if n % 2 == 0:
        half = pow_fast(a, n // 2)
        return half * half
    else:
        half = pow_fast(a, (n - 1) // 2)
        return a * half * half

# Time complexity: O(log n) multiplications.
# Max recursion depth: O(log n) (depth proportional to number of times n halved).
