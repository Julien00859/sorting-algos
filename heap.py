#!/usr/bin/python3

from collections import UserList
import random
import math
from time import time

class Heap(UserList):
    def __init__(self, array):
        super().__init__(array)
        for i in range(len(self)):
            self.sift_down(len(self) - i - 1, len(self))

    def validate(self):
        for i in range(len(self)):
            lchild = i * 2 + 1
            rchild = lchild + 1

            if lchild < len(self) and self[i] < self[lchild]:
                print(f"error validating {self[i]}({i}) vs {self[lchild]}({lchild})")
                return False

            if rchild < len(self) and self[i] < self[rchild]:
                print(f"error validating {self[i]}({i}) vs {self[rchild]}({rchild})")
                return False
        return True


    def swap(self, i, j):
        self[i], self[j] = self[j], self[i]

    def sift_up(self, node, size):
        """
        Compare self, neighbore and parent to find the biggest node,
        if the biggest is one of the children, that child is swap
        with its parent and then this function is call recurcively
        to sort the swapped node against its neighore and parent.
        """

        if not node:
            #print("root")
            # no parent
            return

        parent = (node - 1) // 2
        #print(f"comp {self[parent]}({parent}) <> {self[node]}({node})")
        if self[node] > self[parent]:
            #print("swap")
            self.swap(parent, node)
            self.sift_up(parent, size)

    def sift_down(self, parent, size):
        """
        Compare self and children to find the smallest node,
        if the smallest is one of the children, that child is swap
        with its parent and then this function is call recurcively
        to sort the swapped node against its children.
        """
        lchild = parent * 2 + 1
        rchild = lchild + 1
        if lchild >= size:
            # no children
            #print("bottom", rchild, lchild, size)
            pass
        elif rchild >= size:
            #print("one")
            #print(f"comp {self[parent]}({parent}) <> {self[lchild]}({lchild})")
            # just one child, comp self and child
            if self[lchild] > self[parent]:
                #print("swap")
                self.swap(parent, lchild)

        else:
            # two children, comp self and children
            #print(f"comp {self[parent]}({parent}) <> {self[lchild]}({lchild}) | {self[rchild]}({rchild})")
            bigchild = max(lchild, rchild, key=self.__getitem__)
            if self[bigchild] > self[parent]:
                #print(f"swap with {self[bigchild]}({bigchild})")
                self.swap(parent, bigchild)
                self.sift_down(bigchild, size)

    def sort(self):
        for i in range(len(self) - 1, -1, -1):
            #print(self.data)
            self.swap(0, i)
            #print(self.data)
            self.sift_down(0, i)
            #print()

    def treeview(self):
        def group(array):
            n = 1
            it = iter(array)
            buff = []
            try:
                while True:
                    line = []
                    for _ in range(n):
                        line.append(str(next(it)))
                    buff.append(line)
                    n *= 2
            except StopIteration:
                if line:
                    buff.append(line)
            return buff

        lines = []
        for idx, line in enumerate(reversed(group(self.data))):
            lines.append(" " * (idx << 1))
            for x in line:
                lines[-1] += str(x)
                lines[-1] += " " * (idx << 1 or 1)
        return "\n".join(reversed(lines))

    def __reprt__(self):
        return "<Heap [{}]>".format(", ".join(self.data))

