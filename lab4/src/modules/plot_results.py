import matplotlib.pyplot as plt
import pandas as pd
import os

def plot_time_vs_size(df: pd.DataFrame, kind: str = 'random', out_dir='results'):
    os.makedirs(out_dir, exist_ok=True)
    subset = df[df['kind'] == kind]
    plt.figure()
    for alg, g in subset.groupby('algorithm'):
        g_sorted = g.sort_values('size')
        plt.plot(g_sorted['size'], g_sorted['time_mean'], marker='o', label=alg)
    plt.xlabel('Size (n)')
    plt.ylabel('Time (s)')
    plt.title(f'Time vs Size (kind={kind})')
    plt.legend()
    path = os.path.join(out_dir, f"time_vs_size_{kind}.png")
    plt.savefig(path)
    plt.close()
    print("Saved", path)

def plot_time_vs_kind(df: pd.DataFrame, size: int = 5000, out_dir='results'):
    os.makedirs(out_dir, exist_ok=True)
    subset = df[df['size'] == size]
    plt.figure()
    kinds = sorted(subset['kind'].unique())
    for alg, g in subset.groupby('algorithm'):
        # align by kind
        times = [float(g[g['kind'] == k]['time_mean']) if (g['kind'] == k).any() else None for k in kinds]
        plt.plot(kinds, times, marker='o', label=alg)
    plt.xlabel('Data kind')
    plt.ylabel('Time (s)')
    plt.title(f'Time vs Data Kind (size={size})')
    plt.legend()
    path = os.path.join(out_dir, f"time_vs_kind_n{size}.png")
    plt.savefig(path)
    plt.close()
    print("Saved", path)

def save_summary_table(df: pd.DataFrame, out_dir='results'):
    os.makedirs(out_dir, exist_ok=True)
    csv_path = os.path.join(out_dir, 'summary.csv')
    df.to_csv(csv_path, index=False)
    print("Saved summary table to", csv_path)
