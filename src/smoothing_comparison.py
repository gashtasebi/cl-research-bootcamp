from pathlib import Path
import re

from collections import Counter


# Load the dataset.
data_path = Path("data/morphology_test.txt")
text = data_path.read_text(encoding="utf-8")


# Split the corpus into sentences.
sentences = re.split(r"[.!?]+", text)


# Tokenize each sentence.
sentence_tokens = []

for sentence in sentences:
    tokens = re.findall(r"\b[a-zA-Z]+\b", sentence.lower())

    if tokens:
        sentence_tokens.append(tokens)


# Create sentence-aware bigrams.
bigrams = []

for tokens in sentence_tokens:
    bigrams.extend(zip(tokens, tokens[1:]))


# Count words and bigrams.
unigram_counts = Counter()

for tokens in sentence_tokens:
    unigram_counts.update(tokens)

bigram_counts = Counter(bigrams)


# Vocabulary size.
vocabulary_size = len(unigram_counts)


# Original bigram probability.
def original_probability(word1, word2):
    return bigram_counts[(word1, word2)] / unigram_counts[word1]


# Laplace-smoothed probability.
def laplace_probability(word1, word2):
    return (
        bigram_counts[(word1, word2)] + 1
    ) / (
        unigram_counts[word1] + vocabulary_size
    )


print("=== SMOOTHING COMPARISON ===")
print()

examples = [
    ("are", "studying"),
    ("the", "students"),
    ("students", "is"),
    ("cats", "is"),
]

for word1, word2 in examples:

    original = original_probability(word1, word2)
    smoothed = laplace_probability(word1, word2)

    print(f"P({word2} | {word1})")
    print(f"  Original: {original:.4f}")
    print(f"  Laplace:  {smoothed:.4f}")
    print()
