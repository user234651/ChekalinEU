from modules.greedy_algorithms import GreedyMethods, PackSolver, TimeInterval, PackItem
import random

def show_interval_demo():
    """Демонстрация: подбор непересекающихся занятий."""
    print("=== ДЕМОНСТРАЦИЯ: ОТБОР ЗАНЯТИЙ ===\n")

    # Пример с семинарами
    seminars = [
        TimeInterval(8, 9, "Алгебра"),
        TimeInterval(8, 10, "Физ-лаборатория"),
        TimeInterval(9, 11, "Геометрия"),
        TimeInterval(10, 12, "Биохимия"),
        TimeInterval(11, 13, "Программирование"),
        TimeInterval(12, 14, "Литература"),
    ]

    print("Список занятий:")
    for s in seminars:
        print(f"  {s.name}: {s.start}:00–{s.end}:00")

    chosen = GreedyMethods.schedule_intervals(seminars)

    print("\nМожно посетить:")
    for s in chosen:
        print(f"  {s.name}: {s.start}:00–{s.end}:00")

    print(f"\nВместо {len(seminars)} занятий — посетимо {len(chosen)}")

def show_fractional_pack():
    """Демонстрация непрерывного рюкзака."""
    print("\n=== ДЕМОНСТРАЦИЯ: НЕПРЕРЫВНЫЙ РЮКЗАК ===\n")

    supplies = [
        PackItem(320, 3, "Колбаса"),
        PackItem(210, 2, "Сырок"),
        PackItem(160, 1, "Булка"),
        PackItem(390, 5, "Консервы"),
    ]
    capacity = 6

    print("Список провианта:")
    for p in supplies:
        unit = p.value / p.weight
        print(f"  {p.name}: value={p.value}, weight={p.weight}, unit={unit:.1f}")

    total, sel = GreedyMethods.fractional_pack(capacity, supplies)

    print(f"\nВместимость: {capacity} кг")
    print(f"Максимальная ценность: {total:.2f}")
    print("Выбрано:")
    for it, frac in sel:
        amount = it.weight * frac
        cost = it.value * frac
        print(f"  {it.name}: {amount:.1f} кг за {cost:.1f} руб ({frac:.1%})")

def show_huffman_demo():
    """Демонстрация кодирования Хаффмана."""
    print("\n=== ДЕМОНСТРАЦИЯ: ХАФФМАН ===\n")

    text = "zzzzzzzzzyyyyyxxwww"

    print(f"Исход: '{text}'")
    from collections import Counter
    freq = Counter(text)
    print("Частоты:")
    for ch, cnt in sorted(freq.items()):
        print(f"  '{ch}': {cnt} раз")

    codes, encoded, tree = GreedyMethods.huffman_encode(text)

    print("\nКоды:")
    for ch, code in sorted(codes.items()):
        print(f"  '{ch}': {code}")

    print(f"\nЗакодировано: {encoded}")
    print(f"Байт/бит исходно (ASCII): {len(text) * 8}")
    print(f"Длина кодированного: {len(encoded)}")
    print(f"Экономия: {len(text) * 8 - len(encoded)} бит")

def show_coin_demo():
    """Демонстрация задачи выдачи монет."""
    print("\n=== ДЕМОНСТРАЦИЯ: ВЫДАЧА МОНЕТ ===\n")

    systems = {
        "US-style": [25, 10, 5, 1],
        "Euro-ish": [50, 20, 10, 5, 2, 1],
        "Non-canonical": [25, 10, 1]
    }

    amounts = [68, 95, 43]

    for name, coins in systems.items():
        print(f"\nСистема: {name} -> {coins}")
        for amt in amounts:
            try:
                res = GreedyMethods.make_change(amt, coins)
                total_coins = sum(res.values())
                print(f"  {amt} центов: {res} (итого монет: {total_coins})")
            except ValueError as e:
                print(f"  {amt} центов: {e}")

def show_prim_demo():
    """Демонстрация алгоритма Прима."""
    print("\n=== ДЕМОНСТРАЦИЯ: PRIM ===\n")

    cities = ['Москва', 'Питер', 'Казань', 'Н.Новгород', 'Екат']
    roads = [
        ('Москва', 'Питер', 700),
        ('Москва', 'Казань', 820),
        ('Москва', 'Н.Новгород', 410),
        ('Питер', 'Казань', 1190),
        ('Питер', 'Екат', 1990),
        ('Казань', 'Н.Новгород', 390),
        ('Казань', 'Екат', 910),
        ('Н.Новгород', 'Екат', 1210),
    ]

    print("Города и дороги:")
    for u, v, w in roads:
        print(f"  {u} -- {v}: {w} км")

    mst = GreedyMethods.prim_mst(cities, roads)

    print("\nМинимальная сеть:")
    total = 0
    for e in mst:
        print(f"  {e.u} -- {e.v}: {e.weight} км")
        total += e.weight

    print(f"Общая длина: {total} км")

def show_knapsack_comparison():
    """Демонстрация сравнения методов для рюкзака."""
    print("\n=== ДЕМОНСТРАЦИЯ: СРАВНЕНИЕ РЮКЗАКОВ ===\n")

    items = [
        PackItem(31, 10, "Золото"),
        PackItem(21, 10, "Серебро"),
        PackItem(21, 10, "Бронза"),
    ]
    cap = 20

    print("Пример, где жадный не оптимален:")
    for it in items:
        unit = it.value / it.weight
        print(f"  {it.name}: value={it.value}, weight={it.weight}, unit={unit:.1f}")

    PackSolver.compare_pack_methods(cap, items)

if __name__ == "__main__":
    random.seed(42)

    show_interval_demo()
    show_fractional_pack()
    show_huffman_demo()
    show_coin_demo()
    show_prim_demo()
    show_knapsack_comparison()
