import argparse
from pathlib import Path
import re


def solve_kobza(impossible_letters, existing_letters, pattern):
    """
    Solve the Kobza game by filtering words based on given constraints.
    
    :param impossible_letters: Letters that cannot be in the word
    :param existing_letters: Letters that must be in the word
    :param pattern: Regex pattern to match the word structure
    :return: List of matching words
    """
    # Read dictionary
    dictionary_path = "kobza_filtered_dict_words.txt"
    try:
        five_letters = Path(dictionary_path).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        print(f"Error: Dictionary file not found at {dictionary_path}")
        return []

    found = []

    for word in five_letters:
        # Skip words with impossible letters
        if any(letter in word for letter in impossible_letters):
            continue

        # Check if all existing letters are present
        if not all(letter in word for letter in existing_letters):
            continue

        # Check regex pattern
        if re.match(pattern, word):
            found.append(word)

    return sorted(found)


def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Solve Kobza game (Ukrainian Wordle) by filtering words")

    parser.add_argument("-i", "--impossible",
                        default="",
                        help="Letters that cannot be in the word")

    parser.add_argument("-e", "--existing",
                        default="",
                        help="Letters that must be in the word")

    parser.add_argument("-p", "--pattern",
                        default=".....",
                        help="Regex pattern to match word structure (e.g., '...но')")

    # Parse arguments
    args = parser.parse_args()

    # Solve and print results
    matching_words = solve_kobza(
        args.impossible,
        args.existing,
        args.pattern
    )

    print(f"Found {len(matching_words)} words")
    print("\n".join(matching_words))


if __name__ == "__main__":
    main()
