"""Measure runtime and memory for 3 to 7 names, and save the results."""

import os
import platform
import statistics
import time
import tracemalloc
from contextlib import redirect_stdout
from name_permutations import print_permutations


def main():
    names = ["Bahareh", "Henrietta", "Sarah", "Patrick", "Zeyad", "Alex", "Morgan"]
    results = f"Python: {platform.python_version()}\nSystem: {platform.system()}\n\n"
    results += "People | Median time (ms) | Median peak memory (KiB)\n"

    for n in range(3, 8):
        group = names[:n]
        times = []
        memories = []

        # Measure execution time seven times without showing the lineups.
        for i in range(7):
            with open(os.devnull, "w") as output:
                with redirect_stdout(output):
                    start = time.perf_counter()
                    print_permutations([], group)
                    seconds = time.perf_counter() - start
            times.append(seconds * 1000)

        # Measure memory five times (separately from timing).
        for i in range(5):
            with open(os.devnull, "w") as output:
                with redirect_stdout(output):
                    tracemalloc.start()
                    before = tracemalloc.get_traced_memory()[0]
                    print_permutations([], group)
                    peak = tracemalloc.get_traced_memory()[1]
                    tracemalloc.stop()
            memories.append((peak - before) / 1024)

        median_time = statistics.median(times)
        median_memory = statistics.median(memories)
        line = f"{n} | {median_time:.3f} | {median_memory:.1f}"
        print(line)
        results += line + "\n"
        results += f"Time samples (ms): {times}\n"
        results += f"Memory samples (KiB): {memories}\n"

    results += "\nTime: median of 7 individual runs; time.perf_counter.\n"
    results += "Memory: median of 5 trials; peak traced Python allocation above baseline.\n"
    results += "1 KiB = 1024 bytes. This is not total RAM.\n"
    results += "Output: buffered text to os.devnull; screen display is excluded.\n"
    results += "File opening and closing are outside the measurements.\n"
    results += "Input, name labeling and menu are excluded. No timing during memory tracing.\n"

    with open("runtime_memory_results.txt", "w", encoding="utf-8") as file:
        file.write(results)

    print("Done! Open runtime_memory_results.txt in the working folder of your project.")


if __name__ == "__main__":
    main()
