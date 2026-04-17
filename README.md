# AlgoToolkit

![Java](https://img.shields.io/badge/Java-17-orange?style=flat-square&logo=openjdk)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/License-All%20Rights%20Reserved-red?style=flat-square)

> Algorithms & data structures — original Java implementations from an Algorithms course,  
> rewritten and expanded in Python with complete documentation, complexity analysis, step-by-step tracing, and benchmarking.

---

## Structure

```
AlgoToolkit/
├── java/                          # Original Java implementations (course work)
│   ├── ADT/                       # Abstract Data Type — IntList (linked list)
│   ├── BinaryTree/                # BST, BinarySearch, QuickSort, FindMax
│   └── CaesarCracking/            # Caesar cipher encrypt/decrypt/brute-force
│
└── python/                        # Expanded Python toolkit
    ├── algorithms/
    │   ├── sorting.py             # 8 sorting algorithms
    │   ├── searching.py           # 6 searching algorithms
    │   ├── data_structures.py     # 6 data structures
    │   └── graph.py               # 5 graph algorithms
    ├── benchmark.py               # Performance comparison tool
    └── main.py                    # Interactive CLI
```

---

## Python Toolkit

### Sorting Algorithms (8)

| Algorithm | Best | Average | Worst | Space | Stable |
|-----------|------|---------|-------|-------|--------|
| Bubble Sort | O(n) | O(n²) | O(n²) | O(1) | ✓ |
| Selection Sort | O(n²) | O(n²) | O(n²) | O(1) | ✗ |
| Insertion Sort | O(n) | O(n²) | O(n²) | O(1) | ✓ |
| Merge Sort | O(n log n) | O(n log n) | O(n log n) | O(n) | ✓ |
| Quick Sort | O(n log n) | O(n log n) | O(n²) | O(log n) | ✗ |
| Heap Sort | O(n log n) | O(n log n) | O(n log n) | O(1) | ✗ |
| Counting Sort | O(n+k) | O(n+k) | O(n+k) | O(k) | ✓ |
| Radix Sort | O(nk) | O(nk) | O(nk) | O(n+k) | ✓ |

### Searching Algorithms (6)

| Algorithm | Time | Requirement |
|-----------|------|-------------|
| Linear Search | O(n) | None |
| Binary Search | O(log n) | Sorted |
| Jump Search | O(√n) | Sorted |
| Interpolation Search | O(log log n) avg | Sorted, uniform |
| Exponential Search | O(log n) | Sorted |
| Fibonacci Search | O(log n) | Sorted |

### Data Structures (6)

| Structure | Key Operations |
|-----------|---------------|
| LinkedList | prepend O(1), append O(n), delete O(n), reverse O(n) |
| Stack | push O(1), pop O(1), peek O(1) |
| Queue | enqueue O(1), dequeue O(1) |
| Binary Search Tree | insert/search/delete O(log n) avg, all traversals |
| Min Heap | insert O(log n), extract-min O(log n), heapify O(n) |
| Hash Table | set/get/delete O(1) avg, dynamic resizing |

### Graph Algorithms (5)

| Algorithm | Time | Purpose |
|-----------|------|---------|
| BFS | O(V+E) | Level-order traversal, shortest path (hops) |
| DFS | O(V+E) | Depth-first, cycle detection |
| Dijkstra | O((V+E) log V) | Shortest paths, non-negative weights |
| Bellman-Ford | O(V·E) | Shortest paths, negative weights, cycle detection |
| Kruskal | O(E log E) | Minimum Spanning Tree |

---

## Usage

```bash
cd python

# Interactive CLI
python main.py

# Benchmark all sorting algorithms
python benchmark.py
python benchmark.py --sizes 100 1000 5000
python benchmark.py --algo bubble merge quick heap
```

---

## Original Java — Course Work

The `java/` folder contains the original implementations written during the Algorithms course:

- **ADT** — `IntList` (custom singly linked list implementation)
- **BinaryTree** — BST with insert, inOrder/preOrder/postOrder traversals
- **BinarySearch** — Visual binary search with step-by-step console output
- **QuickSort** — Interactive quicksort with user input
- **FindMax** — Simple array maximum finder
- **Caesar Cipher** — Encrypt/decrypt/brute-force crack

---

## Author

**Aboubacar Sidick Meite** — [@ApollonIUGB77](https://github.com/ApollonIUGB77)

---

© 2026 Aboubacar Sidick Meite (ApollonIUGB77) — All Rights Reserved
