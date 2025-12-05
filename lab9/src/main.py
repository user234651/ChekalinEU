import unittest
from typing import List
from modules.dynamic_programming import (
    FibSeries,
    Knapsack01,
    LCS,
    Levenshtein,
    CoinExchange,
    LIS,
    pretty_print_table
)

def demo_fib():
    """Примеры вычисления ряда Фибоначчи"""
    print("\n" + "="*70)
    print("ПРИМЕР 1: РЯД ФИБОНАЧЧИ")
    print("="*70)
    
    n = 10
    print(f"\nВычисляем F({n}):")
    
    # Наивный подход
    result_naive = FibSeries.naive_recursive(n)
    print(f"1) Наивная рекурсия: F({n}) = {result_naive}")
    
    # Мемоизация
    result_memo = FibSeries.memoized(n)
    print(f"2) С кешем:        F({n}) = {result_memo}")
    
    # Табличный подход
    result_tabular = FibSeries.bottom_up(n)
    print(f"3) Восходящий:     F({n}) = {result_tabular}")
    
    # Оптимизированный
    result_opt = FibSeries.bottom_up_optimized(n)
    print(f"4) Память-оптим.:  F({n}) = {result_opt}")
    
    print(f"\nПервые 15 чисел ряда (пример):")
    fibs = [FibSeries.bottom_up(i) for i in range(15)]
    print(fibs)


def demo_knapsack():
    """Пример задачи рюкзака 0-1"""
    print("\n" + "="*70)
    print("ПРИМЕР 2: KNAPSACK 0-1")
    print("="*70)
    
    # Пример 1: классический набор
    weights = [2, 3, 4, 5]
    values = [3, 4, 5, 6]
    capacity = 8
    
    print(f"\nВходные данные:")
    print(f"Предметы: {list(zip(range(len(weights)), weights, values))}")
    print(f"Вместимость: {capacity}")
    
    # Только максимальная стоимость
    max_value = Knapsack01.compute(weights, values, capacity)
    print(f"\nМаксимальная стоимость: {max_value}")
    
    # С восстановлением
    max_value, items = Knapsack01.compute_with_items(weights, values, capacity)
    print(f"\nС восстановлением решения:")
    print(f"Макс. стоимость: {max_value}")
    print(f"Выбранные предметы (индексы): {items}")
    print(f"Детали:")
    total_weight = 0
    total_value = 0
    for i in items:
        print(f"  Предмет {i}: вес={weights[i]}, стоимость={values[i]}")
        total_weight += weights[i]
        total_value += values[i]
    print(f"Итого: вес={total_weight}, стоимость={total_value}")
    
    # Пример 2: другой набор
    print("\n" + "-"*70)
    print("\nПример 2:")
    weights2 = [6, 3, 4, 2]
    values2 = [30, 14, 16, 9]
    capacity2 = 10
    
    print(f"Предметы: {list(zip(range(len(weights2)), weights2, values2))}")
    print(f"Вместимость: {capacity2}")
    
    max_value2, items2 = Knapsack01.compute_with_items(weights2, values2, capacity2)
    print(f"Максимальная стоимость: {max_value2}")
    print(f"Выбранные предметы: {items2}")


def demo_lcs():
    """Пример задачи LCS (наибольшая общая подпоследовательность)"""
    print("\n" + "="*70)
    print("ПРИМЕР 3: LCS")
    print("="*70)
    
    test_cases = [
        ("abcde", "ace"),
        ("AGGTAB", "GXTXAYB"),
        ("greetings", "growing"),
    ]
    
    for text1, text2 in test_cases:
        print(f"\nСтроки: '{text1}' и '{text2}'")
        
        length = LCS.lcs_length(text1, text2)
        print(f"Длина LCS: {length}")
        
        lcs = LCS.lcs_find(text1, text2)
        print(f"LCS: '{lcs}'")


def demo_levenshtein():
    """Пример вычисления редакционного расстояния"""
    print("\n" + "="*70)
    print("ПРИМЕР 4: РАССТОЯНИЕ ЛЕВЕНШТЕЙНА")
    print("="*70)
    
    test_cases = [
        ("kitten", "sitting"),
        ("saturday", "sunday"),
        ("", "b"),
        ("b", ""),
    ]
    
    for word1, word2 in test_cases:
        print(f"\nПреобразуем '{word1}' -> '{word2}':")
        
        distance = Levenshtein.compute_distance(word1, word2)
        print(f"Расстояние: {distance}")


def demo_coin_change():
    """Пример размена монет"""
    print("\n" + "="*70)
    print("ПРИМЕР 5: РАЗМЕН МОНЕТ")
    print("="*70)
    
    coins = [1, 2, 5, 10]
    amount = 17
    
    print(f"Номиналы: {coins}")
    print(f"Сумма: {amount}")
    
    # Минимальное число монет
    min_count = CoinExchange.min_coins_count(coins, amount)
    print(f"\nМин. количество монет: {min_count}")
    
    # С восстановлением
    min_count, used_coins = CoinExchange.min_coins_with_change(coins, amount)
    print(f"Используемые монеты: {used_coins}")
    print(f"Проверка: {' + '.join(map(str, used_coins))} = {sum(used_coins)}")
    
    # Количество способов
    print(f"\nЧисло способов составить {amount}:")
    combinations = CoinExchange.count_ways(coins, amount)
    print(f"{combinations} способов")


def demo_lis():
    """Пример LIS (наибольшая возрастающая подпоследовательность)"""
    print("\n" + "="*70)
    print("ПРИМЕР 6: LIS")
    print("="*70)
    
    test_arrays = [
        [11, 9, 2, 5, 3, 7, 101, 18],
        [0, 1, 0, 4, 4, 4, 3, 6, 1],
        [6, 5, 4, 3, 2],
    ]
    
    for arr in test_arrays:
        print(f"\nМассив: {arr}")
        
        length = LIS.lis_length(arr)
        print(f"Длина LIS: {length}")
        
        lis = LIS.reconstruct(arr)
        print(f"LIS: {lis}")
        
        length_opt = LIS.length_optimized(arr)
        print(f"Длина (O(n log n)): {length_opt}")

def main():
    """Запуск демонстраций"""
    print("\n" + "="*70)
    print("ДИНАМИЧЕСКОЕ ПРОГРАММИРОВАНИЕ — ДЕМОНСТРАЦИИ")
    print("="*70)
    
    demo_fib()
    demo_knapsack()
    demo_lcs()
    demo_levenshtein()
    demo_coin_change()
    demo_lis()

if __name__ == "__main__":
    main()
