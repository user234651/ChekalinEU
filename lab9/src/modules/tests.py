import unittest
from typing import List
from modules.dynamic_programming import (
    FibSeries,
    Knapsack01,
    LCS,
    Levenshtein,
    CoinExchange,
    LIS,
    pretty_print_table
)

class TestFib(unittest.TestCase):
    """Тесты для вычисления Фибоначчи"""
    
    def test_base_cases(self):
        self.assertEqual(FibSeries.naive_recursive(0), 0)
        self.assertEqual(FibSeries.naive_recursive(1), 1)
        self.assertEqual(FibSeries.memoized(0), 0)
        self.assertEqual(FibSeries.memoized(1), 1)
        self.assertEqual(FibSeries.bottom_up(0), 0)
        self.assertEqual(FibSeries.bottom_up(1), 1)
    
    def test_consistency(self):
        for n in range(2, 20):
            result_naive = FibSeries.naive_recursive(n)
            result_memo = FibSeries.memoized(n)
            result_tabular = FibSeries.bottom_up(n)
            result_opt = FibSeries.bottom_up_optimized(n)
            self.assertEqual(result_naive, result_memo)
            self.assertEqual(result_memo, result_tabular)
            self.assertEqual(result_tabular, result_opt)
    
    def test_known_values(self):
        expected = {
            5: 5,
            10: 55,
            15: 610,
            20: 6765
        }
        for n, expected_value in expected.items():
            self.assertEqual(FibSeries.bottom_up(n), expected_value)

class TestKnapsack(unittest.TestCase):
    """Тесты для рюкзака"""
    
    def test_empty_knapsack(self):
        weights = [1, 2, 3]
        values = [1, 2, 3]
        capacity = 0
        result = Knapsack01.compute(weights, values, capacity)
        self.assertEqual(result, 0)
    
    def test_single_item(self):
        weights = [5]
        values = [10]
        capacity = 10
        result = Knapsack01.compute(weights, values, capacity)
        self.assertEqual(result, 10)
    
    def test_insufficient_capacity(self):
        weights = [10, 20]
        values = [5, 10]
        capacity = 5
        result = Knapsack01.compute(weights, values, capacity)
        self.assertEqual(result, 0)
    
    def test_consistency_with_recovery(self):
        weights = [2, 3, 4, 5]
        values = [3, 4, 5, 6]
        capacity = 8
        value1 = Knapsack01.compute(weights, values, capacity)
        value2, items = Knapsack01.compute_with_items(weights, values, capacity)
        self.assertEqual(value1, value2)
    
    def test_optimized_consistency(self):
        weights = [2, 3, 4, 5]
        values = [3, 4, 5, 6]
        capacity = 8
        value1 = Knapsack01.compute(weights, values, capacity)
        value2 = Knapsack01.compute_optimized(weights, values, capacity)
        self.assertEqual(value1, value2)

class TestLCS(unittest.TestCase):
    """Тесты для LCS"""
    
    def test_identical_strings(self):
        text = "hello"
        length = LCS.lcs_length(text, text)
        lcs = LCS.lcs_find(text, text)
        self.assertEqual(length, len(text))
        self.assertEqual(lcs, text)
    
    def test_empty_strings(self):
        length = LCS.lcs_length("", "")
        lcs = LCS.lcs_find("", "")
        self.assertEqual(length, 0)
        self.assertEqual(lcs, "")
    
    def test_no_common_subsequence(self):
        length = LCS.lcs_length("abc", "def")
        lcs = LCS.lcs_find("abc", "def")
        self.assertEqual(length, 0)
        self.assertEqual(lcs, "")
    
    def test_known_cases(self):
        test_cases = [
            ("abcde", "ace", "ace"),
            ("AGGTAB", "GXTXAYB", "GTAB"),
        ]
        for text1, text2, expected_lcs in test_cases:
            lcs = LCS.lcs_find(text1, text2)
            self.assertEqual(lcs, expected_lcs)

