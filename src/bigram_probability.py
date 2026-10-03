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
    sentence_bigrams = list(zip(tokens, tokens[1:]))
    bigrams.extend(sentence_bigrams)


# Count words and bigrams.
unigram_counts = Counter()

for tokens in sentence_tokens:
    unigram_counts.update(tokens)

bigram_counts = Counter(bigrams)


# Calculate bigram probabilities.
def bigram_probability(word1, word2):
    bigram_count = bigram_counts[(word1, word2)]
    word1_count = unigram_counts[word1]

    if word1_count == 0:
        return 0

    return bigram_count / word1_count


print("=== BIGRAM PROBABILITY ANALYSIS ===")
print()

examples = [
    ("are", "studying"),
    ("the", "students"),
    ("the", "student"),
    ("students", "are"),
    ("cats", "are"),
]

for word1, word2 in examples:
    count_bigram = bigram_counts[(word1, word2)]
    count_word1 = unigram_counts[word1]
    probability = bigram_probability(word1, word2)

    print(f"P({word2} | {word1})")
    print(f"  Count({word1}, {word2}): {count_bigram}")
    print(f"  Count({word1}): {count_word1}")
    print(f"  Probability: {probability:.3f}")
    print()
