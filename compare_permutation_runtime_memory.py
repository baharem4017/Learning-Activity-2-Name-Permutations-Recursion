"""Run beside name_permutations.py to compare three permutation versions.

Uses only Python's standard library. Measures seven distinct names.
Time: median of seven individual runs. Memory: median of five trials.
This simpler method differs from the old slide's batch timing method.
"""

import gc
import os
import platform
import statistics
import time
import tracemalloc
from contextlib import redirect_stdout
from name_permutations import print_permutations


def permutations_for(chosen, remaining):
    if not remaining:
        print(", ".join(chosen))
        return

    for i in range(len(remaining)):
        new_chosen = chosen + [remaining[i]]
        new_remaining = remaining[:i] + remaining[i + 1:]
        permutations_for(new_chosen, new_remaining)


def permutations_while(chosen, remaining):
    if not remaining:
        print(", ".join(chosen))
        return

    i = 0
    while i < len(remaining):
        new_chosen = chosen + [remaining[i]]
        new_remaining = remaining[:i] + remaining[i + 1:]
        permutations_while(new_chosen, new_remaining)
        i += 1


def measure(label, function):
    names = ["Bahareh", "Henrietta", "Sarah", "Patrick", "Zeyad", "Alex", "Morgan"]
    times = []
    memory = []

    # Measure time without displaying the 5,040 output lines.
    for repeat in range(7):
        gc.collect()  # Clean up earlier runs before starting the measurement.
        with open(os.devnull, "w") as output:
            with redirect_stdout(output):
                start = time.perf_counter()
                function([], names)
                seconds = time.perf_counter() - start
        times.append(seconds * 1000)

    # Measure memory separately, with no timer running.
    for repeat in range(5):
        gc.collect()
        with open(os.devnull, "w") as output:
            with redirect_stdout(output):
                tracemalloc.start()
                try:
                    baseline = tracemalloc.get_traced_memory()[0]
                    tracemalloc.reset_peak()
                    function([], names)
                    current, peak = tracemalloc.get_traced_memory()
                finally:
                    tracemalloc.stop()
        memory.append((peak - baseline) / 1024)

    runtime = statistics.median(times)
    peak_memory = statistics.median(memory)
    return f"{label} | {runtime:.3f} | {peak_memory:.1f}\n"


def main():
    report = f"Python: {platform.python_version()}\nSystem: {platform.system()}\n\n"
    report += "Input: 7 distinct names, producing 5,040 orderings\n"
    report += "Version | Median runtime (ms) | Median peak allocation (KiB)\n"
    report += measure("Recursive helper", print_permutations)
    report += measure("for + recursion", permutations_for)
    report += measure("while + recursion", permutations_while)
    report += "\nRuntime: median of 7 individual runs using time.perf_counter.\n"
    report += "Memory: median of 5 trials using tracemalloc, above baseline.\n"
    report += "Garbage collection occurs before each run, outside measurement.\n"
    report += "Output goes to a buffered null stream. Terminal display is excluded.\n"
    report += "Opening and closing the stream are outside measurement.\n"
    report += "Input, duplicate labeling and menu are excluded.\n"
    report += "1 KiB = 1,024 bytes. Traced allocations are not total process RAM.\n"
    report += "This method uses individual runs, not the old slide's batch means.\n"
    report += "Small timing differences can change between runs.\n"

    print(report)
    with open("permutation_comparison_results.txt", "w", encoding="utf-8") as file:
        file.write(report)


if __name__ == "__main__":
    main()
