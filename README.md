# Learning Activity 2: All Permutations of Names

**Author:** Bahareh Mohamadtaheri  
**Course:** DATA 5010 — Introduction to Data Science Programming  
**University:** Bowling Green State University

## Overview

This individual project uses Python recursion to generate every possible lineup of a group of people. Each ordering contains every person once and is printed on a separate line, with names separated by a comma and a space.

The program completes each branch before exploring the next choice, preserving the original input choice order.

The assignment specifies a list of one-word names. This version adds interactive person-count entry and allows one complete name per line. Prompts and the `Permutations:` heading are part of the console interface; the ordering lines use the required comma-separated format.

## Files

| File | Purpose |
| --- | --- |
| `name_permutations.py` | Interactive input and recursive permutation generation using the nested helper |
| `benchmark_runtime_memory.py` | Measure the main implementation with 3 through 7 distinct names |
| `compare_permutation_runtime_memory.py` | Compare the recursive helper, `for + recursion`, and `while + recursion` with 7 distinct names |
| `runtime_memory_results.txt` | Saved laptop results for the 3–7-person measurements |
| `permutation_comparison_results.txt` | Laptop results for the three-version comparison |
| `README.md` | Project description, execution instructions, behavior, and measurement methods |

## Requirements and execution

Python 3 is required. No external packages are needed.

Save `name_permutations.py` in a folder, open a terminal in that folder, and run:

```bash
python name_permutations.py
```

If your system uses the `python3` command, run:

```bash
python3 name_permutations.py
```

Enter a positive whole number of people, then enter each person's name on a separate line. After displaying the permutations, choose whether to enter a new group or exit. You can process several groups in one run.

## Example session

The following session generates permutations for three classmates, starts a new group with one person, and then exits:

```text
Welcome to the Name Permutations Program!
Number of people: 3
Person 1: Bahareh
Person 2: Henrietta
Person 3: Sarah

Permutations:
Bahareh, Henrietta, Sarah
Bahareh, Sarah, Henrietta
Henrietta, Bahareh, Sarah
Henrietta, Sarah, Bahareh
Sarah, Bahareh, Henrietta
Sarah, Henrietta, Bahareh

Would you like to enter another group?
1. Yes - enter a new number of people and names
2. No - exit
Choose 1 or 2 (or yes/no): 1

--- New Group ---
Number of people: 1
Person 1: Zeyad

Permutations:
Zeyad

Would you like to enter another group?
1. Yes - enter a new number of people and names
2. No - exit
Choose 1 or 2 (or yes/no): 2

Goodbye! Thank you for using the program.
```

For the five-person demonstration, enter `5`, followed by Bahareh, Henrietta, Sarah, Patrick, and Zeyad on separate lines. These five distinct names produce 120 orderings.

## Continue or exit menu

After each group, `ask_to_continue()` displays a menu:

| Accepted answer | Action |
| --- | --- |
| `1`, `yes`, or `y` | Start a new group and ask for the number of people and all names again |
| `2`, `no`, or `n` | Print `Goodbye! Thank you for using the program.` and exit |
| Any other answer, including a blank answer | Display an error and ask for a valid menu choice again |

Menu answers are case-insensitive, and leading or trailing whitespace is ignored. For example, `YES` and ` yes ` both start another group.

Each new group starts with a fresh name list. `main()` repeats the input and generation steps until the user chooses to exit. The menu and input loops are separate from the recursive permutation engine.

## How the recursion works

The function `print_permutations(chosen, remaining)` uses two lists:

- `chosen`: names already selected for the current ordering.
- `remaining`: names still available for selection.

The initial call is `print_permutations([], nameList)`.

### Main Base Case

When `remaining` is empty, one complete ordering is ready. The function prints `chosen` using `", ".join(chosen)` and returns.

Returning ends that branch. Earlier calls can then continue exploring other choices.

### Recursive Step

The nested helper `try_choice(i)` selects `remaining[i]`, creates new lists, and calls `print_permutations()` for that branch. After the branch returns, `try_choice(i + 1)` explores the next available choice.

The helper stops when `i == len(remaining)`, meaning all choices at the current level have been tried.

New lists keep each caller's state separate, so no shared-list changes need to be undone. The permutation engine uses recursive calls without `for` or `while` loops. Input collection, validation, duplicate-name labeling, and the menu use loops outside the permutation engine.

## Input policies and error handling

These are implementation choices for the interactive version:

