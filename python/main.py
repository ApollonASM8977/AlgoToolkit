# © 2026 Aboubacar Sidick Meite (ApollonIUGB77) — All Rights Reserved
"""
AlgoToolkit — Interactive CLI for algorithms and data structures.

Modules:
  [1] Sorting      — 8 algorithms with step trace
  [2] Searching    — 6 algorithms with step trace
  [3] Data Structures — LinkedList, Stack, Queue, BST, MinHeap, HashTable
  [4] Graph        — BFS, DFS, Dijkstra, Bellman-Ford, Kruskal
  [5] Benchmark    — Compare all sorting algorithms (launches benchmark.py)

Usage:
  python main.py
"""

from __future__ import annotations
import sys
import subprocess
import random

from algorithms.sorting       import ALL_SORTS
from algorithms.searching     import ALL_SEARCHES
from algorithms.data_structures import (
    LinkedList, Stack, Queue, BinarySearchTree, MinHeap, HashTable
)
from algorithms.graph import Graph, bfs, dfs, dijkstra, bellman_ford, kruskal


# ── Display helpers ────────────────────────────────────────────────────────────

def hr(char="─", w=60):  print(char * w)
def header(title):
    hr("═"); print(f"  {title}"); hr("═")
def section(title):
    print(); hr(); print(f"  {title}"); hr()


def print_array(arr: list, label: str = "") -> None:
    s = f"[{', '.join(str(x) for x in arr)}]"
    print(f"  {label + ': ' if label else ''}{s}")


def parse_int_list(prompt: str) -> list[int]:
    while True:
        raw = input(prompt).strip()
        if not raw:
            # Generate random list
            arr = [random.randint(1, 99) for _ in range(10)]
            print_array(arr, "Generated")
            return arr
        try:
            return [int(x) for x in raw.replace(",", " ").split()]
        except ValueError:
            print("  ✗ Enter space or comma-separated integers, or press Enter for random.")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 1 — Sorting
# ══════════════════════════════════════════════════════════════════════════════

def menu_sorting() -> None:
    header("SORTING ALGORITHMS")
    names = list(ALL_SORTS.keys())
    for i, n in enumerate(names, 1):
        print(f"  {i}. {n.replace('_', ' ').title()}")
    print("  0. Back")
    choice = input("\n  Choose algorithm: ").strip()

    if choice == "0": return
    try:
        algo_name = names[int(choice) - 1]
    except (ValueError, IndexError):
        print("  Invalid choice."); return

    arr = parse_int_list("\n  Enter numbers (or Enter for random): ")
    trace = input("  Show step-by-step trace? [y/N]: ").strip().lower() == "y"

    fn     = ALL_SORTS[algo_name]
    result = fn(arr, trace=trace)

    section(f"Result — {result.algorithm}")
    print_array(result.original, "Input ")
    print_array(result.sorted_arr, "Output")
    print(f"\n  Comparisons : {result.comparisons}")
    print(f"  Swaps       : {result.swaps}")
    c = result.complexity
    print(f"  Time  Best  : {c['best']}")
    print(f"  Time  Avg   : {c['average']}")
    print(f"  Time  Worst : {c['worst']}")
    print(f"  Space       : {c['space']}")

    if trace and result.steps:
        section("Step Trace")
        for step in result.steps[:20]:   # cap output
            print(f"  {step}")
        if len(result.steps) > 20:
            print(f"  ... {len(result.steps) - 20} more steps hidden (large input)")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 2 — Searching
# ══════════════════════════════════════════════════════════════════════════════

def menu_searching() -> None:
    header("SEARCHING ALGORITHMS")
    names = list(ALL_SEARCHES.keys())
    for i, n in enumerate(names, 1):
        print(f"  {i}. {n.replace('_', ' ').title()}")
    print("  0. Back")
    choice = input("\n  Choose algorithm: ").strip()

    if choice == "0": return
    try:
        algo_name = names[int(choice) - 1]
    except (ValueError, IndexError):
        print("  Invalid choice."); return

    # Binary, jump, interpolation, exponential, fibonacci need sorted input
    needs_sorted = algo_name not in ("linear",)
    arr = parse_int_list("\n  Enter numbers (or Enter for random): ")
    if needs_sorted:
        arr = sorted(arr)
        print_array(arr, "Sorted ")

    try:
        target = int(input("  Target value: ").strip())
    except ValueError:
        print("  Invalid number."); return

    trace  = input("  Show step-by-step trace? [y/N]: ").strip().lower() == "y"
    fn     = ALL_SEARCHES[algo_name]
    result = fn(arr, target, trace=trace)

    section(f"Result — {result.algorithm}")
    print(f"  Target      : {result.target}")
    print(f"  Found       : {'✓ YES' if result.found else '✗ NO'}")
    if result.found:
        print(f"  Index       : {result.index}  (value = {arr[result.index]})")
    print(f"  Comparisons : {result.comparisons}")

    if trace and result.steps:
        section("Step Trace")
        for step in result.steps[:30]:
            print(f"  {step}")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 3 — Data Structures demo
