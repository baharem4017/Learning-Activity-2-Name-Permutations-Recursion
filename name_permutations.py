"""Name permutations: a simple interactive version of DATA/CS 5010 Q1.

Run: python name_permutations.py
Enter a positive number of people, one nonempty name or full name per line.
Repeated names represent different people, so repeated output lines are valid.
The permutation engine uses recursion without for/while loops.
"""

def read_person_count():
    """Ask for a positive integer, without an explicit upper limit."""
    while True:
        try:
            count = int(input("Number of people: "))
        except ValueError:
            print("Please enter a positive whole number.")
            continue

        if count >= 1:
            return count
        print("Please enter a number greater than zero.")


def read_names(count):
    """Read each person's name, retrying only when the name is empty."""
    nameList = []
    for number in range(1, count + 1):
        while True:
            raw = input(f"Person {number}: ")
            # Trim outer whitespace and use one space between words.
            name = " ".join(raw.split())

            if name:
                nameList.append(name)
                break
            print("Name cannot be empty. Please try again.")
    return nameList


def print_permutations(chosen, remaining):
    """Print all positional permutations in the original choice order."""
    # Base case: this ordering is complete.
    if not remaining:
        print(", ".join(chosen))
        return

    def try_choice(i):
        # Helper base case: all choices at this level have been tried.
        if i == len(remaining):
            return

        new_chosen = chosen + [remaining[i]]
        new_remaining = remaining[:i] + remaining[i + 1:]

        # Complete this branch before moving to the next choice.
        print_permutations(new_chosen, new_remaining)
        try_choice(i + 1)

    try_choice(0)


def main():
    """Read one group and print its permutations."""
    try:
        count = read_person_count()
        nameList = read_names(count)
        print("\nPermutations:")
        print_permutations([], nameList)
    except EOFError:
        print("\nInput ended. Exiting.")
    except KeyboardInterrupt:
        print("\nCancelled.")


if __name__ == "__main__":
    main()

