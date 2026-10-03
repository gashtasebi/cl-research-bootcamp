from pathlib import Path
import re

from collections import Counter


# Load the dataset.
data_path = Path("data/morphology_test.txt")
text = data_path.read_text(encoding="utf-8")


# Split the corpus into sentences.
sentences = re.split(r"[.!?]+", text)


# Store tokens for each sentence.
sentence_tokens = []

for sentence in sentences:
    tokens = re.findall(r"\b[a-zA-Z]+\b", sentence.lower())

    if tokens:
        sentence_tokens.append(tokens)


# Create sentence-aware bigrams.
bigrams = []

for tokens in sentence_tokens:
    sentence_bigrams = list(zip(tokens, tokens[1:]))
    bigrams.extend(sentence_bigrams)


# Count bigram frequencies.
bigram_counts = Counter(bigrams)


print("=== SENTENCE-AWARE BIGRAM ANALYSIS ===")
print()

print(f"Number of sentences: {len(sentence_tokens)}")
print(f"Total bigrams: {len(bigrams)}")
print(f"Unique bigrams: {len(bigram_counts)}")

print()
print("=== TOP BIGRAMS ===")

for (word1, word2), count in bigram_counts.most_common(10):
    print(f"{word1} {word2:<20} {count}")
