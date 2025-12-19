import unittest
from prefix_function import compute_prefix_function, compute_prefix_function_verbose
from kmp_search import kmp_search, kmp_search_first
from z_function import (
    compute_z_function, z_search, find_period, is_cyclic_shift
)
from string_matching import (
    boyer_moore_search, rabin_karp_search, rabin_karp_multiple_search
)

class TestPrefixFunction(unittest.TestCase):
    
    def test_basic_patterns(self):
        self.assertEqual(compute_prefix_function("X"), [0])
        self.assertEqual(compute_prefix_function("YZ"), [0, 0])
        self.assertEqual(compute_prefix_function("ZZ"), [0, 1])
        
    def test_repeating_sequences(self):
        self.assertEqual(compute_prefix_function("ZZZZ"), [0, 1, 2, 3])
        self.assertEqual(compute_prefix_function("MNMN"), [0, 0, 1, 2])
        
    def test_no_overlapping(self):
        self.assertEqual(compute_prefix_function("ABCDE"), [0, 0, 0, 0, 0])
        self.assertEqual(compute_prefix_function("QRST"), [0, 0, 0, 0])
        
    def test_full_overlap(self):
        result_data = compute_prefix_function("AABAAAB")
        self.assertEqual(result_data[6], 3)
        
    def test_empty_input(self):
        self.assertEqual(compute_prefix_function(""), [])
        
    def test_long_pattern(self):
        sample_pattern = "XYZXYZXY"
        pi_result = compute_prefix_function(sample_pattern)
        self.assertEqual(len(pi_result), len(sample_pattern))
        self.assertEqual(pi_result[0], 0)

class TestKMPSearch(unittest.TestCase):
    
    def test_single_match(self):
        self.assertEqual(kmp_search("ABCDEF", "DEF"), [3])
        self.assertEqual(kmp_search("HELLO", "LLO"), [2])
        
    def test_multiple_matches(self):
        self.assertEqual(kmp_search("ABABDABACDABABCABAB", "ABABCABAB"), [10])
        self.assertEqual(
            kmp_search("AABAACAADAABAABA", "AABA"),
            [0, 9, 12]
        )
        
    def test_overlapping_matches(self):
        self.assertEqual(
            kmp_search("ZZZZ", "ZZ"),
            [0, 1, 2]
        )
        self.assertEqual(
            kmp_search("MNMNMN", "MN"),
            [0, 2, 4]
        )
        
    def test_no_matches(self):
        self.assertEqual(kmp_search("ABCDEF", "WXYZ"), [])
        self.assertEqual(kmp_search("HELLO", "BYE"), [])
        
    def test_pattern_longer_than_text(self):
        self.assertEqual(kmp_search("ABC", "ABCDEF"), [])
        
    def test_empty_inputs(self):
        self.assertEqual(kmp_search("", ""), [])
        self.assertEqual(kmp_search("ABC", ""), [])
        self.assertEqual(kmp_search("", "X"), [])
        
    def test_pattern_equals_text(self):
        self.assertEqual(kmp_search("HELLO", "HELLO"), [0])
        
    def test_first_match(self):
        self.assertEqual(kmp_search_first("AABAACAADAABAABA", "AABA"), 0)
        self.assertEqual(kmp_search_first("ABCDEF", "DEF"), 3)
        self.assertEqual(kmp_search_first("HELLO", "XY"), -1)
        
    def test_case_sensitivity(self):
        self.assertEqual(kmp_search("HELLO", "hello"), [])
        self.assertEqual(kmp_search("Hello", "hello"), [])

class TestZFunction(unittest.TestCase):
    
    def test_simple_strings(self):
        self.assertEqual(compute_z_function("A"), [1])
        self.assertEqual(compute_z_function("BC"), [2, 0])
        self.assertEqual(compute_z_function("DD"), [2, 1])
        
    def test_repeating_strings(self):
        self.assertEqual(compute_z_function("AAAA"), [4, 3, 2, 1])
        self.assertEqual(compute_z_function("XYXY"), [4, 0, 2, 0])
        
    def test_unique_strings(self):
        self.assertEqual(compute_z_function("PQRST"), [5, 0, 0, 0, 0])
        
    def test_z_search(self):
        self.assertEqual(z_search("ABABDABACDABABCABAB", "ABABCABAB"), [10])
        self.assertEqual(z_search("AABAACAADAABAABA", "AABA"), [0, 9, 12])
        self.assertEqual(z_search("HELLO", "XYZ"), [])
        
    def test_find_period(self):
        self.assertEqual(find_period("XYZXYZXYZ"), 3)
        self.assertEqual(find_period("AAAA"), 1)
        self.assertEqual(find_period("MNMN"), 2)
        self.assertEqual(find_period("ABCDEF"), 6)
        
    def test_is_cyclic_shift(self):
        self.assertTrue(is_cyclic_shift("ABCD", "CDAB"))
        self.assertTrue(is_cyclic_shift("ABCD", "DABC"))
        self.assertTrue(is_cyclic_shift("ABCD", "BCDA"))
        self.assertFalse(is_cyclic_shift("ABCD", "ABDC"))
        self.assertFalse(is_cyclic_shift("ABC", "ABCD"))
        self.assertTrue(is_cyclic_shift("", ""))

