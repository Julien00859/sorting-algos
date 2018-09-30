#!/usr/bin/env python3

import json
from collections import defaultdict, ChainMap, Counter
from typing import List
from random import shuffle
from time import time
from sys import argv
from math import ceil, floor
from itertools import tee, takewhile, count
from copy import copy
from operator import gt, lt, ge, le
from functools import partial

funcs = []
def register(func):
    funcs.append(func)
    return func

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

@register
def selection_double(a: List[int], n: int):
    """Find smallest and biggest values, swap them with the i-th and the last i-th values"""
    for i in range(int(n / 2)):
        smallest = i
        biggest = n - i - 1
        for j in range(i, n - i):
            if a[j] < a[smallest]:
                smallest = j
            if a[j] > a[biggest]:
                biggest = j

        big = a[biggest]
        small = a[smallest]
        a[smallest] = a[i]
        a[biggest] = a[n - i - 1]
        a[i] = small
        a[n - i - 1] = big
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
def merge(a: List[int], n: int):
    if n == 1:
        pass
    elif n == 2:
        if a[0] > a[1]:
            a[0], a[1] = a[1], a[0]
    else:
        half = int(n / 2)
        a1 = merge(a[:half], half)
        a2 = merge(a[half:], n - half)

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

def is_sorted(iterable):
    """\forall i,j in \setN \land 0 <= i < j < n \implies a[i] <= a[j]"""
    a_it, b_it = tee(iterable)
    next(b_it, None)
    for a, b in zip(a_it, b_it):
        if a > b:
            return False
    return True

def is_permutation_of(a: List[int], b: List[int]):
    return Counter(a) == Counter(b)

if __name__ == "__main__":
    size = int(argv[1]) if len(argv) > 1 else 100
    results = defaultdict(dict)

    if len(argv) > 2:
        funcs = filter(lambda f: f.__name__ in argv[2:], funcs)

    print("Array length:", size)

    print("\nCreating array... ", end="")
    rnd_array = list(range(floor(-size / 2), floor(size / 2)))
    print("ok\nShuffling... ", end="")
    shuffle(rnd_array)
    print("ok")


    for func in funcs:
        print()
        print("Algo:", func.__name__)

        print("Copying... ", end="", flush=True)
        tmp = copy(rnd_array)
        print("ok")

        print("Sorting... ", end="", flush=True)
        before = time()
        sorted_array = func(tmp, size)
        after = time()
        print("done, tooks {} seconds".format(round(after - before, 4)))

        print("Validating... ", end="", flush=True)
        if is_sorted(sorted_array) and is_permutation_of(rnd_array, sorted_array):
            print("ok")
            results[func.__name__][str(size)] = after - before
        else:
            print("error")
            if len(sorted_array) < 30:
                print(sorted_array)

    with open("results.json") as jsonfile:
        old_results = json.load(jsonfile)

    for algo in results.keys() | old_results.keys():
        results[algo] = dict(ChainMap(
            results.get(algo, {}),
            old_results.get(algo, {})))

    with open("results.json", "w") as jsonfile:
        json.dump(results, jsonfile, indent=2, sort_keys=True)
