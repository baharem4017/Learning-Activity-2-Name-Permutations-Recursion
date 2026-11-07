"""Run beside name_permutations.py. Results: laptop_results.txt.
Measures generation only; input, name labeling and menu are excluded.
"""

import os
import platform
import statistics
import time
import tracemalloc
from contextlib import redirect_stdout
from name_permutations import print_permutations


def main():
    names = ["Bahareh", "Henrietta", "Sarah", "Patrick", "Zeyad", "Alex", "Morgan"]
    report = f"Python: {platform.python_version()}\nSystem: {platform.system()}\n\n"
    report += "People | Median time (ms) | Median peak memory (KiB)\n"

    for n in range(3, 8):
        group = names[:n]
        times = []
        memory = []

        # Measure time seven times. Do not display the permutations.
        for repeat in range(7):
            with open(os.devnull, "w") as output:
                with redirect_stdout(output):
                    start = time.perf_counter()
                    print_permutations([], group)
                    seconds = time.perf_counter() - start
            times.append(seconds * 1000)

        # Measure Python memory separately, five times.
        for repeat in range(5):
            with open(os.devnull, "w") as output:
                with redirect_stdout(output):
                    tracemalloc.start()
                    baseline = tracemalloc.get_traced_memory()[0]
                    print_permutations([], group)
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()
            memory.append((peak - baseline) / 1024)

        runtime = statistics.median(times)
        peak_memory = statistics.median(memory)
        row = f"{n} | {runtime:.3f} | {peak_memory:.1f}"
        print(row)
        report += row + "\n"
        report += f"Time samples (ms): {times}\nMemory samples (KiB): {memory}\n"

    report += "\nTime: median of 7 individual runs; time.perf_counter.\n"
    report += "Memory: median of 5 trials; peak traced Python allocation above baseline.\n"
    report += "1 KiB = 1024 bytes. This is not total RAM.\n"
    report += "Output: buffered text to os.devnull; screen display is excluded.\n"
    report += "File opening and closing are outside the measurements.\n"
    report += "Input, name labeling and menu are excluded. No timing during memory tracing.\n"
    with open("laptop_results.txt", "w", encoding="utf-8") as file:
        file.write(report)
    print("Done! Open laptop_results.txt in the working folder of your project.")


if __name__ == "__main__":
    main()
