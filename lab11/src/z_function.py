def compute_z_function(input_string: str) -> list[int]:
    """
    Вычисление Z-функции для строки.
    
    Сложность: O(n)
    Память: O(n)
    """
    n = len(input_string)
    z_array = [0] * n
    z_array[0] = n
    
    left_idx, right_idx = 0, 0
    
    for i in range(1, n):
        if i > right_idx:
            left_idx, right_idx = i, i
            while right_idx < n and input_string[right_idx - left_idx] == input_string[right_idx]:
                right_idx += 1
            z_array[i] = right_idx - left_idx
            right_idx -= 1
        else:
            k = i - left_idx
            
            if z_array[k] < right_idx - i + 1:
                z_array[i] = z_array[k]
            else:
                left_idx = i
                while right_idx < n and input_string[right_idx - left_idx] == input_string[right_idx]:
                    right_idx += 1
                z_array[i] = right_idx - left_idx
                right_idx -= 1
    
    return z_array

def compute_z_function_verbose(input_string: str) -> tuple[list[int], list[str]]:
    """
    Вычисление Z-функции с пошаговым выводом.
    """
    n = len(input_string)
    z_array = [0] * n
    z_array[0] = n
    steps_list = []
    
    steps_list.append(f"Строка: '{input_string}'")
    steps_list.append(f"z[0] = {n}")
    
    left_idx, right_idx = 0, 0
    
    for i in range(1, n):
        step_msg = f"\nПозиция {i}: символ '{input_string[i]}'"
        
        if i > right_idx:
            step_msg += f"\n  i > right_idx ({i} > {right_idx}), начинаем новое окно"
            left_idx, right_idx = i, i
            
            while right_idx < n and input_string[right_idx - left_idx] == input_string[right_idx]:
                step_msg += f"\n    s[{right_idx - left_idx}]='{input_string[right_idx - left_idx]}' == s[{right_idx}]='{input_string[right_idx]}'"
                right_idx += 1
            
            z_array[i] = right_idx - left_idx
            right_idx -= 1
            step_msg += f"\n  Окно [{left_idx}, {right_idx}], z[{i}] = {z_array[i]}"
        else:
            k = i - left_idx
            step_msg += f"\n  i внутри окна [{left_idx}, {right_idx}]"
            step_msg += f"\n  k = {i} - {left_idx} = {k}"
            
            if z_array[k] < right_idx - i + 1:
                z_array[i] = z_array[k]
                step_msg += f"\n  z[{k}]={z_array[k]} < {right_idx - i + 1}, значит z[{i}] = {z_array[k]}"
            else:
                step_msg += f"\n  z[{k}]={z_array[k]} >= {right_idx - i + 1}, проверяем дальше"
                left_idx = i
                while right_idx < n and input_string[right_idx - left_idx] == input_string[right_idx]:
                    right_idx += 1
                z_array[i] = right_idx - left_idx
                right_idx -= 1
                step_msg += f"\n  Окно [{left_idx}, {right_idx}], z[{i}] = {z_array[i]}"
        
        steps_list.append(step_msg)
    
    steps_list.append(f"\nИтоговый массив: {z_array}")
    return z_array, steps_list

def z_search(text_data: str, pattern_data: str) -> list[int]:
    """
    Поиск паттерна с использованием Z-функции.
    """
    if not pattern_data or not text_data:
        return []
    
    m = len(pattern_data)
    n = len(text_data)
    
    if m > n:
        return []
    
    combined_string = pattern_data + "#" + text_data
    z_result = compute_z_function(combined_string)
    
    matches_list = []
    for i in range(m + 1, len(combined_string)):
        if z_result[i] == m:
            matches_list.append(i - m - 1)
    
    return matches_list

def find_period(input_string: str) -> int:
    """
    Нахождение наименьшего периода строки.
    """
    n = len(input_string)
    z_result = compute_z_function(input_string)
    
    for period in range(1, n // 2 + 1):
        if z_result[period] + period == n:
            if all(z_result[i] + i >= n or z_result[i] == 0 for i in range(1, period)):
                return period
    
    return n

def is_cyclic_shift(string1: str, string2: str) -> bool:
    """
    Проверка, является ли string2 циклическим сдвигом string1.
    """
    if len(string1) != len(string2):
        return False
    
    if not string1:
        return True
    
    combined = string2 + "#" + string1 + string1
    z_result = compute_z_function(combined)
    
    m = len(string2)
    for i in range(m + 1, len(combined)):
        if z_result[i] == m:
            return True
    
    return False

if __name__ == "__main__":
    test_strings = [
        "XYXY",
        "ZZZZ",
        "ABCDA",
        "AABAAAB",
    ]
    
    print("=" * 50)
    print("Z-ФУНКЦИЯ:")
    print("=" * 50)
    for s in test_strings:
        z_result = compute_z_function(s)
        print(f"Строка: {s:15} → z = {z_result}")
    
    print("\n" + "=" * 50)
    print("ПОИСК ПОДСТРОКИ:")
    print("=" * 50)
    test_cases = [
        ("ABABDABACDABABCABAB", "ABABCABAB"),
        ("AABAACAADAABAABA", "AABA"),
    ]
    
    for text_sample, pattern_sample in test_cases:
        positions = z_search(text_sample, pattern_sample)
        print(f"Текст: '{text_sample}'")
        print(f"Шаблон: '{pattern_sample}'")
        print(f"Позиции: {positions}\n")
    
    print("=" * 50)
    print("ПОИСК ПЕРИОДА:")
    print("=" * 50)
    period_strings = ["XYZXYZXYZ", "AAAA", "ABCDEF", "MNMNMN"]
    for s in period_strings:
        period_val = find_period(s)
        print(f"Строка: {s:15} → период = {period_val}")
    
    print("\n" + "=" * 50)
    print("ЦИКЛИЧЕСКИЙ СДВИГ:")
    print("=" * 50)
    shift_tests = [
        ("ABCD", "CDAB"),
        ("ABCD", "DABC"),
        ("ABCD", "ABDC"),
        ("xyzxyz", "yzxyzx"),
    ]
    
    for str1, str2 in shift_tests:
        result_val = is_cyclic_shift(str1, str2)
        print(f"'{str1}' и '{str2}': {result_val}")