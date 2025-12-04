import heapq
from collections import Counter, namedtuple
import math

# Структуры данных
TimeInterval = namedtuple('TimeInterval', ['start', 'end', 'name'])
PackItem = namedtuple('PackItem', ['value', 'weight', 'name'])
HNode = namedtuple('HNode', ['char', 'freq', 'left', 'right'])
GraphEdge = namedtuple('GraphEdge', ['u', 'v', 'weight'])

class GreedyMethods:
    """
    Класс с реализациями ряда жадных стратегий.
    """

    @staticmethod
    def schedule_intervals(intervals):
        """
        Выбор максимального множества непересекающихся интервалов.
        Сложность: O(n log n) — сортировка плюс линейная выборка.
        """
        if not intervals:
            return []

        # Поддерживаем как пары (start, end) и именованные кортежи
        if len(intervals[0]) == 2:
            intervals = [TimeInterval(start, end, f"Task_{i}")
                         for i, (start, end) in enumerate(intervals)]

        intervals_sorted = sorted(intervals, key=lambda x: x.end)

        selected = []
        last_end = -float('inf')

        for inter in intervals_sorted:
            if inter.start >= last_end:
                selected.append(inter)
                last_end = inter.end

        return selected

    @staticmethod
    def fractional_pack(capacity, items):
        """
        Непрерывная версия задачи о рюкзаке; допускает дробные части предметов.
        Сложность: O(n log n) — сортировка по удельной стоимости.
        """
        if not items or capacity <= 0:
            return 0, []

        if len(items[0]) == 2:
            items = [PackItem(value, weight, f"Item_{i}")
                     for i, (value, weight) in enumerate(items)]

        items_sorted = sorted(items, key=lambda x: x.value / x.weight, reverse=True)

        total_value = 0
        remaining = capacity
        chosen = []

        for it in items_sorted:
            if remaining >= it.weight:
                total_value += it.value
                remaining -= it.weight
                chosen.append((it, 1.0))
            else:
                frac = remaining / it.weight
                total_value += it.value * frac
                chosen.append((it, frac))
                break

        return total_value, chosen

    @staticmethod
    def huffman_encode(text):
        """
        Построение префиксного кода Хаффмана для переданной строки.
        Сложность: O(n log n) — операции с кучей при построении дерева.
        """
        if not text:
            return {}, "", None

        freq = Counter(text)

        if len(freq) == 1:
            ch = next(iter(freq))
            return {ch: '0'}, '0' * len(text), HNode(ch, freq[ch], None, None)

        heap = []
        for ch, cnt in freq.items():
            heapq.heappush(heap, (cnt, id(ch), HNode(ch, cnt, None, None)))

        while len(heap) > 1:
            f1, id1, n1 = heapq.heappop(heap)
            f2, id2, n2 = heapq.heappop(heap)
            merged = HNode(None, f1 + f2, n1, n2)
            heapq.heappush(heap, (f1 + f2, id(merged), merged))

        _, _, root = heap[0]

        codes = {}
        def build_codes(node, code):
            if node is None:
                return
            if node.char is not None:
                codes[node.char] = code
                return
            build_codes(node.left, code + '0')
            build_codes(node.right, code + '1')

        build_codes(root, "")
        encoded_text = ''.join(codes[ch] for ch in text)

        return codes, encoded_text, root

    @staticmethod
    def make_change(amount, coins):
        """
        Выдача суммы минимальным числом монет (работает для канонических систем).
        Сложность: O(n) — один проход по номиналам.
        """
        coins_sorted = sorted(coins, reverse=True)
        res = {}
        rem = amount

        for coin in coins_sorted:
            if rem == 0:
                break
            cnt = rem // coin
            if cnt > 0:
                res[coin] = cnt
                rem -= coin * cnt

        if rem > 0:
            raise ValueError(f"Невозможно набрать сумму {amount} доступными монетами")

        return res

    @staticmethod
    def prim_mst(vertices, edges):
        """
        Построение минимального остовного дерева методом Прима.
        Сложность: O(E log V) — использование кучи для рёбер.
        """
        if not vertices:
            return []

        graph = {v: [] for v in vertices}
        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, w))

        visited = set()
        mst = []
        start = vertices[0]

        heap = []
        visited.add(start)

        for neigh, w in graph[start]:
            heapq.heappush(heap, (w, start, neigh))

        while heap and len(visited) < len(vertices):
            w, u, v = heapq.heappop(heap)
            if v in visited:
                continue
            visited.add(v)
            mst.append(GraphEdge(u, v, w))
            for neigh, nw in graph[v]:
                if neigh not in visited:
                    heapq.heappush(heap, (nw, v, neigh))

        return mst

class PackSolver:
    """
    Разные точные подходы для дискретного рюкзака.
    """

    @staticmethod
    def brute_force_0_1_pack(capacity, items):
        """
        Перебор всех подмножеств для 0-1 рюкзака.
        Сложность: O(2^n) — экспоненциальная.
        """
        n = len(items)
        max_val = 0
        best = []

        for mask in range(1 << n):
            cur_w = 0
            cur_v = 0
            sel = []
            for j in range(n):
                if mask & (1 << j):
                    cur_w += items[j].weight
                    cur_v += items[j].value
                    sel.append(items[j])
            if cur_w <= capacity and cur_v > max_val:
                max_val = cur_v
                best = sel

        return max_val, best

    @staticmethod
    def compare_pack_methods(capacity, items):
        """
        Сравнение жадной стратегии с точным перебором для рюкзака.
        """
        print("Сравнение подходов для задачи рюкзака:")
        print(f"Вместимость: {capacity}")
        print("Предметы:")
        for it in items:
            print(f"  {it.name}: value={it.value}, weight={it.weight}, unit={it.value / it.weight:.2f}")

        greedy_val, greedy_sel = GreedyMethods.fractional_pack(capacity, items)
        print(f"\nЖадный (непрерывный): {greedy_val:.2f}")
        print("Выбранные (в %):")
        for it, frac in greedy_sel:
            print(f"  {it.name}: {frac * 100:.1f}%")

        exact_val = None
        if len(items) <= 20:
            exact_val, exact_sel = PackSolver.brute_force_0_1_pack(capacity, items)
            print(f"\nТочный (0-1): {exact_val}")
            print("Выбранные:")
            for it in exact_sel:
                print(f"  {it.name}")
            print(f"\nРазница: {greedy_val - exact_val:.2f}")
        else:
            print("\nТочный перебор: слишком большой набор предметов")

        return greedy_val, exact_val
