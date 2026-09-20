from pathlib import Path
import nltk
from nltk.tokenize import word_tokenize


# Make sure NLTK has the required tokenizer data.
nltk.download("punkt_tab", quiet=True)


# Load the original text.
text_path = Path("data/tokenization_test.txt")
text = text_path.read_text(encoding="utf-8")


# Load the Gold Standard.
gold_path = Path("data/gold_tokens.txt")
gold_tokens = gold_path.read_text(encoding="utf-8").splitlines()


# Generate tokens with NLTK.
predicted_tokens = word_tokenize(text)


print("=== TOKENIZATION EVALUATION ===")
print()

print("Gold Standard tokens:", len(gold_tokens))
print("NLTK tokens:", len(predicted_tokens))

print()
print("=== TOKEN COMPARISON ===")

max_length = max(len(gold_tokens), len(predicted_tokens))

correct = 0

for i in range(max_length):
    gold = gold_tokens[i] if i < len(gold_tokens) else "<missing>"
    predicted = (
        predicted_tokens[i]
        if i < len(predicted_tokens)
        else "<missing>"
    )

    if gold == predicted:
        correct += 1
        status = "CORRECT"
    else:
        status = "ERROR"

    print(
        f"{i + 1:02d} | "
        f"Gold: {gold:<25} | "
        f"NLTK: {predicted:<25} | "
        f"{status}"
    )

print()
print("Correct positions:", correct)
print("Total positions:", max_length)
