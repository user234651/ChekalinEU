from hash_functions import simple_hash, polynomial_hash, djb2_hash
from hash_table_chaining import ChainingHashTable
from hash_table_open_addressing import OpenAddressingHashTable

def test_hash_tables():
    keys = ["apple", "banana", "cherry"]
    # Chaining
    table = ChainingHashTable(hash_func=simple_hash)
    for k in keys:
        table.insert(k, k.upper())
    assert table.search("banana") == "BANANA"
    table.delete("banana")
    assert table.search("banana") is None

    # Open addressing linear
    table2 = OpenAddressingHashTable(hash_func=polynomial_hash, probe_type='linear')
    for k in keys:
        table2.insert(k, k.upper())
    assert table2.search("cherry") == "CHERRY"
    table2.delete("cherry")
    assert table2.search("cherry") is None

    # Open addressing double
    table3 = OpenAddressingHashTable(hash_func=djb2_hash, probe_type='double')
    for k in keys:
        table3.insert(k, k.upper())
    assert table3.search("apple") == "APPLE"

if __name__ == "__main__":
    test_hash_tables()
    print("All tests passed")
