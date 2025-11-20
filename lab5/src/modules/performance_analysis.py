import time
import random
import string

from . import hash_functions
from .hash_table_chaining import ChainingHashTable
from .hash_table_open_addressing import OpenAddressingHashTable


def random_strings(n, length=6):
    return [''.join(random.choices(string.ascii_lowercase, k=length)) for _ in range(n)]

def measure_insert(table_class, hash_func, n=1000, probe_type='linear'):
    if 'OpenAddressing' in table_class.__name__:
        table = table_class(hash_func=hash_func, probe_type=probe_type)
    else:
        table = table_class(hash_func=hash_func)

    keys = random_strings(n)
    start = time.time()
    for k in keys:
        table.insert(k, k)
    return time.time() - start
