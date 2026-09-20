from pathlib import Path
import nltk
from nltk.tokenize import word_tokenize


nltk.download("punkt_tab", quiet=True)


# Load original text.
text_path = Path("data/tokenization_test.txt")
text = text_path.read_text(encoding="utf-8")


# Load Gold Standard.
gold_path = Path("data/gold_tokens.txt")
gold_tokens = gold_path.read_text(encoding="utf-8").splitlines()


# Generate tokens with NLTK.
predicted_tokens = word_tokenize(text)


print("=== TOKEN ALIGNMENT ===")
print()

gold_index = 0
predicted_index = 0

while (
    gold_index < len(gold_tokens)
    and predicted_index < len(predicted_tokens)
):
    gold = gold_tokens[gold_index]
    predicted = predicted_tokens[predicted_index]

    if gold == predicted:
        print(f"MATCH: {gold}")
        gold_index += 1
        predicted_index += 1

    elif predicted.startswith(gold):
        print(f"DIFFERENT: Gold={gold} | NLTK={predicted}")
        gold_index += 1
        predicted_index += 1

    elif gold.startswith(predicted):
        print(f"SPLIT: Gold={gold} | NLTK={predicted}")
        predicted_index += 1

    else:
        print(f"MISMATCH: Gold={gold} | NLTK={predicted}")
        gold_index += 1
        predicted_index += 1


print()
print("Remaining Gold tokens:", len(gold_tokens) - gold_index)
print("Remaining NLTK tokens:", len(predicted_tokens) - predicted_index)
