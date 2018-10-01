#!/usr/bin/env python3

from typing import List
from math import ceil, floor, log2
from itertools import tee, takewhile, count
from operator import gt, lt, ge, le
from functools import partial
from collections import Counter

algorithms = []
def register(func):
    algorithms.append(func)
    return func

def is_sorted(iterable: list):
    a_it, b_it = tee(iterable)
    next(b_it, None)
    for a, b in zip(a_it, b_it):
        if a > b:
            return False
    return True


def is_permutation_of(a: list, b: list):
    return Counter(a) == Counter(b)


@register
def bubble(a, n):
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a

@register
def insertion_swapping(a: List[int], n: int):
    """Move each value to the left until this value is sorted"""
    for i in range(1, n):
        while i and a[i - 1] > a[i]:
            a[i], a[i - 1] = a[i - 1], a[i]
            i -= 1
    return a

@register
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

@register
def selection(a: List[int], n: int):
    """Find smallest value and swap it with the i-th value"""
    for i in range(n):
        smallest = i
        for j in range(i + 1, n):
            if a[j] < a[smallest]:
                smallest = j
        a[i], a[smallest] = a[smallest], a[i]
    return a

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

@register
def shell_using_shell_sequence(a, n):
    seq_func = lambda k: floor(n / 2 ** (k + 1))
    gaps = takewhile(partial(le, 1), map(seq_func, count()))
    return shell(a, n, gaps)

@register
def shell_using_tokuda_sequence(a, n):
    seq_func = lambda k: ceil((9 * (9/4) ** k - 4) / 5)
    gaps = takewhile(partial(gt, n), map(seq_func, count()))
    return shell(a, n, reversed(list(gaps)))

@register
def merge_recurcive(a: List[int], n: int):
    if n <= 1 :
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

@register
def merge_iteratif(a: List[int], n: int):
    if n <= 1:
        return a

    b = list()
    def fusion(lower, half, upper):
        i = lower
        j = half
        while i < half and j < upper:
            if a[i] < a[j]:
                b.append(a[i])
                i += 1
            else:
                b.append(a[j])
                j += 1
        b.extend(a[i:half])
        b.extend(a[j:upper])
        for i in range(upper - 1, lower - 1, -1):
            a[i] = b.pop()


    steps = 2
    while steps < n:
        for lower in range(0, n - steps, steps):
            fusion(lower, lower + floor(steps / 2), lower + steps)

        lower += steps
        fusion(lower, floor((lower + n) / 2), n)

        steps *= 2
    print(steps, n)
    fusion(0, steps, n)
    return a


@register
def index(a: List[int], n: int):
    """Works only with linear values"""
    b = [0] * n
    m = min(a)
    for e in a:
        b[e - m] = e
    return b

