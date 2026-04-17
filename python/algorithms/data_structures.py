# © 2026 Aboubacar Sidick Meite (ApollonIUGB77) — All Rights Reserved
"""
Data Structures — 6 implementations with full operations and docstrings.

Structures:
  LinkedList   — singly linked, O(1) prepend, O(n) search/delete
  Stack        — LIFO via list, O(1) push/pop
  Queue        — FIFO via deque, O(1) enqueue/dequeue
  BinarySearchTree — insert/search/delete/traversals, O(log n) avg
  MinHeap      — O(log n) insert, O(1) peek, O(log n) extract-min
  HashTable    — separate chaining, dynamic resizing, O(1) avg ops
"""

from __future__ import annotations
from collections import deque
from typing import Any, Generator, Optional


# ══════════════════════════════════════════════════════════════════════════════
# 1. Singly Linked List
# ══════════════════════════════════════════════════════════════════════════════

class _LLNode:
    __slots__ = ("data", "next")
    def __init__(self, data: Any) -> None:
        self.data = data
        self.next: Optional[_LLNode] = None


class LinkedList:
    """
    Singly Linked List.

    Operations:
      prepend(val)  — O(1)
      append(val)   — O(n)
      delete(val)   — O(n)
      search(val)   — O(n)
      reverse()     — O(n)  in-place
      to_list()     — O(n)
      __len__       — O(1)  (tracked)
      __iter__      — O(n)
      __repr__      — shows linked chain
    """

    def __init__(self) -> None:
        self.head: Optional[_LLNode] = None
        self._size = 0

    # ── Mutators ──────────────────────────────────────────────────────────────

    def prepend(self, val: Any) -> None:
        """Insert at the front — O(1)."""
        node = _LLNode(val)
        node.next = self.head
        self.head = node
        self._size += 1

    def append(self, val: Any) -> None:
        """Insert at the tail — O(n)."""
        node = _LLNode(val)
        if not self.head:
            self.head = node
        else:
            cur = self.head
            while cur.next:
                cur = cur.next
            cur.next = node
        self._size += 1

    def delete(self, val: Any) -> bool:
        """Remove the first occurrence of val — O(n). Returns True if removed."""
        if not self.head:
            return False
        if self.head.data == val:
            self.head = self.head.next
            self._size -= 1
            return True
        cur = self.head
        while cur.next:
            if cur.next.data == val:
                cur.next = cur.next.next
                self._size -= 1
                return True
            cur = cur.next
        return False

    def reverse(self) -> None:
        """Reverse the list in-place — O(n)."""
        prev: Optional[_LLNode] = None
        cur = self.head
        while cur:
            nxt = cur.next
            cur.next = prev
            prev = cur
            cur = nxt
        self.head = prev

    # ── Accessors ─────────────────────────────────────────────────────────────

    def search(self, val: Any) -> int:
        """Return index of first occurrence, or -1 — O(n)."""
        for i, v in enumerate(self):
            if v == val:
                return i
        return -1

    def to_list(self) -> list:
        return list(self)

    def __len__(self) -> int:
        return self._size

    def __iter__(self) -> Generator:
        cur = self.head
        while cur:
            yield cur.data
            cur = cur.next

    def __repr__(self) -> str:
        return " → ".join(str(v) for v in self) + " → None"


# ══════════════════════════════════════════════════════════════════════════════
# 2. Stack (LIFO)
# ══════════════════════════════════════════════════════════════════════════════

class Stack:
    """
    LIFO Stack backed by a Python list (amortized O(1) push/pop).

    Operations:
      push(val)  — O(1) amortized
      pop()      — O(1) amortized
      peek()     — O(1)
      is_empty() — O(1)
      __len__    — O(1)
    """

    def __init__(self) -> None:
        self._data: list = []

    def push(self, val: Any) -> None:
        self._data.append(val)

    def pop(self) -> Any:
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._data.pop()

    def peek(self) -> Any:
        if self.is_empty():
            raise IndexError("peek on empty stack")
        return self._data[-1]

    def is_empty(self) -> bool:
        return not self._data

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Stack(top → {self._data[::-1]})"


# ══════════════════════════════════════════════════════════════════════════════
# 3. Queue (FIFO)
# ══════════════════════════════════════════════════════════════════════════════

class Queue:
    """
    FIFO Queue backed by collections.deque (O(1) enqueue and dequeue).

    Operations:
      enqueue(val) — O(1)
      dequeue()    — O(1)
      front()      — O(1)
      is_empty()   — O(1)
      __len__      — O(1)
    """

    def __init__(self) -> None:
        self._data: deque = deque()

    def enqueue(self, val: Any) -> None:
        self._data.append(val)

    def dequeue(self) -> Any:
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._data.popleft()

    def front(self) -> Any:
        if self.is_empty():
            raise IndexError("front of empty queue")
        return self._data[0]

    def is_empty(self) -> bool:
        return not self._data

    def __len__(self) -> int:
        return len(self._data)

    def __repr__(self) -> str:
        return f"Queue(front → {list(self._data)})"


