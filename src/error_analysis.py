from pathlib import Path
from collections import Counter, defaultdict
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.pipeline import Pipeline


DEVELOPMENT_PATH = Path("data/sentiment_dataset_evaluation.txt")
CHALLENGE_PATH = Path("data/error_analysis_challenge.txt")
LABELS = ["negative", "positive"]


def load_dataset(path, fields):
    """Read pipe-separated records and validate their fields."""
    examples = []

    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = line.strip()

        if not line:
            continue

        parts = [part.strip() for part in line.split("|", maxsplit=fields - 1)]

        if len(parts) != fields:
            raise ValueError(
                f"{path}, line {line_number}: expected {fields} fields "
                "separated by '|'."
            )

        examples.append(parts)

    return examples


development_rows = load_dataset(DEVELOPMENT_PATH, fields=3)
challenge_rows = load_dataset(CHALLENGE_PATH, fields=3)

if len(development_rows) != 48:
    raise ValueError(
        f"Expected 48 development examples, found {len(development_rows)}."
    )

if len(challenge_rows) != 16:
    raise ValueError(
        f"Expected 16 challenge examples, found {len(challenge_rows)}."
    )

development_labels = [row[0].lower() for row in development_rows]
development_topics = [row[1].lower() for row in development_rows]
development_texts = [row[2] for row in development_rows]

gold_labels = [row[0].lower() for row in challenge_rows]
phenomena = [row[1].lower() for row in challenge_rows]
challenge_texts = [row[2] for row in challenge_rows]

# Recreate the tuned model selected in Experiment 13.
# These settings are fixed; the challenge set is not used for tuning.
model = Pipeline([
    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            token_pattern=r"(?u)\b[a-zA-Z]+\b",
            min_df=1,
            ngram_range=(1, 2),
            sublinear_tf=False,
        ),
    ),
    (
        "classifier",
        LogisticRegression(
            C=0.1,
            max_iter=2000,
            random_state=42,
        ),
    ),
])

model.fit(development_texts, development_labels)

predictions = model.predict(challenge_texts)
probabilities = model.predict_proba(challenge_texts)

classifier = model.named_steps["classifier"]
positive_index = list(classifier.classes_).index("positive")
positive_probabilities = probabilities[:, positive_index]

# The fixed majority baseline is negative because development labels are tied.
development_counts = Counter(development_labels)
majority_label = max(
    development_counts,
    key=lambda label: (
        development_counts[label],
        label == "negative",
    ),
)
baseline_predictions = [majority_label] * len(gold_labels)

print("=== EXPERIMENT 14: ERROR ANALYSIS ===")
print("Development examples:", len(development_rows))
print("Challenge examples:", len(challenge_rows))
print("Development label counts:", dict(sorted(development_counts.items())))
print("Challenge label counts:", dict(sorted(Counter(gold_labels).items())))
print("Challenge phenomena:", dict(sorted(Counter(phenomena).items())))
print("Model settings: fixed from Experiment 13; no challenge-set tuning")
print()

print("=== OVERALL CHALLENGE-SET METRICS ===")
print(f"Majority baseline ({majority_label}):")
print(f"  Accuracy: {accuracy_score(gold_labels, baseline_predictions):.3f}")
print(f"  Macro F1: {f1_score(gold_labels, baseline_predictions, average='macro', zero_division=0):.3f}")
print("Tuned TF-IDF + Logistic Regression:")
print(f"  Accuracy:  {accuracy_score(gold_labels, predictions):.3f}")
print(
    "  Precision: "
    f"{precision_score(gold_labels, predictions, average='macro', zero_division=0):.3f}"
)
print(
    "  Recall:    "
    f"{recall_score(gold_labels, predictions, average='macro', zero_division=0):.3f}"
)
print(
    "  Macro F1:  "
    f"{f1_score(gold_labels, predictions, average='macro', zero_division=0):.3f}"
)

matrix = confusion_matrix(gold_labels, predictions, labels=LABELS)
print("  Confusion matrix (rows=actual, columns=predicted):")
print(f"                 predicted {LABELS[0]:<8} {LABELS[1]}")
for label, row in zip(LABELS, matrix):
    print(f"    actual {label:<8} {row[0]:>5} {row[1]:>8}")
print()

print("=== RESULTS BY LINGUISTIC PHENOMENON ===")
indices_by_phenomenon = defaultdict(list)

for index, phenomenon in enumerate(phenomena):
    indices_by_phenomenon[phenomenon].append(index)

for phenomenon in sorted(indices_by_phenomenon):
    indices = indices_by_phenomenon[phenomenon]
    category_gold = [gold_labels[index] for index in indices]
    category_predictions = [predictions[index] for index in indices]
    category_accuracy = accuracy_score(category_gold, category_predictions)
    errors = sum(
        gold != prediction
        for gold, prediction in zip(category_gold, category_predictions)
    )

    print(
        f"{phenomenon}: accuracy={category_accuracy:.3f}, "
        f"errors={errors}/{len(indices)}"
    )

print()
print("=== ITEM-LEVEL PREDICTIONS ===")

for index, (row, gold, prediction, positive_probability) in enumerate(
    zip(
        challenge_rows,
        gold_labels,
        predictions,
        positive_probabilities,
    ),
    start=1,
):
    _label, phenomenon, text = row
    result = "CORRECT" if gold == prediction else "ERROR"

    print(f"{index}. [{phenomenon}] {text}")
    print(
        f"   Gold: {gold} | Predicted: {prediction} | "
        f"P(positive): {positive_probability:.3f} | {result}"
    )

    # Report unseen single-word terms for diagnosing vocabulary coverage.
    vectorizer = model.named_steps["tfidf"]
    known_unigrams = {
        feature
        for feature in vectorizer.vocabulary_
        if " " not in feature
    }
    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())
    unknown_words = sorted(set(words) - known_unigrams)

    if unknown_words:
        print("   Unseen words:", ", ".join(unknown_words))

    # For errors, show feature contributions toward positive or negative.
    if gold != prediction:
        feature_vector = vectorizer.transform([text]).toarray()[0]
        feature_names = vectorizer.get_feature_names_out()
        coefficients = model.named_steps["classifier"].coef_[0]

        contributions = [
            (feature_names[feature_index],
             feature_vector[feature_index] * coefficients[feature_index])
            for feature_index in range(len(feature_names))
            if feature_vector[feature_index] != 0
        ]
        contributions.sort(key=lambda item: abs(item[1]), reverse=True)

        print("   Strongest feature contributions:")
        if contributions:
            for feature, contribution in contributions[:6]:
                direction = "toward positive" if contribution > 0 else "toward negative"
                print(f"     {feature}: {contribution:+.3f} ({direction})")
        else:
            print("     No known TF-IDF features were present.")

    print()

print("=== PER-CLASS REPORT ===")
print(
    classification_report(
        gold_labels,
        predictions,
        labels=LABELS,
        target_names=LABELS,
        zero_division=0,
    )
)

print("This is a deliberately challenging diagnostic set, not a general benchmark.")
print("The challenge examples were not used to fit the model or select its settings.")
