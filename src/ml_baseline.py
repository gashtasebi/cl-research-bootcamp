from pathlib import Path
from collections import Counter, defaultdict
import random
import re

from nltk.classify import NaiveBayesClassifier


DATA_PATH = Path("data/sentiment_dataset.txt")
TEST_FRACTION = 0.25
RANDOM_SEED = 42


def load_dataset(path):
    """Read lines formatted as label | text."""
    examples = []

    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = line.strip()

        if not line:
            continue

        if "|" not in line:
            raise ValueError(
                f"Line {line_number} must contain a '|' between label and text."
            )

        label, text = line.split("|", maxsplit=1)
        label = label.strip().lower()
        text = text.strip()

        if not label or not text:
            raise ValueError(f"Line {line_number} has a missing label or text.")

        examples.append((label, text))

    return examples


def extract_features(text):
    """Represent a text as binary word-presence features."""
    words = set(re.findall(r"\b[a-zA-Z]+\b", text.lower()))
    return {f"contains({word})": True for word in words}


def stratified_split(examples, test_fraction, seed):
    """Split each label separately to preserve class proportions."""
    grouped = defaultdict(list)

    for example in examples:
        grouped[example[0]].append(example)

    rng = random.Random(seed)
    train_examples = []
    test_examples = []

    for label in sorted(grouped):
        label_examples = grouped[label][:]
        rng.shuffle(label_examples)

        test_size = max(1, round(len(label_examples) * test_fraction))
        test_examples.extend(label_examples[:test_size])
        train_examples.extend(label_examples[test_size:])

    rng.shuffle(train_examples)
    rng.shuffle(test_examples)

    return train_examples, test_examples


def accuracy(gold_labels, predicted_labels):
    if not gold_labels:
        return 0.0

    correct = sum(
        gold == predicted
        for gold, predicted in zip(gold_labels, predicted_labels)
    )
    return correct / len(gold_labels)


examples = load_dataset(DATA_PATH)
labels = sorted({label for label, _text in examples})

if len(labels) < 2:
    raise ValueError("The dataset must contain at least two different labels.")

train_examples, test_examples = stratified_split(
    examples,
    TEST_FRACTION,
    RANDOM_SEED,
)

train_label_counts = Counter(label for label, _text in train_examples)
test_label_counts = Counter(label for label, _text in test_examples)

# Train the Naive Bayes model using training data only.
training_features = [
    (extract_features(text), label)
    for label, text in train_examples
]
classifier = NaiveBayesClassifier.train(training_features)

# Choose the most frequent training label for the majority-class baseline.
# If training labels are tied, choose "negative" when available.
majority_label = max(
    train_label_counts,
    key=lambda label: (
        train_label_counts[label],
        label == "negative",
    ),
)

gold_labels = []
model_predictions = []
baseline_predictions = []

print("=== MACHINE LEARNING BASELINE EXPERIMENT ===")
print("Task: positive/negative sentiment classification")
print("Random seed:", RANDOM_SEED)
print()

print("=== DATA SPLIT ===")
print("Training examples:", len(train_examples), dict(sorted(train_label_counts.items())))
print("Test examples:", len(test_examples), dict(sorted(test_label_counts.items())))
print()

print("Majority-class baseline label:", majority_label)
print()

print("=== TEST PREDICTIONS ===")

for index, (gold_label, text) in enumerate(test_examples, start=1):
    model_prediction = classifier.classify(extract_features(text))
    baseline_prediction = majority_label

    gold_labels.append(gold_label)
    model_predictions.append(model_prediction)
    baseline_predictions.append(baseline_prediction)

    print(f"Example {index}: {text}")
    print("  Gold label:", gold_label)
    print("  Naive Bayes:", model_prediction)
    print("  Majority baseline:", baseline_prediction)
    print()

model_accuracy = accuracy(gold_labels, model_predictions)
baseline_accuracy = accuracy(gold_labels, baseline_predictions)

print("=== ACCURACY ===")
print(f"Naive Bayes accuracy: {model_accuracy:.3f}")
print(f"Majority baseline accuracy: {baseline_accuracy:.3f}")
print(f"Test examples: {len(test_examples)}")

if model_accuracy > baseline_accuracy:
    print("Naive Bayes outperformed the majority-class baseline on this test split.")
elif model_accuracy == baseline_accuracy:
    print("Naive Bayes matched the majority-class baseline on this test split.")
else:
    print("Naive Bayes performed below the majority-class baseline on this test split.")

print()
print("Accuracy is measured on this small held-out test split only.")