# ══════════════════════════════════════════════════════════════════════════════
# 4. Binary Search Tree
# ══════════════════════════════════════════════════════════════════════════════

class _BSTNode:
    __slots__ = ("val", "left", "right")
    def __init__(self, val: Any) -> None:
        self.val = val
        self.left: Optional[_BSTNode] = None
        self.right: Optional[_BSTNode] = None


class BinarySearchTree:
    """
    Binary Search Tree — supports duplicates (inserted to the right).

    Operations:
      insert(val)       — O(log n) avg, O(n) worst
      search(val)       — O(log n) avg, O(n) worst
      delete(val)       — O(log n) avg, O(n) worst
      min_val()         — O(log n)
      max_val()         — O(log n)
      height()          — O(n)
      inorder()         — O(n)  → sorted list
      preorder()        — O(n)
      postorder()       — O(n)
      level_order()     — O(n)  (BFS)
    """

    def __init__(self) -> None:
        self.root: Optional[_BSTNode] = None
        self._size = 0

    # ── Mutators ──────────────────────────────────────────────────────────────

    def insert(self, val: Any) -> None:
        self.root = self._insert(self.root, val)
        self._size += 1

    def _insert(self, node: Optional[_BSTNode], val: Any) -> _BSTNode:
        if node is None:
            return _BSTNode(val)
        if val < node.val:
            node.left  = self._insert(node.left,  val)
        else:
            node.right = self._insert(node.right, val)
        return node

    def delete(self, val: Any) -> bool:
        new_root, deleted = self._delete(self.root, val)
        self.root = new_root
        if deleted:
            self._size -= 1
        return deleted

    def _delete(self, node: Optional[_BSTNode], val: Any):
        if node is None:
            return None, False
        deleted = False
        if val < node.val:
            node.left, deleted = self._delete(node.left, val)
        elif val > node.val:
            node.right, deleted = self._delete(node.right, val)
        else:
            deleted = True
            if node.left is None:
                return node.right, deleted
            if node.right is None:
                return node.left, deleted
            # Replace with inorder successor (min of right subtree)
            successor = self._min_node(node.right)
            node.val   = successor.val
            node.right, _ = self._delete(node.right, successor.val)
        return node, deleted

    def _min_node(self, node: _BSTNode) -> _BSTNode:
        cur = node
        while cur.left:
            cur = cur.left
        return cur

    # ── Accessors ─────────────────────────────────────────────────────────────

    def search(self, val: Any) -> bool:
        cur = self.root
        while cur:
            if val == cur.val:
                return True
            cur = cur.left if val < cur.val else cur.right
        return False

    def min_val(self) -> Any:
        if not self.root:
            raise ValueError("tree is empty")
        return self._min_node(self.root).val

    def max_val(self) -> Any:
        if not self.root:
            raise ValueError("tree is empty")
        cur = self.root
        while cur.right:
            cur = cur.right
        return cur.val

    def height(self) -> int:
        def _h(node):
            if node is None:
                return 0
            return 1 + max(_h(node.left), _h(node.right))
        return _h(self.root)

    def inorder(self) -> list:
        result: list = []
        def _io(node):
            if node:
                _io(node.left)
                result.append(node.val)
                _io(node.right)
        _io(self.root)
        return result

    def preorder(self) -> list:
        result: list = []
        def _pre(node):
            if node:
                result.append(node.val)
                _pre(node.left)
                _pre(node.right)
        _pre(self.root)
        return result

    def postorder(self) -> list:
        result: list = []
        def _post(node):
            if node:
                _post(node.left)
                _post(node.right)
                result.append(node.val)
        _post(self.root)
        return result

    def level_order(self) -> list[list]:
        """BFS traversal — returns list of levels."""
        if not self.root:
            return []
        levels: list[list] = []
        q = deque([self.root])
        while q:
            level = []
            for _ in range(len(q)):
                node = q.popleft()
                level.append(node.val)
                if node.left:  q.append(node.left)
                if node.right: q.append(node.right)
            levels.append(level)
        return levels

    def __len__(self) -> int:
        return self._size

    def __contains__(self, val: Any) -> bool:
        return self.search(val)

    def __repr__(self) -> str:
        return f"BST(size={self._size}, height={self.height()}, inorder={self.inorder()})"


# ══════════════════════════════════════════════════════════════════════════════
# 5. Min-Heap
# ══════════════════════════════════════════════════════════════════════════════