class TestBoyerMoore(unittest.TestCase):
    
    def test_single_match(self):
        self.assertEqual(boyer_moore_search("ABCDEF", "DEF"), [3])
        self.assertEqual(boyer_moore_search("HELLO", "LLO"), [2])
        
    def test_multiple_matches(self):
        result = boyer_moore_search("AABAACAADAABAABA", "AABA")
        self.assertEqual(result, [0, 9, 12])
        
    def test_no_matches(self):
        self.assertEqual(boyer_moore_search("ABCDEF", "WXYZ"), [])
        
    def test_overlapping(self):
        result = boyer_moore_search("ZZZZ", "ZZ")
        self.assertTrue(len(result) > 0)
        
    def test_empty_inputs(self):
        self.assertEqual(boyer_moore_search("", ""), [])
        self.assertEqual(boyer_moore_search("ABC", ""), [])

class TestRabinKarp(unittest.TestCase):
    
    def test_single_match(self):
        self.assertEqual(rabin_karp_search("ABCDEF", "DEF"), [3])
        
    def test_multiple_matches(self):
        result = rabin_karp_search("AABAACAADAABAABA", "AABA")
        self.assertEqual(result, [0, 9, 12])
        
    def test_overlapping_matches(self):
        result = rabin_karp_search("ZZZZ", "ZZ")
        self.assertEqual(result, [0, 1, 2])
        
    def test_no_matches(self):
        self.assertEqual(rabin_karp_search("ABCDEF", "WXYZ"), [])
        
    def test_empty_inputs(self):
        self.assertEqual(rabin_karp_search("", ""), [])
        self.assertEqual(rabin_karp_search("ABC", ""), [])
        
    def test_multiple_patterns(self):
        text_data = "AABAACAADAABAABA"
        patterns_list = ["AABA", "AAB", "ABA"]
        results = rabin_karp_multiple_search(text_data, patterns_list)
        
        self.assertEqual(results["AABA"], [0, 9, 12])
        self.assertEqual(results["AAB"], [0, 9, 12])
        self.assertEqual(results["ABA"], [1, 10, 13])

class TestAlgorithmConsistency(unittest.TestCase):
    
    def test_all_algorithms_same_results(self):
        test_cases = [
            ("ABABDABACDABABCABAB", "ABABCABAB"),
            ("AABAACAADAABAABA", "AABA"),
            ("xyzxyzxyzxyz", "yzxy"),
            ("MISSISSIPPI", "ISS"),
        ]
        
        for text_sample, pattern_sample in test_cases:
            kmp_result = kmp_search(text_sample, pattern_sample)
            z_result = z_search(text_sample, pattern_sample)
            rk_result = rabin_karp_search(text_sample, pattern_sample)
            
            self.assertEqual(kmp_result, z_result)
            self.assertEqual(kmp_result, rk_result)
    
    def test_various_string_types(self):
        text1 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        pattern1 = "MNO"
        
        text2 = "XYXYXYXYXY"
        pattern2 = "XYX"
        
        text3 = "AAAABBBBCCCCDDDD"
        pattern3 = "AAB"
        
        for text_sample, pattern_sample in [(text1, pattern1), (text2, pattern2), (text3, pattern3)]:
            kmp_result = kmp_search(text_sample, pattern_sample)
            z_result = z_search(text_sample, pattern_sample)
            rk_result = rabin_karp_search(text_sample, pattern_sample)
            
            self.assertEqual(kmp_result, z_result)
            self.assertEqual(kmp_result, rk_result)

class TestPracticalProblems(unittest.TestCase):
    
    def test_find_all_occurrences(self):
        text_data = "ababcababa"
        pattern_data = "aba"
        result = kmp_search(text_data, pattern_data)
        self.assertEqual(result, [0, 5, 7])
        
    def test_find_period(self):
        periods_data = {
            "XYZXYZXYZ": 3,
            "AAAA": 1,
            "MNMNMNMN": 2,
            "ABCDEF": 6,
        }
        
        for string_val, expected_period in periods_data.items():
            found_period = find_period(string_val)
            self.assertEqual(found_period, expected_period)
    
    def test_cyclic_shift(self):
        self.assertTrue(is_cyclic_shift("abcd", "cdab"))
        self.assertTrue(is_cyclic_shift("abcd", "dabc"))
        self.assertFalse(is_cyclic_shift("abcd", "abdc"))
        self.assertFalse(is_cyclic_shift("abc", "abcd"))

class TestIntegration(unittest.TestCase):
    
    def test_complex_text_search(self):
        text_sample = "Быстрый коричневый лис прыгает через ленивую собаку. Быстрый коричневый лис."
        pattern_sample = "коричневый лис"
        
        result = kmp_search(text_sample, pattern_sample)
        self.assertEqual(len(result), 2)
        
    def test_unicode_strings(self):
        text_data = "привет мир привет"
        pattern_data = "привет"
        
        kmp_result = kmp_search(text_data, pattern_data)
        self.assertEqual(kmp_result, [0, 11])

if __name__ == "__main__":
    unittest.main(verbosity=2)