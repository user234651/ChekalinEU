# src/modules/plot_generator.py
import matplotlib.pyplot as plt

def plot_times(fill_factors, times, labels):
    for t, label in zip(times, labels):
        plt.plot(fill_factors, t, label=label)
    plt.xlabel("Load factor")
    plt.ylabel("Insertion time (s)")
    plt.legend()
    plt.show()
