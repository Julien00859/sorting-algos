from typing import List, Any
from itertools import tee
from collections import Counter


def is_sorted(a: List[int]):
    a_it, b_it = tee(a)
    next(b_it, None)
    for x, y in zip(a_it, b_it):
        if x > y:
            return False
    return True


def is_permutation_of(a: List[Any], b: List[int]):
    return Counter(a) == Counter(b)


def is_linear(a: List[int], n: int):
    m1 = min(a)
    m2 = min(a, key=lambda x: x if x != m1 else float('inf'))
    M = max(a)

    return m2 - m1 == 1 and M - m1 == n - 1 and len(set(a)) == len(a)


def is_bounded(a: List[int], n: int):
    return max(a) - min(a) <= n - 1


def is_numeric(a: List[Any], n: int):
    return all(map(lambda x: isinstance(x, (int, float)), a))

