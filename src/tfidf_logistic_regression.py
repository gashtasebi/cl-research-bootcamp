from pathlib import Path
from collections import Counter, defaultdict
import random

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score


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
                f"Line {line_number} must contain '|' between label and text."
            )

        label, text = line.split("|", maxsplit=1)
        label = label.strip().lower()
        text = text.strip()

        if not label or not text:
            raise ValueError(f"Line {line_number} has a missing label or text.")

        examples.append((label, text))

    return examples


def stratified_split(examples, test_fraction, seed):
    """Reproduce Experiment 11's stratified split exactly."""
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


examples = load_dataset(DATA_PATH)
labels = sorted({label for label, _text in examples})

if set(labels) != {"negative", "positive"}:
    raise ValueError(
        "This experiment expects exactly the labels 'negative' and 'positive'."
    )

train_examples, test_examples = stratified_split(
    examples,
    TEST_FRACTION,
    RANDOM_SEED,
)

train_texts = [text for _label, text in train_examples]
train_labels = [label for label, _text in train_examples]
test_texts = [text for _label, text in test_examples]
test_labels = [label for label, _text in test_examples]

# Fit TF-IDF on training texts only, then transform the held-out test texts.
vectorizer = TfidfVectorizer(
    lowercase=True,
    token_pattern=r"(?u)\b[a-zA-Z]+\b",
)
X_train = vectorizer.fit_transform(train_texts)
X_test = vectorizer.transform(test_texts)

# Train logistic regression on the TF-IDF feature matrix.
model = LogisticRegression(max_iter=1000, random_state=RANDOM_SEED)
model.fit(X_train, train_labels)
model_predictions = model.predict(X_test)

# Majority-class baseline from the training labels.
train_label_counts = Counter(train_labels)
majority_label = max(
    train_label_counts,
    key=lambda label: (
        train_label_counts[label],
        label == "negative",
    ),
)
baseline_predictions = [majority_label] * len(test_labels)

model_accuracy = accuracy_score(test_labels, model_predictions)
baseline_accuracy = accuracy_score(test_labels, baseline_predictions)

print("=== TF-IDF AND LOGISTIC REGRESSION ===")
print("Task: positive/negative sentiment classification")
print("Random seed:", RANDOM_SEED)
print()

print("=== DATA SPLIT ===")
print("Training examples:", len(train_examples), dict(sorted(Counter(train_labels).items())))
print("Test examples:", len(test_examples), dict(sorted(Counter(test_labels).items())))
print()

print("=== TF-IDF FEATURE MATRICES ===")
print("Training matrix shape:", X_train.shape)
print("Test matrix shape:", X_test.shape)
print("Vocabulary size learned from training data:", len(vectorizer.vocabulary_))
print()

# Show the strongest non-zero TF-IDF features in the first test example.
if len(test_texts) > 0:
    first_test_vector = X_test[0].toarray()[0]
    feature_names = vectorizer.get_feature_names_out()
    nonzero_indices = [
        index for index, value in enumerate(first_test_vector)
        if value > 0
    ]
    strongest_indices = sorted(
        nonzero_indices,
        key=lambda index: first_test_vector[index],
        reverse=True,
    )[:8]

    print("TF-IDF features for the first test example:")
    print(test_texts[0])
    if strongest_indices:
        for index in strongest_indices:
            print(f"  {feature_names[index]}: {first_test_vector[index]:.3f}")
    else:
        print("  No test words were present in the training vocabulary.")
    print()

print("=== TEST PREDICTIONS ===")
for index, (text, gold, prediction, baseline) in enumerate(
    zip(test_texts, test_labels, model_predictions, baseline_predictions),
    start=1,
):
    print(f"Example {index}: {text}")
    print("  Gold label:", gold)
    print("  Logistic Regression:", prediction)
    print("  Majority baseline:", baseline)
    print()

print("=== ACCURACY ===")
print(f"TF-IDF + Logistic Regression: {model_accuracy:.3f}")
print(f"Majority-class baseline:      {baseline_accuracy:.3f}")
print("Test examples:", len(test_examples))

if model_accuracy > baseline_accuracy:
    print("Logistic Regression outperformed the majority baseline on this split.")
elif model_accuracy == baseline_accuracy:
    print("Logistic Regression matched the majority baseline on this split.")
else:
    print("Logistic Regression performed below the majority baseline on this split.")

print()
print("These results describe this small held-out test split only.")