| Situation | Behavior |
| --- | --- |
| Invalid person count, such as `0`, `-1`, `3.5`, or `abc` | Ask again for a positive whole number; there is no explicit maximum count |
| Blank or whitespace-only name | Ask again for the same person's name |
| Name longer than 30 characters (after whitespace normalization) | Show a length error and ask again |
| Digits, emojis, commas, brackets, or other invalid symbols in a name | Reject the name and ask again |
| Valid name characters | English letters (A-Z, a-z), spaces between words, and hyphens or apostrophes placed between English letters |
| Leading, trailing, or repeated whitespace | Remove outer whitespace and use one space between words |
| Multiword name | Keep the complete entered name as one list element |
| One person | Print that person's name once |
| Repeated names | Accept each occurrence as a separate person and assign fixed numbered labels, including the first occurrence |
| End of input (`EOFError`), including at the menu | Print `Input ended. Goodbye!` and stop |
| Ctrl+C (`KeyboardInterrupt`), including at the menu | Print `Cancelled. Goodbye!` and stop |
| Python recursion-depth limit (`RecursionError`) during generation | Print `Python recursion limit reached. Try a smaller group. Goodbye!` and stop |

Capitalization is preserved. Names must use English letters only, with optional spaces between words and internal hyphens or apostrophes (examples: `Mary Jane`, `Anne-Marie`, and `O'Connor`). Numbers, emojis, commas, brackets, and other symbols are rejected. Input whitespace is normalized before the 30-character limit is checked. Invalid names are requested again for the same person.

### Numbering repeated names

After all names have been entered, `number_duplicate_names(nameList)` assigns labels before permutation generation. Only repeated names receive a number, including the first occurrence. For example, `Ali`, `Ali`, and `Sara` become `Ali [1]`, `Ali [2]`, and `Sara`.

For comparison, the helper uses `lower()` to convert names to lowercase after whitespace normalization, so `Ali` and `ali` are treated as repeated names. It uses ordinary lists, `count()`, `append()`, and loops to find duplicates and choose available numbers. Each person's entered capitalization is preserved. Unique names stay unchanged. Numbers follow input order and stay with the same person in every permutation; they do not indicate a person's current position in the lineup. Numbering starts fresh for each new group.

The interactive input rules do not allow brackets or digits in entered names, so a user cannot type a pre-numbered label such as `Ali [1]`. Bracketed numbers are added automatically by `number_duplicate_names()` only after valid names have been entered.

Example session with repeated names:

```text
Welcome to the Name Permutations Program!
Number of people: 3
Person 1: Ali
Person 2: Ali
Person 3: Sara

Permutations:
Ali [1], Ali [2], Sara
Ali [1], Sara, Ali [2]
Ali [2], Ali [1], Sara
Ali [2], Sara, Ali [1]
Sara, Ali [1], Ali [2]
Sara, Ali [2], Ali [1]

Would you like to enter another group?
1. Yes - enter a new number of people and names
2. No - exit
Choose 1 or 2 (or yes/no): 2

Goodbye! Thank you for using the program.
```

If generation is interrupted, previously printed lines remain in the terminal.

## Output growth and limitations

For `n` distinct names, there are `n!` distinct orderings:

| Number of distinct names | Orderings |
| ---: | ---: |
| 1 | 1 |
| 3 | 6 |
| 5 | 120 |
| 7 | 5,040 |

These are mathematical counts, not measured runtimes. With repeated names, fixed numbered labels distinguish the people, so the program still prints `n!` distinct labeled orderings.

The program prints results as they are generated instead of storing every permutation. Recursive helper calls and new list copies still consume memory.

There is no explicit maximum person count. Factorial output growth quickly makes large inputs impractical, and large runs can exceed Python's recursion or resource limits. The program handles the listed input problems, interruptions, and `RecursionError`; it does not catch every possible failure.

## Performance measurements

The two measurement scripts are separate from the interactive program. Keep all three `.py` files in the same folder. They use Python's standard library and require no additional packages. Importing `name_permutations.py` does not start its interactive menu.

Run the commands below from the project folder. If needed, use `python3` instead of `python`.

### 1. Measure the main implementation for different group sizes

```bash
python benchmark_runtime_memory.py
```

This script imports the main `print_permutations()` function and measures it with 3, 4, 5, 6, and 7 distinct names. It prints the median results and writes `runtime_memory_results.txt` in the current working folder. The generated report also records Python version, operating system, seven individual time samples and five memory samples for each group size, plus measurement notes. A new run replaces that output file.

Reported laptop measurements from the saved results file:

| People (n) | Orderings (n!) | Median runtime (ms) | Median peak traced allocation above baseline (KiB) |
| ---: | ---: | ---: | ---: |
| 3 | 6 | 0.004 | 5.3 |
| 4 | 24 | 0.018 | 19.5 |
| 5 | 120 | 0.171 | 88.5 |
| 6 | 720 | 0.780 | 163.7 |
| 7 | 5,040 | 5.645 | 194.7 |

