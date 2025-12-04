from modules.binary_search_tree import BinTree
from modules.tree_traversal import *
from modules.analysis import build_balanced_tree, build_degenerate_tree

def demo_tree_operations():
    print("=== ДЕМОНСТРАЦИЯ BST ===\n")

    tree = BinTree()

    # Вставка элементов
    values = [55, 28, 72, 18, 33, 63, 88, 12, 24, 37, 47]
    print(f"Вставляем значения: {values}")

    for value in values:
        tree.add(value)

    print("\nДерево:")
    print(tree._render())

    # Проверка свойств
    print(f"Размер дерева: {tree.size()}")
    print(f"Высота дерева: {tree.compute_height()}")
    print(f"Минимальное значение: {tree.get_min().value}")
    print(f"Максимальное значение: {tree.get_max().value}")
    print(f"Является корректным BST: {tree.validate_bst()}")

    # Обходы
    print(f"\nРекурсивный in-order обход: {inorder_rec(tree.root)}")
    print(f"Итеративный in-order обход: {inorder_iter(tree.root)}")
    print(f"Pre-order обход: {preorder_rec(tree.root)}")
    print(f"Post-order обход: {postorder_rec(tree.root)}")
    print(f"Level-order обход: {level_order(tree.root)}")

    # Поиск
    search_values = [37, 58, 18]
    for value in search_values:
        result = tree.find(value)
        if result:
            print(f"Значение {value} найдено")
        else:
            print(f"Значение {value} не найдено")

    # Удаление
    delete_values = [18, 28, 55]
    for value in delete_values:
        print(f"\nУдаляем значение {value}")
        success = tree.remove(value)
        if success:
            print(f"Значение удалено")
            print(f"In-order после удаления: {inorder_rec(tree.root)}")
            print(f"BST корректно: {tree.validate_bst()}")
            print(f"Размер дерева после удаления: {tree.size()}")
        else:
            print(f"Значение {value} не найдено")

def demo_tree_comparison():
    print("\n\n=== СРАВНЕНИЕ ДЕРЕВЬЕВ ===\n")

    size = 15

    # Сбалансированное дерево
    balanced_tree, values_used = build_balanced_tree(size)
    print("Сбалансированное дерево (случайные значения):")
    print(balanced_tree._render())
    print(f"Высота: {balanced_tree.compute_height()}")
    print(f"Размер: {balanced_tree.size()}")

    # Вырожденное дерево
    degenerate_tree, values_used = build_degenerate_tree(size)
    print("\nВырожденное дерево (отсортированные значения):")
    print(degenerate_tree._render())
    print(f"Высота: {degenerate_tree.compute_height()}")
    print(f"Размер: {degenerate_tree.size()}")

if __name__ == "__main__":
    demo_tree_operations()
    demo_tree_comparison()
