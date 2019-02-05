#!/usr/bin/env python3

from functools import partial, wraps
from itertools import takewhile, count, permutations, chain
from math import ceil, floor
from operator import gt, le
from threading import Thread, Event
from time import time, sleep as sleep_
from typing import List, Any

from checks import is_numeric, is_bounded, is_linear, is_sorted
from heap import Heap


class RestrictionError(Exception):
    def __init__(self, function):
        return super().__init__("restricted by %s" % function.__name__)
    pass


algorithms = []
def register(*checks):
    def wrapper(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            for check in checks:
                if not check(*args, **kwargs):
                    raise RestrictionError(check)
            before = time()
            return func(*args, **kwargs), time() - before
        algorithms.append(wrapped)
        return func  # Don't change the function itself
    return wrapper


@register()
def bogo(a: List[Any], n: int):
    """Generate all the permutations of ``a``, returns the sorted one"""
    for perm in permutations(a, n):
        if is_sorted(perm):
            return perm


@register(is_numeric)
def sleep(a: List[int], n: int):
    """Sleep the time of each value to append the value to a new list"""
    m = min(a)
    b = []
    threads = []
    start = Event()

    def wait(x):
        start.wait()
        sleep_((x - m) / 100)
        b.append(x)

    for x in a:
        th = Thread(target=wait, args=(x,))
        th.start()
        threads.append(th)
    start.set()
    for th in threads:
        th.join()
    return b


@register()
def bubble(a: List[Any], n: int):
    """Swap each neighbore until they are all sorted"""
    for i in range(n):
        for j in range(n - i - 1):
            if a[j] > a[j + 1]:
                a[j], a[j + 1] = a[j + 1], a[j]
    return a


@register()
def insertion_swapping(a: List[Any], n: int):
    """Move each value to the left until this value is sorted"""
    for i in range(1, n):
        while i and a[i - 1] > a[i]:
            a[i], a[i - 1] = a[i - 1], a[i]
            i -= 1
    return a


@register()
def insertion_shifting(a: List[Any], n: int):
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
def selection(a: List[Any], n: int):
    """Find smallest value and swap it with the i-th value"""
    for i in range(n):
        smallest = i
        for j in range(i + 1, n):
            if a[j] < a[smallest]:
                smallest = j
        a[i], a[smallest] = a[smallest], a[i]
    return a


@register()
def heap(a: List[Any], n: int):
    """Sequentially heapify the list and pop the largest element"""
    h = Heap(a)
    h.sort()
    return h


def shell(a: List[Any], n: int, gaps: List[int]):
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
def shell_using_shell_sequence(a: List[Any], n: int):
    seq_func = lambda k: floor(n / 2 ** (k + 1))
    gaps = takewhile(partial(le, 1), map(seq_func, count()))
    return shell(a, n, gaps)


@register()
def shell_using_tokuda_sequence(a: List[Any], n: int):
    seq_func = lambda k: ceil((9 * (9/4) ** k - 4) / 5)
    gaps = takewhile(partial(gt, n), map(seq_func, count()))
    return shell(a, n, reversed(list(gaps)))


@register()
def merge_iterative(a: List[Any], n: int):
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
def quick_recurcive(a: List[Any], n: int):
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
def merge_recurcive(a: List[Any], n: int):
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


@register(is_numeric)
def radix_lsd(a: List[int], n: int):
    length = max(a).bit_length()
    for i in range(0, length + 1, 2):
        twobits = [[] for i in range(4)]
        window = 0b11 << i
        for j in range(len(a)):
            twobits[(a[j] & window) >> i].append(a[j])
        a = list(chain(*twobits))
    return a


@register(is_numeric, is_bounded)
def counting(a: List[int], n: int):
    b = [0] * n
    m = min(a)
    for i in range(n):
        b[a[i] - m] += 1

    i = 0
    for idx, cnt in enumerate(b):
        for _ in range(cnt):
            a[i] = idx + m
            i += 1
    return a


@register(is_numeric, is_linear)
def assignment(a: List[int], n: int):
    b = [0] * n
    m = min(a)
    for e in a:
        b[e - m] = e
    return b
