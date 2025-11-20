import timeit
import copy
from typing import Dict, Callable, List, Tuple
import pandas as pd

def run_tests(datasets: Dict[int, Dict[str, List[int]]],
              algorithms: Dict[str, Callable[[List[int]], List[int]]],
              repeats: int = 3) -> pd.DataFrame:
    records = []
    for n, kinds in datasets.items():
        for kind_name, arr in kinds.items():
            print(f"Testing size={n}, kind={kind_name} ...")
            for alg_name, alg in algorithms.items():
                # prepare timer — ensure we use a fresh copy each run
                def run_once():
                    a_copy = copy.deepcopy(arr)
                    result = alg(a_copy)
                    if result != sorted(arr):
                        raise AssertionError(f"{alg_name} failed to sort for size={n}, kind={kind_name}")
                timer = timeit.Timer(stmt=run_once)
                try:
                    times = [timer.timeit(number=1) for _ in range(repeats)]
                except AssertionError as e:
                    raise
                mean_t = float(pd.Series(times).mean())
                std_t = float(pd.Series(times).std())
                print(f"  {alg_name}: {mean_t:.6f}s (avg over {repeats})")
                records.append({
                    'algorithm': alg_name,
                    'size': n,
                    'kind': kind_name,
                    'time_mean': mean_t,
                    'time_std': std_t
                })
    df = pd.DataFrame.from_records(records)
    return df
