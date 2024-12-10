from pathlib import Path
import re

# https://github.com/kobzaapp/kobzadict/blob/main/out/kobza_filtered_dict_words.txt
five_letters = Path("kobza_filtered_dict_words.txt").read_text(encoding="utf-8").splitlines()

impossible_letters = "кіабумерпчв"
possible_letters = "доин"
pattern = "...но"

found = []

for word in five_letters:
    contains_impossible_letters = False
    for letter in impossible_letters:
        if letter in word:
            contains_impossible_letters = True
            break
    if contains_impossible_letters:
        continue

    contains_possible_letters = 0
    for letter in possible_letters:
        if letter in word:
            contains_possible_letters += 1
        else:
            break
    if contains_possible_letters < len(possible_letters):
        continue

    if re.match(pattern, word):
        found.append(word)

print(f"Found {len(found)} words")
print("\n".join(found))
