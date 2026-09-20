from pathlib import Path
import nltk
from nltk.tokenize import word_tokenize


nltk.download("punkt_tab", quiet=True)


# --------------------------------------------------
# Load data
# --------------------------------------------------

text_path = Path("data/tokenization_test.txt")
text = text_path.read_text(encoding="utf-8")

gold_path = Path("data/gold_tokens.txt")
gold_tokens = gold_path.read_text(encoding="utf-8").splitlines()


# --------------------------------------------------
# Helper function
# --------------------------------------------------

def find_token_spans(text, tokens):
    """
    Find the character start and end position
    of every token in the original text.
    """

    spans = []
    search_start = 0

    for token in tokens:
        start = text.find(token, search_start)

        if start == -1:
            raise ValueError(
                f"Could not find token in text: {token}"
            )

        end = start + len(token)

        spans.append((start, end, token))

        search_start = end

    return spans


# --------------------------------------------------
# Generate NLTK tokens
# --------------------------------------------------

predicted_tokens = word_tokenize(text)


# --------------------------------------------------
# Convert tokens into character spans
# --------------------------------------------------

gold_spans = find_token_spans(text, gold_tokens)
predicted_spans = find_token_spans(text, predicted_tokens)


# --------------------------------------------------
# Extract token boundaries
# --------------------------------------------------

gold_boundaries = {
    (start, end)
    for start, end, token in gold_spans
}

predicted_boundaries = {
    (start, end)
    for start, end, token in predicted_spans
}


# --------------------------------------------------
# Calculate TP / FP / FN
# --------------------------------------------------

true_positives = len(
    gold_boundaries & predicted_boundaries
)

false_positives = len(
    predicted_boundaries - gold_boundaries
)

false_negatives = len(
    gold_boundaries - predicted_boundaries
)


# --------------------------------------------------
# Calculate Precision
# --------------------------------------------------

if true_positives + false_positives > 0:
    precision = (
        true_positives
        / (true_positives + false_positives)
    )
else:
    precision = 0.0


# --------------------------------------------------
# Calculate Recall
# --------------------------------------------------

if true_positives + false_negatives > 0:
    recall = (
        true_positives
        / (true_positives + false_negatives)
    )
else:
    recall = 0.0


# --------------------------------------------------
# Calculate F1
# --------------------------------------------------

if precision + recall > 0:
    f1 = (
        2 * precision * recall
        / (precision + recall)
    )
else:
    f1 = 0.0


# --------------------------------------------------
# Print results
# --------------------------------------------------

print("=== TOKENIZATION EVALUATION ===")
print()

print("Gold tokens:", len(gold_tokens))
print("NLTK tokens:", len(predicted_tokens))

print()

print("True Positives:", true_positives)
print("False Positives:", false_positives)
print("False Negatives:", false_negatives)

print()

print(f"Precision: {precision:.3f}")
print(f"Recall:    {recall:.3f}")
print(f"F1 Score:  {f1:.3f}")

print()

print("=== INTERPRETATION ===")

if f1 >= 0.90:
    print("The tokenizer closely matches the Gold Standard.")
elif f1 >= 0.75:
    print("The tokenizer shows moderate agreement with the Gold Standard.")
else:
    print("The tokenizer differs substantially from the Gold Standard.")
