"""Name permutations: an interactive version of DATA/CS 5010 Q1.

Run: python name_permutations.py
Enter a positive number of people, one nonempty name or full name per line.
Repeated names represent different people, so repeated output lines are valid.
The permutation engine uses recursion without for/while loops.
After each group, choose whether to enter another group or exit.
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


def ask_to_continue():
    """Return True for another group or False to exit."""
    print("\nWould you like to enter another group?")
    print("1. Yes - enter a new number of people and names")
    print("2. No - exit")

    while True:
        choice = input("Choose 1 or 2 (or yes/no): ").strip().lower()

        if choice in ("1", "yes", "y"):
            return True
        if choice in ("2", "no", "n"):
            return False

        print("Invalid choice. Please enter 1 (yes) or 2 (no).")


def main():
    """Generate permutations for each group until the user chooses to exit."""
    print("Welcome to the Name Permutations Program!")

    try:
        while True:
            count = read_person_count()
            nameList = read_names(count)
            print("\nPermutations:")
            print_permutations([], nameList)

            if not ask_to_continue():
                print("\nGoodbye! Thank you for using the program.")
                break

            print("\n--- New Group ---")
    except EOFError:
        print("\nInput ended. Goodbye!")
    except KeyboardInterrupt:
        print("\nCancelled. Goodbye!")


if __name__ == "__main__":
    main()
