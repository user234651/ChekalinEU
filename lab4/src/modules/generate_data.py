import random
from typing import Dict, List
import numpy as np

def generate_array(n: int, kind: str, seed: int = None) -> List[int]:
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)
    if kind == 'random':
        return list(np.random.randint(-10**6, 10**6, size=n))
    elif kind == 'sorted':
        arr = list(np.random.randint(-10**6, 10**6, size=n))
        arr.sort()
        return arr
    elif kind == 'reversed':
        arr = list(np.random.randint(-10**6, 10**6, size=n))
        arr.sort(reverse=True)
        return arr
    elif kind == 'almost_sorted':
        arr = list(np.random.randint(-10**6, 10**6, size=n))
        arr.sort()
        k = max(1, int(0.05 * n))
        for _ in range(k):
            i = random.randrange(0, n)
            j = random.randrange(0, n)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    else:
        raise ValueError(f'Unknown kind: {kind}')

def generate_datasets(sizes=None, kinds=None, seed=None) -> Dict[int, Dict[str, List[int]]]:
    if sizes is None:
        sizes = [100, 1000, 5000, 10000]
    if kinds is None:
        kinds = ['random', 'sorted', 'reversed', 'almost_sorted']
    datasets = {}
    for n in sizes:
        datasets[n] = {}
        for k in kinds:
            datasets[n][k] = generate_array(n, k, seed=seed)
    return datasets

if __name__ == "__main__":
    ds = generate_datasets()
    print("Generated sizes:", list(ds.keys()))
