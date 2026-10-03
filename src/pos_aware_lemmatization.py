from pathlib import Path
import re

import nltk
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer


# Load the dataset.
data_path = Path("data/morphology_test.txt")
text = data_path.read_text(encoding="utf-8")


# Extract tokens.
tokens = re.findall(r"\b[a-zA-Z]+\b", text.lower())


# POS tagging.
tagged_tokens = pos_tag(tokens)


# Initialize the lemmatizer.
lemmatizer = WordNetLemmatizer()


def penn_to_wordnet(tag):
    """
    Convert a Penn Treebank POS tag to a WordNet POS tag.
    """

    if tag.startswith("N"):
        return "n"

    if tag.startswith("V"):
        return "v"

    if tag.startswith("J"):
        return "a"

    if tag.startswith("R"):
        return "r"

    return "n"


print("=== POS-AWARE LEMMATIZATION ===")
print()

print(f"{'WORD':<15} {'PENN POS':<10} {'LEMMA':<15}")
print("-" * 40)

for word, penn_tag in tagged_tokens:

    wordnet_tag = penn_to_wordnet(penn_tag)

    lemma = lemmatizer.lemmatize(
        word,
        pos=wordnet_tag
    )

    print(f"{word:<15} {penn_tag:<10} {lemma:<15}")
