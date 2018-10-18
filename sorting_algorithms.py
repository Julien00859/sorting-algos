#!/usr/bin/env python3

from typing import List
from math import ceil, floor, log2
from itertools import tee, takewhile, count, accumulate
from operator import gt, lt, ge, le
from functools import partial
from time import time
from collections import Counter
from functools import wraps
from heap import Heap

algorithms = []
def register(key=None):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            if key is not None and not key(*args, **kwargs):
                raise RestrictionError()
            before = time()
            return func(*args, **kwargs), time() - before
        algorithms.append(wrapped)
        return func  # Don't change the function itself
    return wrapper

class RestrictionError(Exception):
    pass

def is_sorted(a: List[int]):
    a_it, b_it = tee(a)
    next(b_it, None)
    for x, y in zip(a_it, b_it):
        if x > y:
            return False
    return True


def is_permutation_of(a: List[int], b: List[int]):
    return Counter(a) == Counter(b)

def is_linear(a: List[int], n: int):
    m1 = min(a)
    m2 = min(a, key=lambda x: x if x != m1 else float('inf'))
    M = max(a)

    return m2 - m1 == 1 and M - m1 == n - 1 and len(set(a)) == len(a)

def is_bounded(a: List[int], n: int):
    return max(a) - min(a) <= n - 1


@register()
def bubble(a, n):
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

@register()
def insertion_swapping(a: List[int], n: int):
    """Move each value to the left until this value is sorted"""
    for i in range(1, n):
        while i and a[i - 1] > a[i]:
            a[i], a[i - 1] = a[i - 1], a[i]
            i -= 1
    return a

@register()
def insertion_shifting(a: List[int], n: int):
    """Move each value to the left until this value is sorted"""
    for i in range(1, n):
        value = a[i]
        j = i
        while j > 0 and a[j - 1] > value:
            a[j] = a[j - 1]
            j -= 1
        a[j] = value
    return a

@register()
def selection(a: List[int], n: int):
    """Find smallest value and swap it with the i-th value"""
    for i in range(n):
        smallest = i
        for j in range(i + 1, n):
            if a[j] < a[smallest]:
                smallest = j
        a[i], a[smallest] = a[smallest], a[i]
    return a

@register()
def heap(a: List[int], n: int):
    h = Heap(a)
    h.sort()
    return h

def shell(a: List[int], n: int, gaps: List[int]):
    """:found on internet:"""
    for gap in gaps:
        for i in range(gap, n):
            tmp = a[i]
            while i >= gap and a[i - gap] > tmp:
                a[i] = a[i - gap]
                i -= gap
            a[i] = tmp
    return a

@register()
def shell_using_shell_sequence(a, n):
    seq_func = lambda k: floor(n / 2 ** (k + 1))
    gaps = takewhile(partial(le, 1), map(seq_func, count()))
    return shell(a, n, gaps)

@register()
def shell_using_tokuda_sequence(a, n):
    seq_func = lambda k: ceil((9 * (9/4) ** k - 4) / 5)
    gaps = takewhile(partial(gt, n), map(seq_func, count()))
    return shell(a, n, reversed(list(gaps)))

@register()
def merge_iterative(a: List[int], n: int):
    if n <= 1:
        return a

    tmp = list()
    def fusion(lower, half, upper):
        aa = a
        i = lower
        j = half
        while i < half and j < upper:
            if aa[i] < aa[j]:
                tmp.append(aa[i])
                i += 1
            else:
                tmp.append(aa[j])
                j += 1
        tmp.extend(aa[i:half])
        tmp.extend(aa[j:upper])
        for i in range(upper - 1, lower - 1, -1):
            aa[i] = tmp.pop()

    half_steps = 1
    steps = half_steps << 1
    while steps < n:
        for lower in range(0, n - steps, steps):
            fusion(lower, lower + half_steps, lower + steps)

        lower += steps
        fusion(lower, lower + half_steps, n)

        half_steps = steps
        steps <<= 1
    fusion(0, half_steps, n)
    return a

@register()
def quick_recurcive(a: List[int], n: int):
    if n <= 1:
        return a
    elif n == 2:
        if a[0] > a[1]:
            a[0], a[1] = a[1], a[0]

    lowers = []
    lowers_cnt = 0
    equals = []
    highers = []
    highers_cnt = 0

    pivot = a[floor(n / 2)]
    for i in range(n):
        if a[i] < pivot:
            lowers.append(a[i])
            lowers_cnt += 1
        elif a[i] > pivot:
            highers.append(a[i])
            highers_cnt += 1
        else:
            equals.append(a[i])
    
    b = quick_recurcive(lowers, lowers_cnt)
    b.extend(equals)
    b.extend(quick_recurcive(highers, highers_cnt))
    return b

@register()
def merge_recurcive(a: List[int], n: int):
    if n <= 1:
        pass
    elif n == 2:
        if a[0] > a[1]:
            a[0], a[1] = a[1], a[0]
    else:
        half = floor(n / 2)
        a1 = merge_recurcive(a[:half], half)
        a2 = merge_recurcive(a[half:], n - half)

        i = 0
        j = 0
        while i < half and j < (n - half):
            if a1[i] < a2[j]:
                a[i + j] = a1[i]
                i += 1
            else:
                a[i + j] = a2[j]
                j += 1
        while i < half:
            a[i + j] = a1[i]
            i += 1
        while j < (n - half):
            a[i + j] = a2[j]
            j += 1
    return a

def real_merge_cheat(a, start, end):
    if (start < end):
        mid = (start + end) // 2
        tmp = real_merge_cheat(a, start, mid)
        tmp.extend(reversed(real_merge_cheat(a, mid + 1, end)))
        i = 0
        j = end - start
        for k in range(start, end + 1):
            if (tmp[i] <= tmp[j]):
                a[k] = tmp[i]
                i += 1
            else:
                a[k] = tmp[j]
                j -= 1
    return a[start:end+1]

@register()
def merge_cheat(a: List[int], n: int):
    return real_merge_cheat(a, 0, n - 1)

@register(is_bounded)
def counting(a: List[int], n: int):
    """Works only if"""
    b = [0] * n
    m = min(a)
    M = max(a)
    if M - m > n:
        return b

    for i in range(n):
        b[a[i] - m] += 1

    i = 0
    for idx, count in enumerate(b):
        for _ in range(count):
            a[i] = idx + m
            i += 1
    return a

@register(is_linear)
def assignment(a: List[int], n: int):
    b = [0] * n
    m = min(a)
    for e in a:
        b[e - m] = e
    return b
