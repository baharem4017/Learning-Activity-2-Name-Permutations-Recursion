"""Generate all name orderings using recursion.

Run: python name_permutations.py
Enter a positive number of people and one name per person.
"""

MAX_NAME_LENGTH = 30


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


def is_valid_name(name):
    """Allow English letters, spaces, and internal hyphens/apostrophes."""
    if not name or len(name) > MAX_NAME_LENGTH:
        return False

    for i in range(len(name)):
        char = name[i]
        is_letter = ("A" <= char <= "Z") or ("a" <= char <= "z")

        if is_letter:
            continue

        if char == " ":
            # A space must separate two letters.
            if i == 0 or i == len(name) - 1:
                return False
            previous = name[i - 1]
            following = name[i + 1]
            previous_ok = ("A" <= previous <= "Z") or ("a" <= previous <= "z")
            following_ok = ("A" <= following <= "Z") or ("a" <= following <= "z")
            if not previous_ok or not following_ok:
                return False
            continue

        if char == "-" or char == "'":
            # Hyphens/apostrophes must be between English letters.
            if i == 0 or i == len(name) - 1:
                return False
            previous = name[i - 1]
            following = name[i + 1]
            previous_ok = ("A" <= previous <= "Z") or ("a" <= previous <= "z")
            following_ok = ("A" <= following <= "Z") or ("a" <= following <= "z")
            if not previous_ok or not following_ok:
                return False
            continue

        return False

    return True


def read_names(count):
    """Ask again if a name is empty or invalid."""
    nameList = []
    for number in range(1, count + 1):
        while True:
            raw = input(f"Person {number}: ")
            name = " ".join(raw.split())

            if not name:
                print("Name cannot be empty. Please try again.")
            elif len(name) > MAX_NAME_LENGTH:
                print(f"Name is too long (maximum {MAX_NAME_LENGTH} characters).")
            elif not is_valid_name(name):
                print("Use English letters only. Spaces, internal hyphens (-), and apostrophes (') are allowed; no numbers or other symbols.")
            else:
                nameList.append(name)
                break
    return nameList


def number_duplicate_names(nameList):
    """Number repeated names, ignoring differences in capitalization."""
    lower_names = []
    for name in nameList:
        lower_names.append(name.lower())

    labeled_names = []
    used_labels = []
    for name in nameList:
        label = name
        if lower_names.count(name.lower()) > 1:
            number = 1
            label = f"{name} [{number}]"
            while label.lower() in lower_names or label.lower() in used_labels:
                number += 1
                label = f"{name} [{number}]"

        labeled_names.append(label)
        used_labels.append(label.lower())
    return labeled_names


def print_permutations(chosen, remaining):
    """Use recursion to print each complete ordering."""
    if not remaining:
        print(", ".join(chosen))
        return

    def try_choice(i):
        if i == len(remaining):
            return
        new_chosen = chosen + [remaining[i]]
        new_remaining = remaining[:i] + remaining[i + 1:]
        print_permutations(new_chosen, new_remaining)
        try_choice(i + 1)

    try_choice(0)


def ask_to_continue():
    """Ask whether the user wants another group."""
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
    print("Welcome to the Name Permutations Program!")
    try:
        while True:
            count = read_person_count()
            nameList = read_names(count)
            nameList = number_duplicate_names(nameList)
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
    except RecursionError:
        print("\nPython recursion limit reached. Try a smaller group. Goodbye!")


if __name__ == "__main__":
    main()
