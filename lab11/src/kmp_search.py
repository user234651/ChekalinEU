from prefix_function import compute_prefix_function

def kmp_search(text: str, pattern: str) -> list[int]:
    """
    Алгоритм Кнута-Морриса-Пратта для поиска паттерна.
    Возвращает список индексов всех вхождений.
    
    Сложность: O(n + m)
    Память: O(m)
    """
    if not pattern or not text:
        return []
    
    n, m = len(text), len(pattern)
    if m > n:
        return []
    
    prefix_array = compute_prefix_function(pattern)
    matches = []
    pattern_idx = 0
    
    for i in range(n):
        while pattern_idx > 0 and text[i] != pattern[pattern_idx]:
            pattern_idx = prefix_array[pattern_idx - 1]
        
        if text[i] == pattern[pattern_idx]:
            pattern_idx += 1
        
        if pattern_idx == m:
            matches.append(i - m + 1)
            pattern_idx = prefix_array[m - 1]
    
    return matches

def kmp_search_first(text: str, pattern: str) -> int:
    """
    Поиск первого вхождения паттерна.
    Возвращает индекс или -1.
    """
    if not pattern or not text:
        return -1
    
    n, m = len(text), len(pattern)
    if m > n:
        return -1
    
    prefix_array = compute_prefix_function(pattern)
    pattern_idx = 0
    
    for i in range(n):
        while pattern_idx > 0 and text[i] != pattern[pattern_idx]:
            pattern_idx = prefix_array[pattern_idx - 1]
        
        if text[i] == pattern[pattern_idx]:
            pattern_idx += 1
        
        if pattern_idx == m:
            return i - m + 1
    
    return -1

def kmp_search_with_steps(text: str, pattern: str) -> tuple[list[int], list[str]]:
    """
    Поиск с пошаговым отображением процесса.
    """
    if not pattern or not text:
        return [], []
    
    n, m = len(text), len(pattern)
    if m > n:
        return [], ["Длина паттерна превышает длину текста"]
    
    prefix_array = compute_prefix_function(pattern)
    matches = []
    steps = []
    pattern_idx = 0
    
    steps.append(f"Текст: {text}")
    steps.append(f"Ищем:  {pattern}")
    steps.append(f"π:     {prefix_array}")
    steps.append("")
    
    for i in range(n):
        step_msg = f"Позиция {i}: символ '{text[i]}' (в паттерне индекс={pattern_idx})"
        
        while pattern_idx > 0 and text[i] != pattern[pattern_idx]:
            step_msg += f"\n  Различие: '{text[i]}' ≠ '{pattern[pattern_idx]}'"
            pattern_idx = prefix_array[pattern_idx - 1]
            step_msg += f" → новый индекс = {pattern_idx}"
        
        if text[i] == pattern[pattern_idx]:
            step_msg += f"\n  Совпадение: '{text[i]}' == '{pattern[pattern_idx]}' → индекс = {pattern_idx + 1}"
            pattern_idx += 1
        
        if pattern_idx == m:
            step_msg += f"\n  ✓ Обнаружено вхождение на позиции {i - m + 1}"
            matches.append(i - m + 1)
            pattern_idx = prefix_array[m - 1]
        
        steps.append(step_msg)
    
    steps.append(f"\nИтог: найдено вхождений — {len(matches)}")
    if matches:
        steps.append(f"Местоположения: {matches}")
    
    return matches, steps

if __name__ == "__main__":
    test_data = [
        ("ABABDABACDABABCABAB", "ABABCABAB"),
        ("AABAACAADAABAABA", "AABA"),
        ("xyzxyzxyzxyz", "yzxy"),
        ("барабанщик", "рабан"),
    ]
    
    for text_data, pattern_data in test_data:
        positions = kmp_search(text_data, pattern_data)
        print(f"Текст: '{text_data}'")
        print(f"Шаблон: '{pattern_data}'")
        print(f"Позиции: {positions}\n")