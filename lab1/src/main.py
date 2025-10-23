from modules.search_comparsion import run_performance_analysis
from modules.plot_generator import plot_search_performance, plot_comparsion

def main():
    print("=== Анализ производительности алгоритмов поиска ===")  # O(1)
    print("Автор: ChekalinEU")                                    # O(1)
    print("Лабораторная работа 1")                               # O(1)
    
    results = run_performance_analysis()                         # O(Σ(iterations * (n_i + log n_i)))
    
    print("\nПостроение графиков...")                            # O(1)
    plot_search_performance(results)                             # O(n log n)
    plot_comparsion(results)                                     # O(n log n)
    
    print("\nАнализ завершен!")                                  # O(1)
    print("Результаты сохранены в директории src/data/")         # O(1)

if __name__ == "__main__":
    main()
# Общая сложность: O(Σ(iterations * (n_i + log n_i)))