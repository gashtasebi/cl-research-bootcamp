from pathlib import Path
import re

from collections import Counter


# Load the dataset.
data_path = Path("data/morphology_test.txt")
text = data_path.read_text(encoding="utf-8")


# Tokenize the text.
tokens = re.findall(r"\b[a-zA-Z]+\b", text.lower())


# Create unigrams.
unigrams = tokens


# Create bigrams.
bigrams = list(zip(tokens, tokens[1:]))


# Count frequencies.
unigram_counts = Counter(unigrams)
bigram_counts = Counter(bigrams)


print("=== N-GRAM ANALYSIS ===")
print()

print(f"Total tokens: {len(tokens)}")
print(f"Unique tokens: {len(unigram_counts)}")
print(f"Total bigrams: {len(bigrams)}")
print(f"Unique bigrams: {len(bigram_counts)}")

print()
print("=== TOP UNIGRAMS ===")

for word, count in unigram_counts.most_common(10):
    print(f"{word:<15} {count}")


print()
print("=== TOP BIGRAMS ===")

for (word1, word2), count in bigram_counts.most_common(10):
    print(f"{word1} {word2:<20} {count}")