The ordering counts are mathematical values. Runtime and allocation are measurements.

### 2. Compare three implementations

```bash
python compare_permutation_runtime_memory.py
```

This script uses the same seven distinct names for every version: Bahareh, Henrietta, Sarah, Patrick, Zeyad, Alex, and Morgan. Each version produces 5,040 orderings.

- **Recursive helper:** imports the main program's `print_permutations()` function, which uses the nested `try_choice(i)` helper.
- **for + recursion:** uses a `for` loop to explore the choices at each level, then makes recursive calls for the branches.
- **while + recursion:** uses a `while` loop to explore the choices at each level, then makes recursive calls for the branches.

All three versions use recursion for permutation generation and create new lists for each branch. The alternative versions are inside the comparison script. They do not replace the main program's loop-free permutation engine.

The script prints its report and writes `permutation_comparison_results.txt` in the current working folder. A new run replaces that output file.

Reported laptop measurements from `permutation_comparison_results.txt`:

| Version | Median runtime (ms) | Median peak traced allocation above baseline (KiB) |
| --- | ---: | ---: |
| Recursive helper | 5.548 | 223.9 |
| for + recursion | 2.319 | 26.1 |
| while + recursion | 2.357 | 25.8 |

In this experiment, both loop versions had lower median runtime and traced allocation than the helper version. The `for` and `while` times are close. These reported medians do not establish a consistent winner between them.

### Measurement method and interpretation

Both reports identify Python 3.14.7 on Darwin (macOS). The scripts record the Python version and operating system each time they run. Results can change on another computer or between runs.

Both scripts use:

- `time.perf_counter()` for runtime, reported in milliseconds as the median of seven individual runs.
- `tracemalloc` for memory, reported as the median of five peak traced Python allocations above the pre-call baseline.
- Separate time and memory measurements, so memory tracing does not run during timing.
- Buffered output to `os.devnull`, which discards the ordering text and excludes terminal display.

Stream opening and closing are outside the measurements. Forming and printing the ordering text are inside the measured function call. Interactive input, duplicate labeling, and the menu are excluded. One KiB equals 1,024 bytes. Traced allocation is not total process RAM.

The comparison script calls `gc.collect()` before every run, outside measurement, and resets the traced peak after recording the baseline. The group-size script does not explicitly perform those cleanup steps. Treat their results as separate experiments, including their different reported helper-memory values.

These scripts measure individual runs, not batch means. The comparison report contains medians but does not include the raw trial values, so it does not support claims about overlapping timing ranges. The group-size report includes its seven time samples and five memory samples for each group size.


## Manual verification

Suggested checks for the current implementation:

1. Run the three-person example and compare all six lines, including their order and comma spacing.
2. Enter one person, such as Zeyad, and confirm that one ordering prints.
3. Enter an invalid count and a blank name; confirm that the relevant prompt repeats.
4. Enter a multiword name and confirm that it remains one person's name.
5. Enter Patrick, Patrick, and Sarah; confirm that six distinct lines print using `Patrick [1]`, `Patrick [2]`, and `Sarah`. Check that each label stays with the same person throughout the output.
6. After the permutations, enter `1` and confirm that the program asks for a new count and new names.
7. Enter an invalid menu answer, such as `maybe` or a blank answer; confirm that the menu prompt repeats without regenerating the previous output.
8. Check that `yes` and `y` continue, and that `no` and `n` exit; also try uppercase answers and surrounding spaces.
9. Enter `2` after a group and confirm that the goodbye message prints and the program stops.
10. Check EOF handling and Ctrl+C in the terminal, including at the continue-or-exit prompt.
11. Enter `Ali` and `ali`; confirm that `Ali [1]` and `ali [2]` appear.
12. Enter `123`, `John123`, an emoji, `John!`, or `Ali [1]` as a name; confirm that each is rejected and the same person is prompted again.
13. Enter a name longer than 30 characters; confirm that it is rejected, then enter exactly 30 valid letters and confirm acceptance.
14. Try valid names such as `Mary Jane`, `Anne-Marie`, and `O'Connor`; confirm that each is accepted. Try `-Ali`, `Ali-`, or `Ali--Sara`; confirm that invalid hyphen placement is rejected.
15. Enter names with extra spaces and confirm they are normalized.
16. Start another group with repeated names and confirm that numbering starts fresh.
17. If checking recursion-depth handling, use a controlled test or simulated `RecursionError` rather than printing an impractically large number of permutations.
