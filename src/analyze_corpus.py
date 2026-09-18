from pathlib import Path
import re
from collections import Counter


corpus_path = Path("data/corpus.txt")
test_path = Path("data/tokenization_test.txt")


# --------------------------------------------------
# 1. Load corpus
# --------------------------------------------------

text = corpus_path.read_text(encoding="utf-8")

print("=== CORPUS ANALYSIS ===")
print()

print("Characters:", len(text))

documents = text.splitlines()
print("Documents:", len(documents))

sentences = [
    sentence.strip()
    for sentence in text.replace("!", ".").replace("?", ".").split(".")
    if sentence.strip()
]

print("Sentences:", len(sentences))


# --------------------------------------------------
# 2. Tokenization
# --------------------------------------------------

tokens = re.findall(r"\b\w+\b", text.lower())

print("Tokens:", len(tokens))


# --------------------------------------------------
# 3. Vocabulary
# --------------------------------------------------

vocabulary = set(tokens)

print("Vocabulary size:", len(vocabulary))


# --------------------------------------------------
# 4. Frequency
# --------------------------------------------------

frequency = Counter(tokens)

print()
print("Most frequent words:")

for word, count in frequency.most_common(10):
    print(f"{word} -> {count}")


# --------------------------------------------------
# 5. Tokenization error analysis
# --------------------------------------------------

test_text = test_path.read_text(encoding="utf-8")

test_tokens = re.findall(r"\b\w+\b", test_text.lower())

print()
print("=== TOKENIZATION ERROR ANALYSIS ===")
print()

print("Original text:")
print(test_text)

print("Our tokens:")

for token in test_tokens:
    print(f"- {token}")
