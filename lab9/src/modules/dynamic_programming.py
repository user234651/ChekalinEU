import sys
from typing import Dict, List, Tuple

class FibSeries:
    """Разные способы вычисления чисел Фибоначчи.

    Временная сложность: указана для каждого подхода.
    """
    @staticmethod
    def naive_recursive(n: int) -> int:
        """
        Наивная рекурсия.
        Время: O(2^n), Память: O(n).
        """
        if n <= 1:
            return n
        return FibSeries.naive_recursive(n - 1) + FibSeries.naive_recursive(n - 2)

    @staticmethod
    def memoized(n: int, memo: Dict[int, int] = None) -> int:
        """
        Рекурсия с кэшем (top-down).
        Время: O(n), Память: O(n).
        """
        if memo is None:
            memo = {}
        if n in memo:
            return memo[n]
        if n <= 1:
            return n
        memo[n] = FibSeries.memoized(n - 1, memo) + FibSeries.memoized(n - 2, memo)
        return memo[n]

    @staticmethod
    def bottom_up(n: int) -> int:
        """
        Восходящий (табличный) подход.
        Время: O(n), Память: O(n).
        """
        if n <= 1:
            return n
        dp = [0] * (n + 1)
        dp[1] = 1
        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]
        return dp[n]

    @staticmethod
    def bottom_up_optimized(n: int) -> int:
        """
        Вариант без лишней памяти.
        Время: O(n), Память: O(1).
        """
        if n <= 1:
            return n
        prev, curr = 0, 1
        for _ in range(2, n + 1):
            prev, curr = curr, prev + curr
        return curr

class Knapsack01:
    """0-1 рюкзак: полные и оптимизированные реализации."""

    @staticmethod
    def compute(weights: List[int], values: List[int], capacity: int) -> int:
        """
        Полный табличный подход.
        Время: O(n * capacity), Память: O(n * capacity).
        """
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if weights[i - 1] <= w:
                    dp[i][w] = max(
                        values[i - 1] + dp[i - 1][w - weights[i - 1]],
                        dp[i - 1][w]
                    )
                else:
                    dp[i][w] = dp[i - 1][w]
        return dp[n][capacity]

    @staticmethod
    def compute_with_items(
        weights: List[int],
        values: List[int],
        capacity: int
    ) -> Tuple[int, List[int]]:
        """
        Полный подход с восстановлением решения.
        Время: O(n * capacity), Память: O(n * capacity).
        """
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if weights[i - 1] <= w:
                    dp[i][w] = max(
                        values[i - 1] + dp[i - 1][w - weights[i - 1]],
                        dp[i - 1][w]
                    )
                else:
                    dp[i][w] = dp[i - 1][w]
        items = []
        w = capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                items.append(i - 1)
                w -= weights[i - 1]
        items.reverse()
        return dp[n][capacity], items

    @staticmethod
    def compute_optimized(weights: List[int], values: List[int], capacity: int) -> int:
        """
        Одномерный массив, оптимизация по памяти.
        Время: O(n * capacity), Память: O(capacity).
        """
        n = len(weights)
        dp = [0] * (capacity + 1)
        for i in range(n):
            for w in range(capacity, weights[i] - 1, -1):
                dp[w] = max(dp[w], values[i] + dp[w - weights[i]])
        return dp[capacity]

    @staticmethod
    def compute_optimized_with_items(
        weights: List[int],
        values: List[int],
        capacity: int
    ) -> Tuple[int, List[int]]:
        """
        Оптимизированный подход с восстановлением (использует полную таблицу для восстановления).
        Время: O(n * capacity), Память: O(n * capacity).
        """
        n = len(weights)
        dp = [[0] * (capacity + 1) for _ in range(n + 1)]
        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if weights[i - 1] <= w:
                    dp[i][w] = max(
                        values[i - 1] + dp[i - 1][w - weights[i - 1]],
                        dp[i - 1][w]
                    )
                else:
                    dp[i][w] = dp[i - 1][w]
        items = []
        w = capacity
        for i in range(n, 0, -1):
            if dp[i][w] != dp[i - 1][w]:
                items.append(i - 1)
                w -= weights[i - 1]
        items.reverse()
        return dp[n][capacity], items

class LCS:
    """LCS — динамическая таблица и восстановление."""

    @staticmethod
    def lcs_length(text1: str, text2: str) -> int:
        """
        Длина LCS.
        Время: O(m * n), Память: O(m * n).
        """
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp[m][n]

    @staticmethod
    def lcs_find(text1: str, text2: str) -> str:
        """
        Восстановление LCS.
        Время: O(m * n), Память: O(m * n).
        """
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        lcs = []
        i, j = m, n
        while i > 0 and j > 0:
            if text1[i - 1] == text2[j - 1]:
                lcs.append(text1[i - 1])
                i -= 1
                j -= 1
            elif dp[i - 1][j] > dp[i][j - 1]:
                i -= 1
            else:
                j -= 1
        return ''.join(reversed(lcs))

    @staticmethod
    def get_matrix(text1: str, text2: str) -> List[List[int]]:
        """
        Таблица DP для LCS (для визуализации).
        """
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if text1[i - 1] == text2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1] + 1
                else:
                    dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])
        return dp

