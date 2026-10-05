from pathlib import Path
from collections import Counter

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
from sklearn.model_selection import GridSearchCV, StratifiedGroupKFold
from sklearn.pipeline import Pipeline


DEVELOPMENT_PATH = Path("data/sentiment_dataset_evaluation.txt")
FINAL_TEST_PATH = Path("data/sentiment_final_test.txt")
RANDOM_SEED = 42
LABELS = ["negative", "positive"]


def load_dataset(path):
    """Read records formatted as label | topic | text."""
    examples = []

    for line_number, line in enumerate(
        path.read_text(encoding="utf-8").splitlines(),
        start=1,
    ):
        line = line.strip()

        if not line:
            continue

        parts = [part.strip() for part in line.split("|", maxsplit=2)]

        if len(parts) != 3:
            raise ValueError(
                f"{path}, line {line_number}: expected label | topic | text"
            )

        label, topic, text = parts
        label = label.lower()
        topic = topic.lower()

        if label not in LABELS:
            raise ValueError(
                f"{path}, line {line_number}: unexpected label {label!r}"
            )

        if not topic or not text:
            raise ValueError(
                f"{path}, line {line_number}: topic and text must be present"
            )

        examples.append({
            "label": label,
            "topic": topic,
            "text": text,
        })

    return examples


def make_pipeline():
    """Keep vectorization inside the pipeline to prevent data leakage."""
    return Pipeline([
        (
            "tfidf",
            TfidfVectorizer(
                lowercase=True,
                token_pattern=r"(?u)\b[a-zA-Z]+\b",
            ),
        ),
        (
            "classifier",
            LogisticRegression(
                max_iter=2000,
                random_state=RANDOM_SEED,
            ),
        ),
    ])


def report_metrics(name, gold, predictions):
    """Print standard classification metrics and the confusion matrix."""
    print(name)
    print(f"  Accuracy:  {accuracy_score(gold, predictions):.3f}")
    print(
        "  Precision: "
        f"{precision_score(gold, predictions, average='macro', zero_division=0):.3f}"
    )
    print(
        "  Recall:    "
        f"{recall_score(gold, predictions, average='macro', zero_division=0):.3f}"
    )
    print(
        "  Macro F1:  "
        f"{f1_score(gold, predictions, average='macro', zero_division=0):.3f}"
    )

    matrix = confusion_matrix(gold, predictions, labels=LABELS)
    print("  Confusion matrix (rows=actual, columns=predicted):")
    print(f"                 predicted {LABELS[0]:<8} {LABELS[1]}")
    for label, row in zip(LABELS, matrix):
        print(f"    actual {label:<8} {row[0]:>5} {row[1]:>8}")
    print()


development = load_dataset(DEVELOPMENT_PATH)
final_test = load_dataset(FINAL_TEST_PATH)

if len(development) != 48:
    raise ValueError(
        f"Expected 48 development examples, found {len(development)}."
    )

if len(final_test) != 12:
    raise ValueError(
        f"Expected 12 final test examples, found {len(final_test)}."
    )

development_labels = [row["label"] for row in development]
development_topics = [row["topic"] for row in development]
development_texts = [row["text"] for row in development]

test_labels = [row["label"] for row in final_test]
test_topics = [row["topic"] for row in final_test]
test_texts = [row["text"] for row in final_test]

if set(development_labels) != set(LABELS):
    raise ValueError("The development data must contain both sentiment labels.")

if set(test_labels) != set(LABELS):
    raise ValueError("The final test data must contain both sentiment labels.")

print("=== EXPERIMENT 13: FINAL MODEL EVALUATION ===")
print("Development examples:", len(development))
print("Final test examples:", len(final_test))
print("Development label counts:", dict(sorted(Counter(development_labels).items())))
print("Final test label counts:", dict(sorted(Counter(test_labels).items())))
print("Development topics:", dict(sorted(Counter(development_topics).items())))
print("Final test topics:", dict(sorted(Counter(test_topics).items())))
print()

# Tune only on development data. Each validation fold holds out whole topics.
grouped_cv = StratifiedGroupKFold(
    n_splits=3,
    shuffle=True,
    random_state=RANDOM_SEED,
)

parameter_grid = {
    "tfidf__ngram_range": [(1, 1), (1, 2)],
    "tfidf__min_df": [1, 2],
    "tfidf__sublinear_tf": [False, True],
    "classifier__C": [0.1, 1, 10],
}

search = GridSearchCV(
    estimator=make_pipeline(),
    param_grid=parameter_grid,
    scoring="f1_macro",
    cv=grouped_cv,
    refit=True,
    n_jobs=1,
)

search.fit(
    development_texts,
    development_labels,
    groups=development_topics,
)

tuned_model = search.best_estimator_
tuned_predictions = tuned_model.predict(test_texts)

# Train an untuned/default model on the same complete development set.
default_model = make_pipeline()
default_model.fit(development_texts, development_labels)
default_predictions = default_model.predict(test_texts)

# Majority baseline based only on development labels.
development_counts = Counter(development_labels)
majority_label = max(
    development_counts,
    key=lambda label: (
        development_counts[label],
        label == "negative",
    ),
)
baseline_predictions = [majority_label] * len(test_labels)

print("=== MODEL SELECTION ===")
print("Cross-validation: 3-fold, grouped by topic")
print(f"Best cross-validation macro F1: {search.best_score_:.3f}")
print("Best parameters:", search.best_params_)
print()

print("=== FINAL TEST METRICS ===")
report_metrics("Majority-class baseline", test_labels, baseline_predictions)
report_metrics("Default TF-IDF + Logistic Regression", test_labels, default_predictions)
report_metrics("Tuned TF-IDF + Logistic Regression", test_labels, tuned_predictions)

print("=== FINAL TEST PREDICTIONS ===")
for index, (row, gold, prediction) in enumerate(
    zip(final_test, test_labels, tuned_predictions),
    start=1,
):
    result = "CORRECT" if gold == prediction else "INCORRECT"
    print(f"{index}. [{row['topic']}] {row['text']}")
    print(f"   Gold: {gold} | Tuned prediction: {prediction} | {result}")

print()
print("=== PER-CLASS REPORT FOR THE TUNED MODEL ===")
print(
    classification_report(
        test_labels,
        tuned_predictions,
        labels=LABELS,
        target_names=LABELS,
        zero_division=0,
    )
)

# Show whether test words are represented in the development vocabulary.
vectorizer = tuned_model.named_steps["tfidf"]
analyzer = vectorizer.build_analyzer()
vocabulary = set(vectorizer.vocabulary_)

print("=== FINAL TEST VOCABULARY COVERAGE ===")
for row in final_test:
    tokens = analyzer(row["text"])
    unknown_tokens = sorted(set(tokens) - vocabulary)
    print(f"[{row['topic']}] {row['text']}")
    print("  Out-of-vocabulary terms:", ", ".join(unknown_tokens) if unknown_tokens else "none")

print()
print("The final test set was not used for cross-validation or model selection.")
