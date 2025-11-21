import os
from typing import List, Tuple

def binary_search_recursive(arr: List[int], target: int, lo: int = 0, hi: int = None) -> int:
    if hi is None:
        hi = len(arr) - 1
    if lo > hi:
        return -1
    mid = (lo + hi) // 2
    if arr[mid] == target:
        return mid
    elif arr[mid] < target:
        return binary_search_recursive(arr, target, mid + 1, hi)
    else:
        return binary_search_recursive(arr, target, lo, mid - 1)

# Сложность: время O(log n), глубина рекурсии O(log n).

def walk_dir_recursive(path: str, prefix: str = "") -> Tuple[List[str], int]:
    lines = []
    max_depth = 0

    try:
        entries = sorted(os.listdir(path))
    except PermissionError:
        lines.append(f"{prefix}[PermissionError]: {path}")
        return lines, 0
    except FileNotFoundError:
        lines.append(f"{prefix}[NotFound]: {path}")
        return lines, 0

    for i, name in enumerate(entries):
        full = os.path.join(path, name)
        connector = "└── " if i == len(entries) - 1 else "├── "
        lines.append(f"{prefix}{connector}{name}")
        if os.path.isdir(full):
            ext_prefix = prefix + ("    " if i == len(entries) - 1 else "│   ")
            sub_lines, sub_depth = walk_dir_recursive(full, ext_prefix)
            lines.extend(sub_lines)
            max_depth = max(max_depth, 1 + sub_depth)
    return lines, max_depth

def hanoi_moves(n: int, src: str, dst: str, aux: str, moves: List[Tuple[str,str]] = None) -> List[Tuple[str,str]]:
    if moves is None:
        moves = []
    if n <= 0:
        return moves
    if n == 1:
        moves.append((src, dst))
        return moves
    hanoi_moves(n - 1, src, aux, dst, moves)
    moves.append((src, dst))
    hanoi_moves(n - 1, aux, dst, src, moves)
    return moves

# Временная сложность: O(2^n) (число перемещений).
# Глубина рекурсии: n (цепочка вызовов уменьшается на 1 каждый уровень).