class Levenshtein:
    """Редакционное расстояние — таблицы и оптимизация."""

    @staticmethod
    def compute_distance(word1: str, word2: str) -> int:
        """
        Полный DP для расстояния Левенштейна.
        Время: O(m * n), Память: O(m * n).
        """
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        return dp[m][n]

    @staticmethod
    def compute_distance_optimized(word1: str, word2: str) -> int:
        """
        Оптимизация по памяти (одномерный массив).
        Время: O(m * n), Память: O(n).
        """
        m, n = len(word1), len(word2)
        if m < n:
            word1, word2 = word2, word1
            m, n = n, m
        prev = list(range(n + 1))
        curr = [0] * (n + 1)
        for i in range(1, m + 1):
            curr[0] = i
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    curr[j] = prev[j - 1]
                else:
                    curr[j] = 1 + min(prev[j], curr[j - 1], prev[j - 1])
            prev, curr = curr, prev
        return prev[n]

    @staticmethod
    def get_matrix(word1: str, word2: str) -> List[List[int]]:
        """
        Таблица DP для визуализации редакционного расстояния.
        """
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            dp[i][0] = i
        for j in range(n + 1):
            dp[0][j] = j
        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
        return dp

class CoinExchange:
    """Размен монет: минимальное количество, восстановление и подсчёт способов."""

    @staticmethod
    def min_coins_count(coins: List[int], amount: int) -> int:
        """
        Минимальное количество монет для суммы.
        Время: O(n * amount), Память: O(amount).
        """
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        for i in range(1, amount + 1):
            for coin in coins:
                if coin <= i:
                    dp[i] = min(dp[i], dp[i - coin] + 1)
        return dp[amount] if dp[amount] != float('inf') else -1

    @staticmethod
    def min_coins_with_change(coins: List[int], amount: int) -> Tuple[int, List[int]]:
        """
        Минимум монет и восстановление набора монет.
        """
        dp = [float('inf')] * (amount + 1)
        dp[0] = 0
        parent = [-1] * (amount + 1)
        for i in range(1, amount + 1):
            for coin in coins:
                if coin <= i and dp[i - coin] + 1 < dp[i]:
                    dp[i] = dp[i - coin] + 1
                    parent[i] = coin
        if dp[amount] == float('inf'):
            return -1, []
        used_coins = []
        current = amount
        while current > 0:
            coin = parent[current]
            used_coins.append(coin)
            current -= coin
        return dp[amount], used_coins

    @staticmethod
    def count_ways(coins: List[int], amount: int) -> int:
        """
        Число способов составить сумму данными монетами.
        Время: O(n * amount), Память: O(amount).
        """
        dp = [0] * (amount + 1)
        dp[0] = 1
        for coin in coins:
            for i in range(coin, amount + 1):
                dp[i] += dp[i - coin]
        return dp[amount]

class LIS:
    """Наибольшая возрастающая подпоследовательность: O(n^2) и O(n log n)."""

    @staticmethod
    def lis_length(arr: List[int]) -> int:
        """
        Длина LIS (квадратичный подход).
        Время: O(n^2), Память: O(n).
        """
        n = len(arr)
        if n == 0:
            return 0
        dp = [1] * n
        for i in range(1, n):
            for j in range(i):
                if arr[j] < arr[i]:
                    dp[i] = max(dp[i], dp[j] + 1)
        return max(dp)

    @staticmethod
    def reconstruct(arr: List[int]) -> List[int]:
        """
        Восстановление самой подпоследовательности (квадратичный подход).
        """
        n = len(arr)
        if n == 0:
            return []
        dp = [1] * n
        parent = [-1] * n
        for i in range(1, n):
            for j in range(i):
                if arr[j] < arr[i] and dp[j] + 1 > dp[i]:
                    dp[i] = dp[j] + 1
                    parent[i] = j
        max_length = max(dp)
        max_idx = dp.index(max_length)
        lis = []
        idx = max_idx
        while idx != -1:
            lis.append(arr[idx])
            idx = parent[idx]
        lis.reverse()
        return lis

    @staticmethod
    def length_optimized(arr: List[int]) -> int:
        """
        Оптимизированная длина LIS (бинпоиск).
        Время: O(n log n), Память: O(n).
        """
        import bisect
        tails = []
        for num in arr:
            pos = bisect.bisect_left(tails, num)
            if pos == len(tails):
                tails.append(num)
            else:
                tails[pos] = num
        return len(tails)

def pretty_print_table(table: List[List[int]], row_label: str = "", col_label: str = "") -> None:
    """
    Вывод DP-таблицы в читаемом виде.
    """
    if not table:
        return
    width = max(max(len(str(cell)) for row in table for cell in row), 4)
    if col_label:
        print("  " + col_label[:width], end="")
        for j in range(len(table[0])):
            print(f"{j:{width}}", end="")
        print()
    for i, row in enumerate(table):
        if row_label:
            print(f"{i}{row_label[min(i, len(row_label)-1)]}", end=" ")
        for cell in row:
            print(f"{cell:{width}}", end="")
        print()