class MinHeap:
    """
    Min-Heap (complete binary tree stored in an array).
    The smallest element is always at the root.

    Operations:
      insert(val)     — O(log n)
      peek()          — O(1)
      extract_min()   — O(log n)
      heapify(list)   — O(n)   (build heap from existing list)
      __len__         — O(1)
    """

    def __init__(self, data: Optional[list] = None) -> None:
        self._heap: list = []
        if data:
            self.heapify(data)

    def heapify(self, data: list) -> None:
        """Build heap from list in O(n)."""
        self._heap = list(data)
        n = len(self._heap)
        for i in range(n // 2 - 1, -1, -1):
            self._sift_down(i)

    def insert(self, val: Any) -> None:
        self._heap.append(val)
        self._sift_up(len(self._heap) - 1)

    def peek(self) -> Any:
        if not self._heap:
            raise IndexError("peek on empty heap")
        return self._heap[0]

    def extract_min(self) -> Any:
        if not self._heap:
            raise IndexError("extract from empty heap")
        if len(self._heap) == 1:
            return self._heap.pop()
        root = self._heap[0]
        self._heap[0] = self._heap.pop()
        self._sift_down(0)
        return root

    def _sift_up(self, i: int) -> None:
        while i > 0:
            parent = (i - 1) // 2
            if self._heap[i] < self._heap[parent]:
                self._heap[i], self._heap[parent] = self._heap[parent], self._heap[i]
                i = parent
            else:
                break

    def _sift_down(self, i: int) -> None:
        n = len(self._heap)
        while True:
            smallest = i
            left  = 2 * i + 1
            right = 2 * i + 2
            if left  < n and self._heap[left]  < self._heap[smallest]: smallest = left
            if right < n and self._heap[right] < self._heap[smallest]: smallest = right
            if smallest == i:
                break
            self._heap[i], self._heap[smallest] = self._heap[smallest], self._heap[i]
            i = smallest

    def __len__(self) -> int:
        return len(self._heap)

    def __repr__(self) -> str:
        return f"MinHeap(min={self._heap[0] if self._heap else None}, size={len(self._heap)})"


# ══════════════════════════════════════════════════════════════════════════════
# 6. Hash Table (separate chaining)
# ══════════════════════════════════════════════════════════════════════════════

class HashTable:
    """
    Hash Table with separate chaining for collision resolution.
    Dynamically resizes when load factor exceeds 0.75.

    Operations:
      set(key, val)  — O(1) avg, O(n) worst
      get(key)       — O(1) avg, O(n) worst
      delete(key)    — O(1) avg, O(n) worst
      contains(key)  — O(1) avg
      keys()         — O(n)
      values()       — O(n)
      items()        — O(n)
      __len__        — O(1)
    """

    _LOAD_FACTOR_THRESHOLD = 0.75

    def __init__(self, initial_capacity: int = 16) -> None:
        self._capacity = initial_capacity
        self._size = 0
        self._buckets: list[list] = [[] for _ in range(self._capacity)]

    def _hash(self, key: Any) -> int:
        return hash(key) % self._capacity

    def set(self, key: Any, val: Any) -> None:
        idx = self._hash(key)
        for i, (k, _) in enumerate(self._buckets[idx]):
            if k == key:
                self._buckets[idx][i] = (key, val)
                return
        self._buckets[idx].append((key, val))
        self._size += 1
        if self._size / self._capacity > self._LOAD_FACTOR_THRESHOLD:
            self._resize()

    def get(self, key: Any, default: Any = None) -> Any:
        idx = self._hash(key)
        for k, v in self._buckets[idx]:
            if k == key:
                return v
        return default

    def delete(self, key: Any) -> bool:
        idx = self._hash(key)
        for i, (k, _) in enumerate(self._buckets[idx]):
            if k == key:
                self._buckets[idx].pop(i)
                self._size -= 1
                return True
        return False

    def contains(self, key: Any) -> bool:
        return self.get(key, _SENTINEL) is not _SENTINEL

    def keys(self) -> list:
        return [k for bucket in self._buckets for k, _ in bucket]

    def values(self) -> list:
        return [v for bucket in self._buckets for _, v in bucket]

    def items(self) -> list[tuple]:
        return [(k, v) for bucket in self._buckets for k, v in bucket]

    def _resize(self) -> None:
        old_buckets = self._buckets
        self._capacity *= 2
        self._size = 0
        self._buckets = [[] for _ in range(self._capacity)]
        for bucket in old_buckets:
            for k, v in bucket:
                self.set(k, v)

    def load_factor(self) -> float:
        return self._size / self._capacity

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: Any) -> bool:
        return self.contains(key)

    def __repr__(self) -> str:
        return (f"HashTable(size={self._size}, capacity={self._capacity}, "
                f"load={self.load_factor():.2f})")


_SENTINEL = object()