# ══════════════════════════════════════════════════════════════════════════════

def menu_data_structures() -> None:
    header("DATA STRUCTURES — DEMO")
    opts = ["LinkedList", "Stack", "Queue", "Binary Search Tree", "Min Heap", "Hash Table"]
    for i, o in enumerate(opts, 1):
        print(f"  {i}. {o}")
    print("  0. Back")
    choice = input("\n  Choose structure: ").strip()

    if choice == "0": return

    # ── LinkedList ────────────────────────────────────────────────────────────
    if choice == "1":
        section("Linked List Demo")
        ll = LinkedList()
        for v in [10, 20, 30, 40, 50]:
            ll.append(v)
        print(f"  After append 10..50 : {ll!r}")
        ll.prepend(5)
        print(f"  After prepend(5)    : {ll!r}")
        ll.delete(30)
        print(f"  After delete(30)    : {ll!r}")
        print(f"  search(40)          : index {ll.search(40)}")
        ll.reverse()
        print(f"  After reverse()     : {ll!r}")
        print(f"  Length              : {len(ll)}")

    # ── Stack ─────────────────────────────────────────────────────────────────
    elif choice == "2":
        section("Stack Demo (LIFO)")
        s = Stack()
        for v in [1, 2, 3, 4, 5]:
            s.push(v)
            print(f"  push({v})  → {s!r}")
        print(f"  peek()  → {s.peek()}")
        while not s.is_empty():
            print(f"  pop()   → {s.pop()}  (size={len(s)})")

    # ── Queue ─────────────────────────────────────────────────────────────────
    elif choice == "3":
        section("Queue Demo (FIFO)")
        q = Queue()
        for v in ["A", "B", "C", "D"]:
            q.enqueue(v)
            print(f"  enqueue({v!r}) → {q!r}")
        while not q.is_empty():
            print(f"  dequeue() → {q.dequeue()!r}  (size={len(q)})")

    # ── BST ───────────────────────────────────────────────────────────────────
    elif choice == "4":
        section("Binary Search Tree Demo")
        bst = BinarySearchTree()
        vals = [50, 30, 70, 20, 40, 60, 80]
        for v in vals:
            bst.insert(v)
        print(f"  Inserted      : {vals}")
        print(f"  Inorder       : {bst.inorder()}  (sorted ✓)")
        print(f"  Preorder      : {bst.preorder()}")
        print(f"  Postorder     : {bst.postorder()}")
        print(f"  Level-order   : {bst.level_order()}")
        print(f"  Height        : {bst.height()}")
        print(f"  Min           : {bst.min_val()}")
        print(f"  Max           : {bst.max_val()}")
        print(f"  search(40)    : {bst.search(40)}")
        bst.delete(30)
        print(f"  After delete(30), inorder: {bst.inorder()}")

    # ── MinHeap ───────────────────────────────────────────────────────────────
    elif choice == "5":
        section("Min Heap Demo")
        data = [9, 4, 7, 1, 5, 3]
        mh = MinHeap(data)
        print(f"  heapify({data}) → {mh!r}")
        mh.insert(2)
        print(f"  After insert(2) → peek = {mh.peek()}")
        while len(mh):
            print(f"  extract_min() → {mh.extract_min()}  (remaining={len(mh)})")

    # ── HashTable ─────────────────────────────────────────────────────────────
    elif choice == "6":
        section("Hash Table Demo")
        ht = HashTable()
        for k, v in [("name", "Aboubacar"), ("age", 21), ("city", "Abidjan"), ("lang", "Python")]:
            ht.set(k, v)
            print(f"  set({k!r}, {v!r})")
        print(f"\n  {ht!r}")
        print(f"  get('name')   → {ht.get('name')}")
        print(f"  'age' in ht   → {'age' in ht}")
        ht.delete("city")
        print(f"  After delete('city'), keys: {ht.keys()}")
        print(f"  items()       → {ht.items()}")


# ══════════════════════════════════════════════════════════════════════════════
# MODULE 4 — Graph
# ══════════════════════════════════════════════════════════════════════════════

