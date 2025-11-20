def simple_hash(key: str) -> int:
    """Сумма кодов символов"""
    return sum(ord(c) for c in key)

def polynomial_hash(key: str, p: int = 53, m: int = 2**64) -> int:
    """Полиномиальная хеш-функция"""
    hash_value = 0
    for i, c in enumerate(key):
        hash_value = (hash_value + (ord(c) * pow(p, i, m))) % m
    return hash_value

def djb2_hash(key: str) -> int:
    """Хеш-функция DJB2"""
    hash_value = 5381
    for c in key:
        hash_value = ((hash_value << 5) + hash_value) + ord(c)
    return hash_value & 0xFFFFFFFFFFFFFFFF
