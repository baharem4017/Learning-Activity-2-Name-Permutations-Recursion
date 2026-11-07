# Learning Activity 2: All Permutations of Names

**Author:** Bahareh Mohamadtaheri  
**Course:** DATA/CS 5010 — Introduction to Data Science Programming  
**University:** Bowling Green State University

## Overview

This individual project uses Python recursion to generate every possible lineup of a group of people. Each ordering contains every person once and is printed on a separate line, with names separated by a comma and a space.

The program completes each branch before exploring the next choice, preserving the original input choice order.

The assignment specifies a list of one-word names. This version adds interactive person-count entry and allows one complete name per line. Prompts and the `Permutations:` heading are part of the console interface; the ordering lines use the required comma-separated format.

## Files

| File | Purpose |
| --- | --- |
| `name_permutations.py` | Interactive input and recursive permutation generation |
| `README.md` | Project description, execution instructions, and behavior |

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

New lists keep each caller's state separate, so no shared-list changes need to be undone. The permutation engine uses recursive calls without `for` or `while` loops. Input collection and validation use loops.

## Input policies and error handling

These are implementation choices for the interactive version:

| Situation | Behavior |
| --- | --- |
| Invalid person count, such as `0`, `-1`, or `abc` | Ask again for a positive whole number |
| Blank or whitespace-only name | Ask again for the same person's name |
| Leading, trailing, or repeated whitespace | Remove outer whitespace and use one space between words |
| Multiword name | Keep the complete entered name as one list element |
| One person | Print that person's name once |
| Repeated names | Accept each occurrence as a separate person; repeated output lines are allowed |
| End of input (`EOFError`), including at the menu | Print `Input ended. Goodbye!` and stop |
| Ctrl+C (`KeyboardInterrupt`), including at the menu | Print `Cancelled. Goodbye!` and stop |

Capitalization is preserved. The simplified implementation accepts any nonempty name text; it does not enforce English-only names or detailed character restrictions.

Repeated labels are not removed or renamed. For example, Patrick, Patrick, and Sarah produce six positional orderings but only three different output strings.

If generation is interrupted, previously printed lines remain in the terminal.

## Output growth and limitations

For `n` distinct names, there are `n!` distinct orderings:

| Number of distinct names | Orderings |
| ---: | ---: |
| 1 | 1 |
| 3 | 6 |
| 5 | 120 |
| 7 | 5,040 |

These are mathematical counts, not measured runtimes. With repeated names, the program still prints `n!` positional orderings, but some output strings repeat.

The program prints results as they are generated instead of storing every permutation. Recursive helper calls and new list copies still consume memory.

There is no explicit maximum person count. Factorial output growth quickly makes large inputs impractical, and large runs can exceed Python's recursion or resource limits. The program handles the listed input problems and interruptions; it does not catch every possible failure.

## Manual verification

Suggested checks for the current implementation:

1. Run the three-person example and compare all six lines, including their order and comma spacing.
2. Enter one person, such as Zeyad, and confirm that one ordering prints.
3. Enter an invalid count and a blank name; confirm that the relevant prompt repeats.
4. Enter a multiword name and confirm that it remains one person's name.
5. Enter Patrick, Patrick, and Sarah; confirm that six lines print, including repeated strings.
6. After the permutations, enter `1` and confirm that the program asks for a new count and new names.
7. Enter an invalid menu answer, such as `maybe` or a blank answer; confirm that the menu prompt repeats without regenerating the previous output.
8. Check that `yes` and `y` continue, and that `no` and `n` exit; also try uppercase answers and surrounding spaces.
9. Enter `2` after a group and confirm that the goodbye message prints and the program stops.
10. Check EOF handling and Ctrl+C in the terminal, including at the continue-or-exit prompt.
