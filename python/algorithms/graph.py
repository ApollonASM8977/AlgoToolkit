# © 2026 Aboubacar Sidick Meite (ApollonIUGB77) — All Rights Reserved
"""
Graph Algorithms — adjacency list representation with 5 classic algorithms.

Graph class supports both directed and undirected, weighted and unweighted graphs.

Algorithms:
  bfs(start)              — Breadth-First Search
  dfs(start)              — Depth-First Search
  dijkstra(start)         — Shortest paths (non-negative weights)
  bellman_ford(start)     — Shortest paths (handles negative weights, detects negative cycles)
  kruskal()               — Minimum Spanning Tree (undirected graphs)
"""

from __future__ import annotations
from collections import deque
from dataclasses import dataclass, field
from typing import Any, Optional
import heapq


# ── Graph ──────────────────────────────────────────────────────────────────────

class Graph:
    """
    Weighted directed/undirected graph using adjacency lists.

    Nodes can be any hashable value (int, str, etc.).
    Edge weights default to 1 if not specified.
    """

    def __init__(self, directed: bool = False) -> None:
        self.directed = directed
        self._adj: dict[Any, list[tuple[Any, float]]] = {}   # node → [(neighbor, weight)]

    # ── Construction ──────────────────────────────────────────────────────────

    def add_node(self, node: Any) -> None:
        if node not in self._adj:
            self._adj[node] = []

    def add_edge(self, u: Any, v: Any, weight: float = 1.0) -> None:
        self.add_node(u)
        self.add_node(v)
        self._adj[u].append((v, weight))
        if not self.directed:
            self._adj[v].append((u, weight))

    def remove_edge(self, u: Any, v: Any) -> None:
        self._adj[u] = [(n, w) for n, w in self._adj[u] if n != v]
        if not self.directed:
            self._adj[v] = [(n, w) for n, w in self._adj[v] if n != u]

    def neighbors(self, node: Any) -> list[tuple[Any, float]]:
        return self._adj.get(node, [])

    @property
    def nodes(self) -> list:
        return list(self._adj.keys())

    @property
    def edges(self) -> list[tuple]:
        result = []
        seen = set()
        for u, neighbors in self._adj.items():
            for v, w in neighbors:
                key = (min(u, v), max(u, v)) if not self.directed else (u, v)
                if key not in seen:
                    result.append((u, v, w))
                    seen.add(key)
        return result

    def __len__(self) -> int:
        return len(self._adj)

    def __repr__(self) -> str:
        d = "directed" if self.directed else "undirected"
        return f"Graph({d}, {len(self._adj)} nodes, {len(self.edges)} edges)"


# ── BFS ────────────────────────────────────────────────────────────────────────

@dataclass
class BFSResult:
    start:     Any
    visited:   list          # nodes in BFS order
    distances: dict          # node → distance from start (hops)
    parent:    dict          # node → parent in BFS tree
    steps:     list[dict]

    def path_to(self, target: Any) -> list:
        """Reconstruct shortest path (by hops) from start to target."""
        if target not in self.parent and target != self.start:
            return []
        path = []
        cur = target
        while cur is not None:
            path.append(cur)
            cur = self.parent.get(cur)
        return path[::-1]


def bfs(graph: Graph, start: Any, trace: bool = False) -> BFSResult:
    """
    Breadth-First Search — visits nodes level by level.
    Time: O(V + E) | Space: O(V)
    Returns: visited order, shortest path distances (hops), BFS tree.
    """
    visited_order: list  = []
    dist:   dict         = {start: 0}
    parent: dict         = {start: None}
    steps:  list[dict]   = []
    queue   = deque([start])
    visited = {start}

    while queue:
        node = queue.popleft()
        visited_order.append(node)
        if trace:
            steps.append({"visiting": node, "distance": dist[node], "queue": list(queue)})
        for neighbor, _ in graph.neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                dist[neighbor]   = dist[node] + 1
                parent[neighbor] = node
                queue.append(neighbor)

    return BFSResult(start, visited_order, dist, parent, steps)


# ── DFS ────────────────────────────────────────────────────────────────────────

@dataclass
class DFSResult:
    start:        Any
    visited:      list          # nodes in DFS order
    discovery:    dict          # node → discovery time
    finish:       dict          # node → finish time
    parent:       dict
    has_cycle:    bool
    steps:        list[dict]

    def path_to(self, target: Any) -> list:
        if target not in self.parent and target != self.start:
            return []
        path = []
        cur = target
        while cur is not None:
            path.append(cur)
            cur = self.parent.get(cur)
        return path[::-1]


def dfs(graph: Graph, start: Any, trace: bool = False) -> DFSResult:
    """
    Depth-First Search — explores as deep as possible before backtracking.
    Time: O(V + E) | Space: O(V)
    Also detects cycles.
    """
    visited_order: list = []
    discovery: dict     = {}
    finish:    dict     = {}
    parent:    dict     = {start: None}
    steps:     list     = []
    timer              = [0]
    in_stack           = set()
    cycle_found        = [False]
    visited            = set()

    def _dfs(node: Any) -> None:
        visited.add(node)
        in_stack.add(node)
        timer[0] += 1
        discovery[node] = timer[0]
        visited_order.append(node)
        if trace:
            steps.append({"event": "discover", "node": node, "time": timer[0]})

        for neighbor, _ in graph.neighbors(node):
            if neighbor not in visited:
                parent[neighbor] = node
                _dfs(neighbor)
            elif neighbor in in_stack:
                cycle_found[0] = True

        in_stack.discard(node)
        timer[0] += 1
        finish[node] = timer[0]
        if trace:
            steps.append({"event": "finish", "node": node, "time": timer[0]})

    _dfs(start)
    # Visit remaining unvisited nodes (disconnected graph)
    for node in graph.nodes:
        if node not in visited:
            parent.setdefault(node, None)
            _dfs(node)

    return DFSResult(start, visited_order, discovery, finish, parent, cycle_found[0], steps)