def _build_sample_graph() -> Graph:
    """Build a sample weighted undirected graph for demos."""
    g = Graph(directed=False)
    edges = [
        ("A", "B", 4), ("A", "C", 2), ("B", "C", 5),
        ("B", "D", 10), ("C", "E", 3), ("D", "F", 11),
        ("E", "D", 4), ("E", "F", 8), ("F", "G", 2),
    ]
    for u, v, w in edges:
        g.add_edge(u, v, w)
    return g


def menu_graph() -> None:
    header("GRAPH ALGORITHMS")
    g = _build_sample_graph()
    print("  Sample graph (undirected, weighted):")
    print("  Nodes:", ", ".join(sorted(g.nodes)))
    print("  Edges:", ", ".join(f"{u}-{v}(w={w:.0f})" for u, v, w in sorted(g.edges)))

    opts = ["BFS", "DFS", "Dijkstra", "Bellman-Ford", "Kruskal MST"]
    print()
    for i, o in enumerate(opts, 1):
        print(f"  {i}. {o}")
    print("  0. Back")
    choice = input("\n  Choose algorithm: ").strip()
    if choice == "0": return

    start = input("  Start node [A]: ").strip() or "A"
    trace = input("  Show steps? [y/N]: ").strip().lower() == "y"

    # ── BFS ───────────────────────────────────────────────────────────────────
    if choice == "1":
        result = bfs(g, start, trace)
        section("BFS Result")
        print(f"  Visit order : {' → '.join(str(n) for n in result.visited)}")
        print(f"  Distances   : {dict(sorted(result.distances.items()))}")
        target = input("  Path to node (or Enter to skip): ").strip()
        if target and target in g.nodes:
            print(f"  Path {start}→{target}: {result.path_to(target)}")

    # ── DFS ───────────────────────────────────────────────────────────────────
    elif choice == "2":
        result = dfs(g, start, trace)
        section("DFS Result")
        print(f"  Visit order : {' → '.join(str(n) for n in result.visited)}")
        print(f"  Has cycle   : {result.has_cycle}")
        print(f"  Discovery   : {dict(sorted(result.discovery.items()))}")

    # ── Dijkstra ──────────────────────────────────────────────────────────────
    elif choice == "3":
        result = dijkstra(g, start, trace)
        section("Dijkstra Shortest Paths")
        for node in sorted(result.distances):
            d = result.distances[node]
            path = result.path_to(node)
            d_str = f"{d:.1f}" if d != float("inf") else "∞"
            print(f"  {start} → {node}  dist={d_str}  path={path}")

    # ── Bellman-Ford ──────────────────────────────────────────────────────────
    elif choice == "4":
        result = bellman_ford(g, start, trace)
        section("Bellman-Ford Shortest Paths")
        print(f"  Negative cycle detected: {result.negative_cycle}")
        for node in sorted(result.distances):
            d = result.distances[node]
            d_str = f"{d:.1f}" if d != float("inf") else "∞"
            print(f"  {start} → {node}  dist={d_str}")

    # ── Kruskal ───────────────────────────────────────────────────────────────
    elif choice == "5":
        result = kruskal(g, trace)
        section("Kruskal MST")
        for u, v, w in result.mst_edges:
            print(f"  {u} — {v}  (weight={w:.1f})")
        print(f"\n  Total MST weight: {result.total_weight:.1f}")


# ══════════════════════════════════════════════════════════════════════════════
# Main menu
# ══════════════════════════════════════════════════════════════════════════════

MENU = [
    ("Sorting Algorithms",   menu_sorting),
    ("Searching Algorithms", menu_searching),
    ("Data Structures",      menu_data_structures),
    ("Graph Algorithms",     menu_graph),
    ("Benchmark (all sorts)", None),
]


def main() -> None:
    print("\n" + "═" * 60)
    print("  ALGO TOOLKIT")
    print("  © 2026 Aboubacar Sidick Meite (ApollonIUGB77)")
    print("═" * 60)

    while True:
        print()
        for i, (name, _) in enumerate(MENU, 1):
            print(f"  {i}. {name}")
        print("  0. Exit")
        choice = input("\n  > ").strip()

        if choice == "0":
            print("\n  Goodbye!\n")
            sys.exit(0)

        try:
            idx = int(choice) - 1
            name, fn = MENU[idx]
        except (ValueError, IndexError):
            print("  Invalid choice."); continue

        if fn is None:
            # Benchmark — launch subprocess
            print("\n  Launching benchmark...\n")
            subprocess.run([sys.executable, "benchmark.py"])
        else:
            fn()


if __name__ == "__main__":
    main()
