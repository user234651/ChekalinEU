def compute_prefix_function(input_string: str) -> list[int]:
    """
    Вычисление префикс-функции для строки.
    
    Сложность: O(n)
    Память: O(n)
    """
    n = len(input_string)
    prefix_array = [0] * n
    
    for i in range(1, n):
        j = prefix_array[i - 1]
        
        while j > 0 and input_string[i] != input_string[j]:
            j = prefix_array[j - 1]
        
        if input_string[i] == input_string[j]:
            j += 1
        
        prefix_array[i] = j
    
    return prefix_array

def compute_prefix_function_verbose(input_string: str) -> tuple[list[int], list[str]]:
    """
    Вычисление префикс-функции с детальным выводом.
    """
    n = len(input_string)
    prefix_array = [0] * n
    steps_list = []
    
    steps_list.append(f"Исходная строка: '{input_string}'")
    steps_list.append(f"π[0] = 0 (начальное значение)")
    
    for i in range(1, n):
        j = prefix_array[i - 1]
        step_info = f"\nПозиция {i}: символ '{input_string[i]}'"
        
        while j > 0 and input_string[i] != input_string[j]:
            step_info += f"\n  '{input_string[i]}' ≠ '{input_string[j]}' (j={j}), переходим к π[{j-1}]={prefix_array[j-1]}"
            j = prefix_array[j - 1]
        
        if input_string[i] == input_string[j]:
            step_info += f"\n  '{input_string[i]}' == '{input_string[j]}', увеличиваем j"
            j += 1
        
        prefix_array[i] = j
        step_info += f"\n  π[{i}] = {j}"
        steps_list.append(step_info)
    
    steps_list.append(f"\nИтоговый массив: {prefix_array}")
    return prefix_array, steps_list

if __name__ == "__main__":
    test_strings = [
        "XYXY",
        "ZZZZ",
        "ABCDA",
        "AABAAAB",
        "XYZXYZXY"
    ]
    
    for s in test_strings:
        pi_result = compute_prefix_function(s)
        print(f"Строка: {s:15} → π = {pi_result}")