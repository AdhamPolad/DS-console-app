"""Small helpers shared by the benchmarks."""
import time


def measure(fn, reps):
    """Return average time of fn() in microseconds."""
    start = time.perf_counter()
    for _ in range(reps):
        fn()
    return (time.perf_counter() - start) / reps * 1e6


def print_table(title, sizes, results):
    """results: {operation: {structure: [time per size]}}"""
    print("\n" + "=" * 70)
    print(title)
    print("=" * 70)
    for op, structs in results.items():
        print(f"\n-- {op} (avg microseconds per operation) --")
        print(f"{'Structure':<18}" + "".join(f"n={n:<12}" for n in sizes))
        for name, times in structs.items():
            print(f"{name:<18}" + "".join(f"{t:<14.2f}" for t in times))


def ask_int(prompt):
    try:
        return int(input(prompt))
    except ValueError:
        print("Please enter a number.")
        return None
