# © 2026 Aboubacar Sidick Meite (ApollonIUGB77) — All Rights Reserved
"""
Benchmark — compare all sorting algorithms on random, sorted, and reverse-sorted data.
Measures wall-clock time, comparisons, and swaps.

Usage:
  python benchmark.py                  # default sizes
  python benchmark.py --sizes 100 1000 5000
  python benchmark.py --algo bubble merge quick
"""

from __future__ import annotations
import argparse
import random
import time

from algorithms.sorting import ALL_SORTS


# ── Config ─────────────────────────────────────────────────────────────────────

DEFAULT_SIZES = [100, 500, 1000, 5000]
INTEGER_ONLY  = {"counting", "radix"}    # algorithms that require integers

COL_WIDTH = 14


# ── Helpers ────────────────────────────────────────────────────────────────────

def _generate(size: int, kind: str) -> list[int]:
    if kind == "random":
        return [random.randint(0, size * 10) for _ in range(size)]
    elif kind == "sorted":
        return list(range(size))
    elif kind == "reverse":
        return list(range(size, 0, -1))
    elif kind == "nearly":
        arr = list(range(size))
        # swap ~5% of elements
        for _ in range(max(1, size // 20)):
            i, j = random.randrange(size), random.randrange(size)
            arr[i], arr[j] = arr[j], arr[i]
        return arr
    raise ValueError(f"unknown kind: {kind}")


def _hr(char: str = "─", width: int = 90) -> str:
    return char * width


def _fmt_time(seconds: float) -> str:
    if seconds < 0.001:
        return f"{seconds * 1_000_000:.1f} µs"
    elif seconds < 1:
        return f"{seconds * 1000:.2f} ms"
    return f"{seconds:.3f} s"


# ── Runner ─────────────────────────────────────────────────────────────────────

def run_benchmark(sizes: list[int], algo_names: list[str]) -> None:
    kinds = ["random", "sorted", "reverse", "nearly"]

    for size in sizes:
        print(f"\n{_hr('═')}")
        print(f"  ARRAY SIZE: {size:,}")
        print(_hr("═"))

        # Header
        header = f"{'Algorithm':<18}"
        for kind in kinds:
            header += f" {kind.capitalize():>{COL_WIDTH}}"
        print(header)
        print(_hr())

        for name in algo_names:
            fn   = ALL_SORTS[name]
            row  = f"{name.replace('_', ' ').title():<18}"

            for kind in kinds:
                arr = _generate(size, kind)
                # Integer-only algos need non-negative integers — already fine
                start = time.perf_counter()
                result = fn(arr, trace=False)
                elapsed = time.perf_counter() - start

                cell = _fmt_time(elapsed)
                row += f" {cell:>{COL_WIDTH}}"

            print(row)

        print(_hr())

    # ── Complexity summary ────────────────────────────────────────────────────
    print(f"\n{_hr('═')}")
    print("  COMPLEXITY SUMMARY")
    print(_hr("═"))
    hdr = f"{'Algorithm':<18} {'Best':>12} {'Average':>14} {'Worst':>14} {'Space':>10} {'Stable':>8}"
    print(hdr)
    print(_hr())

    STABLE = {"bubble", "insertion", "merge", "counting", "radix"}

    for name, fn in ALL_SORTS.items():
        if name not in algo_names:
            continue
        # Run on small array just to get complexity metadata
        dummy = fn([5, 3, 1, 4, 2], trace=False)
        c = dummy.complexity
        stable = "✓" if name in STABLE else "✗"
        print(f"{name.replace('_',' ').title():<18} {c['best']:>12} {c['average']:>14} {c['worst']:>14} {c['space']:>10} {stable:>8}")

    print(_hr())


# ── CLI ────────────────────────────────────────────────────────────────────────

def main() -> None:
    parser = argparse.ArgumentParser(description="Sorting algorithm benchmark")
    parser.add_argument(
        "--sizes", nargs="+", type=int, default=DEFAULT_SIZES,
        help="Array sizes to test (default: 100 500 1000 5000)"
    )
    parser.add_argument(
        "--algo", nargs="+", choices=list(ALL_SORTS.keys()),
        default=list(ALL_SORTS.keys()),
        help="Algorithms to include"
    )
    args = parser.parse_args()

    print("\n" + "═" * 90)
    print("  ALGO TOOLKIT — Sorting Benchmark")
    print("  © 2026 Aboubacar Sidick Meite (ApollonIUGB77)")
    print("═" * 90)

    run_benchmark(args.sizes, args.algo)


if __name__ == "__main__":
    main()
