"""Measure permutation runtime and memory for 3 to 7 people."""

import os
import time
import statistics
import tracemalloc
from contextlib import redirect_stdout
from name_permutations import print_permutations


def main():
    names = ["Bahareh", "Henrietta", "Sarah", "Patrick", "Zeyad", "Alex", "Morgan"]
    results = "People | Time (ms) | Memory (KiB)\n"

    for n in range(3, 8):
        group = names[:n]
        times = []
        memories = []

        # Hide the printed lineups while we measure performance.
        with open(os.devnull, "w") as output:
            with redirect_stdout(output):
                # Repeat timing 7 times.
                for i in range(7):
                    start = time.perf_counter()
                    print_permutations([], group)
                    times.append((time.perf_counter() - start) * 1000)

                # Repeat memory measurement 5 times, separately.
                for i in range(5):
                    tracemalloc.start()
                    before = tracemalloc.get_traced_memory()[0]
                    print_permutations([], group)
                    peak = tracemalloc.get_traced_memory()[1]
                    tracemalloc.stop()
                    memories.append((peak - before) / 1024)

        time_ms = statistics.median(times)
        memory_kib = statistics.median(memories)
        line = f"{n} | {time_ms:.3f} | {memory_kib:.1f}"
        print(line)
        results += line + "\n"

    results += "\nTime: median of 7 runs, in milliseconds.\n"
    results += "Memory: median of 5 trials, peak traced allocation above baseline in KiB.\n"
    results += "Generation only; input, labels, menu, and screen output excluded.\n"

    with open("runtime_memory_results.txt", "w", encoding="utf-8") as file:
        file.write(results)

    print("Results saved to runtime_memory_results.txt")


if __name__ == "__main__":
    main()