# ── Dijkstra ───────────────────────────────────────────────────────────────────

@dataclass
class DijkstraResult:
    start:     Any
    distances: dict          # node → shortest distance
    parent:    dict
    steps:     list[dict]

    def path_to(self, target: Any) -> list:
        if target not in self.distances or self.distances[target] == float("inf"):
            return []
        path = []
        cur = target
        while cur is not None:
            path.append(cur)
            cur = self.parent.get(cur)
        return path[::-1]

    def distance_to(self, target: Any) -> float:
        return self.distances.get(target, float("inf"))


def dijkstra(graph: Graph, start: Any, trace: bool = False) -> DijkstraResult:
    """
    Dijkstra's algorithm — single-source shortest paths for non-negative weights.
    Time: O((V + E) log V) with binary heap | Space: O(V)
    """
    INF = float("inf")
    dist   = {node: INF for node in graph.nodes}
    parent = {node: None for node in graph.nodes}
    dist[start] = 0
    steps: list[dict] = []

    # min-heap: (distance, node)
    heap = [(0, start)]

    while heap:
        d, u = heapq.heappop(heap)
        if d > dist[u]:
            continue   # stale entry
        if trace:
            steps.append({"relaxing": u, "dist": d})
        for v, weight in graph.neighbors(u):
            new_dist = dist[u] + weight
            if new_dist < dist[v]:
                dist[v]   = new_dist
                parent[v] = u
                heapq.heappush(heap, (new_dist, v))

    return DijkstraResult(start, dist, parent, steps)


# ── Bellman-Ford ───────────────────────────────────────────────────────────────

@dataclass
class BellmanFordResult:
    start:          Any
    distances:      dict
    parent:         dict
    negative_cycle: bool
    steps:          list[dict]

    def path_to(self, target: Any) -> list:
        if self.negative_cycle or self.distances.get(target) == float("inf"):
            return []
        path = []
        cur = target
        while cur is not None:
            path.append(cur)
            cur = self.parent.get(cur)
        return path[::-1]


def bellman_ford(graph: Graph, start: Any, trace: bool = False) -> BellmanFordResult:
    """
    Bellman-Ford algorithm — shortest paths allowing negative edge weights.
    Detects negative cycles.
    Time: O(V·E) | Space: O(V)
    """
    INF = float("inf")
    nodes = graph.nodes
    edges = graph.edges

    dist   = {n: INF for n in nodes}
    parent = {n: None for n in nodes}
    dist[start] = 0
    steps: list[dict] = []

    # Relax all edges V-1 times
    for iteration in range(len(nodes) - 1):
        updated = False
        for u, v, w in edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                dist[v]   = dist[u] + w
                parent[v] = u
                updated   = True
            # For undirected graphs
            if not graph.directed and dist[v] != INF and dist[v] + w < dist[u]:
                dist[u]   = dist[v] + w
                parent[u] = v
                updated   = True
        if trace:
            steps.append({"iteration": iteration + 1, "distances": dict(dist)})
        if not updated:
            break   # Early exit

    # Check for negative cycles
    negative_cycle = False
    for u, v, w in edges:
        if dist[u] != INF and dist[u] + w < dist[v]:
            negative_cycle = True
            break

    return BellmanFordResult(start, dist, parent, negative_cycle, steps)


# ── Kruskal's MST ──────────────────────────────────────────────────────────────

@dataclass
class KruskalResult:
    mst_edges:   list[tuple]   # (u, v, weight) sorted by weight
    total_weight: float
    steps:       list[dict]


class _UnionFind:
    def __init__(self, nodes):
        self.parent = {n: n for n in nodes}
        self.rank   = {n: 0  for n in nodes}

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])   # path compression
        return self.parent[x]

    def union(self, x, y) -> bool:
        rx, ry = self.find(x), self.find(y)
        if rx == ry:
            return False   # same component → would form cycle
        if self.rank[rx] < self.rank[ry]:
            rx, ry = ry, rx
        self.parent[ry] = rx
        if self.rank[rx] == self.rank[ry]:
            self.rank[rx] += 1
        return True


def kruskal(graph: Graph, trace: bool = False) -> KruskalResult:
    """
    Kruskal's MST — greedily adds the cheapest edge that doesn't form a cycle.
    Uses Union-Find (path compression + union by rank).
    Time: O(E log E) | Space: O(V)
    Only valid for undirected graphs.
    """
    edges = sorted(graph.edges, key=lambda e: e[2])
    uf    = _UnionFind(graph.nodes)
    mst: list[tuple] = []
    total = 0.0
    steps: list[dict] = []

    for u, v, w in edges:
        if uf.union(u, v):
            mst.append((u, v, w))
            total += w
            if trace:
                steps.append({"added_edge": (u, v, w), "mst_so_far": list(mst)})
            if len(mst) == len(graph.nodes) - 1:
                break   # MST complete

    return KruskalResult(mst, total, steps)
