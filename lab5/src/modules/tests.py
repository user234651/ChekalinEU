import unittest
from modules.hash_functions import sum_hash, poly_hash, djb2_hash, HashFunction
from modules.hash_table_chaining import HashTableChaining
from modules.hash_table_open_addressing import OpenAddressingHashTable

class SimpleTests(unittest.TestCase):
    def test_hash_functions(self):
        self.assertIsInstance(sum_hash("abc"), int)
        self.assertIsInstance(poly_hash("abc"), int)
        self.assertIsInstance(djb2_hash("abc"), int)

    def test_chaining_basic(self):
        ht = HashTableChaining(initial_capacity=7, hash_fn=HashFunction(sum_hash))
        ht.insert("a", 1)
        ht.insert("b", 2)
        self.assertEqual(ht.get("a"), 1)
        self.assertEqual(ht.get("b"), 2)
        self.assertTrue(ht.delete("a"))
        self.assertIsNone(ht.get("a"))

    def test_open_addressing_linear(self):
        oa = OpenAddressingHashTable(initial_capacity=11, method='linear', hash_fn=HashFunction(djb2_hash))
        for i in range(8):
            oa.insert(f"k{i}", i)
        for i in range(8):
            self.assertEqual(oa.get(f"k{i}"), i)
        self.assertTrue(oa.delete("k3"))
        self.assertIsNone(oa.get("k3"))

    def test_open_addressing_double_hash(self):
        oa = OpenAddressingHashTable(initial_capacity=11, method='double', hash_fn=HashFunction(poly_hash))
        for i in range(7):
            oa.insert(f"x{i}", i)
        for i in range(7):
            self.assertEqual(oa.get(f"x{i}"), i)

if __name__ == '__main__':
    unittest.main()
