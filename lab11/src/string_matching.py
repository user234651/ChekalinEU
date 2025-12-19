def boyer_moore_search(text_data: str, pattern_data: str) -> list[int]:
    """
    Алгоритм Бойера-Мура для поиска подстроки.
    
    Сложность: O(n/m) в среднем, O(nm) в худшем
    Память: O(|Σ|)
    """
    if not pattern_data or not text_data:
        return []
    
    n, m = len(text_data), len(pattern_data)
    if m > n:
        return []
    
    bad_char_dict = {}
    for i in range(m - 1):
        bad_char_dict[pattern_data[i]] = m - 1 - i
    
    default_shift_val = m
    
    matches_list = []
    i = 0
    
    while i <= n - m:
        j = m - 1
        
        while j >= 0 and pattern_data[j] == text_data[i + j]:
            j -= 1
        
        if j < 0:
            matches_list.append(i)
            i += default_shift_val if i + m >= n else bad_char_dict.get(text_data[i + m], default_shift_val)
        else:
            bad_char = text_data[i + j]
            shift_val = bad_char_dict.get(bad_char, default_shift_val)
            shift_val = max(1, shift_val - (m - 1 - j))
            i += shift_val
    
    return matches_list

def boyer_moore_search_optimized(text_data: str, pattern_data: str) -> list[int]:
    """
    Улучшенная версия алгоритма Бойера-Мура.
    """
    if not pattern_data or not text_data:
        return []
    
    n, m = len(text_data), len(pattern_data)
    if m > n:
        return []
    
    bad_char_table = [-1] * 256
    for i in range(m):
        bad_char_table[ord(pattern_data[i])] = i
    
    matches_list = []
    shift_val = 0
    
    while shift_val <= n - m:
        j = m - 1
        
        while j >= 0 and pattern_data[j] == text_data[shift_val + j]:
            j -= 1
        
        if j < 0:
            matches_list.append(shift_val)
            shift_val += 1 if shift_val + m >= n else m - bad_char_table[ord(text_data[shift_val + m])]
        else:
            shift_val += max(1, j - bad_char_table[ord(text_data[shift_val + j])])
    
    return matches_list

def rabin_karp_search(text_data: str, pattern_data: str, prime_val: int = 101) -> list[int]:
    """
    Алгоритм Рабина-Карпа для поиска подстроки.
    
    Сложность: O(n + m) в среднем, O(nm) в худшем
    Память: O(1)
    """
    if not pattern_data or not text_data:
        return []
    
    n, m = len(text_data), len(pattern_data)
    if m > n:
        return []
    
    BASE = 256
    MOD = 101 * 10**9 + 7
    
    pattern_hash = 0
    text_hash = 0
    power_base = 1
    
    for i in range(m - 1):
        power_base = (power_base * BASE) % MOD
    
    for i in range(m):
        pattern_hash = (BASE * pattern_hash + ord(pattern_data[i])) % MOD
        text_hash = (BASE * text_hash + ord(text_data[i])) % MOD
    
    matches_list = []
    
    for i in range(n - m + 1):
        if pattern_hash == text_hash:
            if text_data[i:i + m] == pattern_data:
                matches_list.append(i)
        
        if i < n - m:
            text_hash = (BASE * (text_hash - ord(text_data[i]) * power_base) + ord(text_data[i + m])) % MOD
            if text_hash < 0:
                text_hash += MOD
    
    return matches_list

def rabin_karp_multiple_search(text_data: str, patterns_list: list[str]) -> dict[str, list[int]]:
    """
    Поиск нескольких шаблонов одновременно.
    """
    if not patterns_list or not text_data:
        return {}
    
    n = len(text_data)
    results_dict = {pattern: [] for pattern in patterns_list}
    
    BASE = 256
    MOD = 101 * 10**9 + 7
    
    pattern_hashes = {}
    for pattern in patterns_list:
        h_val = 0
        for char in pattern:
            h_val = (BASE * h_val + ord(char)) % MOD
        pattern_hashes[pattern] = h_val
    
    for pattern in patterns_list:
        m = len(pattern)
        if m > n:
            continue
        
        pattern_hash = pattern_hashes[pattern]
        power_base = 1
        
        for i in range(m - 1):
            power_base = (power_base * BASE) % MOD
        
        text_hash = 0
        for i in range(m):
            text_hash = (BASE * text_hash + ord(text_data[i])) % MOD
        
        for i in range(n - m + 1):
            if pattern_hash == text_hash:
                if text_data[i:i + m] == pattern:
                    results_dict[pattern].append(i)
            
            if i < n - m:
                text_hash = (BASE * (text_hash - ord(text_data[i]) * power_base) + ord(text_data[i + m])) % MOD
                if text_hash < 0:
                    text_hash += MOD
    
    return results_dict

if __name__ == "__main__":
    test_cases = [
        ("ABABDABACDABABCABAB", "ABABCABAB"),
        ("AABAACAADAABAABA", "AABA"),
        ("xyzxyzxyzxyz", "yzxy"),
        ("барабанщик", "рабан"),
    ]
    
    print("=" * 60)
    print("АЛГОРИТМ БОЙЕРА-МУРА:")
    print("=" * 60)
    
    for text_sample, pattern_sample in test_cases:
        positions = boyer_moore_search(text_sample, pattern_sample)
        print(f"Текст: '{text_sample}'")
        print(f"Шаблон: '{pattern_sample}'")
        print(f"Позиции: {positions}\n")
    
    print("\n" + "=" * 60)
    print("АЛГОРИТМ РАБИНА-КАРПА:")
    print("=" * 60)
    
    for text_sample, pattern_sample in test_cases:
        positions = rabin_karp_search(text_sample, pattern_sample)
        print(f"Текст: '{text_sample}'")
        print(f"Шаблон: '{pattern_sample}'")
        print(f"Позиции: {positions}\n")
    
    print("\n" + "=" * 60)
    print("ПОИСК НЕСКОЛЬКИХ ШАБЛОНОВ:")
    print("=" * 60)
    
    text_sample = "AABAACAADAABAABA"
    patterns = ["AABA", "AAB", "ABA"]
    results = rabin_karp_multiple_search(text_sample, patterns)
    
    print(f"Текст: '{text_sample}'")
    for pattern_val, positions_list in results.items():
        print(f"  Шаблон '{pattern_val}': {positions_list}")