class TestLevenshtein(unittest.TestCase):
    """Тесты для расстояния Левенштейна"""
    
    def test_identical_words(self):
        distance = Levenshtein.compute_distance("hello", "hello")
        self.assertEqual(distance, 0)
    
    def test_empty_strings(self):
        self.assertEqual(Levenshtein.compute_distance("", ""), 0)
        self.assertEqual(Levenshtein.compute_distance("a", ""), 1)
        self.assertEqual(Levenshtein.compute_distance("", "a"), 1)
    
    def test_single_character_difference(self):
        distance = Levenshtein.compute_distance("a", "b")
        self.assertEqual(distance, 1)
        distance = Levenshtein.compute_distance("a", "ab")
        self.assertEqual(distance, 1)
        distance = Levenshtein.compute_distance("ab", "a")
        self.assertEqual(distance, 1)
    
    def test_consistency(self):
        test_cases = [
            ("kitten", "sitting"),
            ("saturday", "sunday"),
            ("abcdef", "fedcba"),
        ]
        for word1, word2 in test_cases:
            dist1 = Levenshtein.compute_distance(word1, word2)
            dist2 = Levenshtein.compute_distance_optimized(word1, word2)
            self.assertEqual(dist1, dist2)
    
    def test_symmetry(self):
        word1, word2 = "hello", "world"
        dist1 = Levenshtein.compute_distance(word1, word2)
        dist2 = Levenshtein.compute_distance(word2, word1)
        self.assertEqual(dist1, dist2)

class TestCoinChange(unittest.TestCase):
    """Тесты для размена монет"""
    
    def test_zero_amount(self):
        coins = [1, 2, 5]
        count = CoinExchange.min_coins_count(coins, 0)
        self.assertEqual(count, 0)
    
    def test_single_coin(self):
        coins = [1, 2, 5]
        count = CoinExchange.min_coins_count(coins, 5)
        self.assertEqual(count, 1)
    
    def test_impossible(self):
        coins = [2, 5]
        count = CoinExchange.min_coins_count(coins, 3)
        self.assertEqual(count, -1)
    
    def test_with_recovery(self):
        coins = [1, 2, 5]
        amount = 10
        count, used_coins = CoinExchange.min_coins_with_change(coins, amount)
        self.assertEqual(count, len(used_coins))
        self.assertEqual(sum(used_coins), amount)
    
    def test_combinations(self):
        coins = [1, 2, 5]
        amount = 5
        combinations = CoinExchange.count_ways(coins, amount)
        self.assertEqual(combinations, 4)

class TestLIS(unittest.TestCase):
    """Тесты для LIS"""
    
    def test_empty_array(self):
        length = LIS.lis_length([])
        self.assertEqual(length, 0)
    
    def test_single_element(self):
        length = LIS.lis_length([5])
        self.assertEqual(length, 1)
        lis = LIS.reconstruct([5])
        self.assertEqual(lis, [5])
    
    def test_decreasing_sequence(self):
        arr = [5, 4, 3, 2, 1]
        length = LIS.lis_length(arr)
        self.assertEqual(length, 1)
    
    def test_increasing_sequence(self):
        arr = [1, 2, 3, 4, 5]
        length = LIS.lis_length(arr)
        self.assertEqual(length, 5)
        lis = LIS.reconstruct(arr)
        self.assertEqual(lis, arr)
    
    def test_consistency(self):
        test_arrays = [
            [10, 9, 2, 5, 3, 7, 101, 18],
            [0, 1, 0, 4, 4, 4, 3, 5, 1],
        ]
        for arr in test_arrays:
            len1 = LIS.lis_length(arr)
            len2 = LIS.length_optimized(arr)
            self.assertEqual(len1, len2)

if __name__ == "__main__":
    unittest.main(argv=[''], exit=False, verbosity=2)
