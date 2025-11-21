import os
import argparse

from modules import generate_data, sorts, performance_test, plot_results

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sizes", nargs="+", type=int, default=[100, 1000, 5000, 10000],
                        help="Sizes to generate")
    parser.add_argument("--kinds", nargs="+", type=str, default=['random', 'sorted', 'reversed', 'almost_sorted'],
                        help="Data kinds")
    parser.add_argument("--repeats", type=int, default=3, help="timeit repeats")
    parser.add_argument("--out", type=str, default="results", help="output directory")
    args = parser.parse_args()

    print("Generating datasets...")
    datasets = generate_data.generate_datasets(sizes=args.sizes, kinds=args.kinds, seed=42)

    algorithms = {
        'bubble_sort': sorts.bubble_sort,
        'insertion_sort': sorts.insertion_sort,
        'merge_sort': sorts.merge_sort,
        'quick_sort': sorts.quick_sort,
        'heap_sort': sorts.heap_sort
    }

    print("Running performance tests (this may take a while for large sizes)...")
    df = performance_test.run_tests(datasets, algorithms, repeats=args.repeats)

    print("Saving and plotting results...")
    plot_results.save_summary_table(df, out_dir=args.out)
    plot_results.plot_time_vs_size(df, kind='random', out_dir=args.out)
    target_size = 5000 if 5000 in args.sizes else args.sizes[0]
    plot_results.plot_time_vs_kind(df, size=target_size, out_dir=args.out)

    print("Done. Results directory:", os.path.abspath(args.out))

if __name__ == "__main__":
    main()
