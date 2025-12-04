import unittest
from modules.greedy_algorithms import GreedyMethods, PackSolver, TimeInterval, PackItem

class TestGreedyAlgorithms(unittest.TestCase):
    """Тесты жадных методов."""

    def test_interval_scheduling(self):
        intervals = [
            TimeInterval(1, 3, "A"),
            TimeInterval(2, 5, "B"),
            TimeInterval(4, 7, "C"),
            TimeInterval(6, 9, "D"),
            TimeInterval(8, 10, "E"),
        ]

        selected = GreedyMethods.schedule_intervals(intervals)

        for i in range(len(selected) - 1):
            self.assertLessEqual(selected[i].end, selected[i + 1].start)

        self.assertEqual(len(selected), 3)  # A, C, E

    def test_fractional_knapsack(self):
        items = [
            PackItem(60, 10, "Item1"),
            PackItem(100, 20, "Item2"),
            PackItem(120, 30, "Item3"),
        ]
        capacity = 50

        value, selection = GreedyMethods.fractional_pack(capacity, items)

        expected_value = 60 + 100 + (120 * 20 / 30)
        self.assertAlmostEqual(value, expected_value, places=2)

        total_weight = 0
        for item, fraction in selection:
            total_weight += item.weight * fraction

        self.assertLessEqual(total_weight, capacity)

    def test_huffman_coding(self):
        text = "abracadabra"

        codes, encoded, tree = GreedyMethods.huffman_encode(text)

        unique_chars = set(text)
        self.assertEqual(set(codes.keys()), unique_chars)

        all_codes = list(codes.values())
        for i, code1 in enumerate(all_codes):
            for j, code2 in enumerate(all_codes):
                if i != j:
                    self.assertFalse(code1.startswith(code2))
                    self.assertFalse(code2.startswith(code1))

        decoded_chars = []
        current = ""
        for bit in encoded:
            current += bit
            if current in codes.values():
                for ch, c in codes.items():
                    if c == current:
                        decoded_chars.append(ch)
                        current = ""
                        break

        decoded_text = "".join(decoded_chars)
        self.assertEqual(decoded_text, text)

    def test_coin_change(self):
        coins = [25, 10, 5, 1]
        amount = 67

        result = GreedyMethods.make_change(amount, coins)

        total = sum(coin * count for coin, count in result.items())
        self.assertEqual(total, amount)

        total_coins = sum(result.values())
        self.assertEqual(total_coins, 6)

    def test_prim_algorithm(self):
        vertices = ['A', 'B', 'C', 'D']
        edges = [
            ('A', 'B', 1),
            ('A', 'C', 3),
            ('B', 'C', 2),
            ('B', 'D', 4),
            ('C', 'D', 5),
        ]

        mst_edges = GreedyMethods.prim_mst(vertices, edges)

        self.assertEqual(len(mst_edges), len(vertices) - 1)

        total_weight = sum(edge.weight for edge in mst_edges)
        self.assertEqual(total_weight, 7)

        connected = set()
        for e in mst_edges:
            connected.add(e.u)
            connected.add(e.v)

        self.assertEqual(connected, set(vertices))

class TestPackSolver(unittest.TestCase):
    """Тесты точных методов для рюкзака."""

    def test_brute_force_01_knapsack(self):
        items = [
            PackItem(60, 10, "Item1"),
            PackItem(100, 20, "Item2"),
            PackItem(120, 30, "Item3"),
        ]
        capacity = 50

        value, selection = PackSolver.brute_force_0_1_pack(capacity, items)

        total_weight = sum(item.weight for item in selection)
        self.assertLessEqual(total_weight, capacity)

        self.assertEqual(value, 220)

if __name__ == "__main__":
    unittest.main()
