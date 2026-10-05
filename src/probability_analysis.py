from pathlib import Path
from collections import Counter
import re


# Each non-empty line in this corpus is treated as one document.
corpus_path = Path("data/corpus.txt")
documents = [
    line.strip()
    for line in corpus_path.read_text(encoding="utf-8").splitlines()
    if line.strip()
]

# Normalize to lowercase and extract alphabetic word tokens.
document_tokens = [
    re.findall(r"\b[a-zA-Z]+\b", document.lower())
    for document in documents
]

all_tokens = [
    token
    for tokens in document_tokens
    for token in tokens
]

token_counts = Counter(all_tokens)
total_tokens = len(all_tokens)
vocabulary_size = len(token_counts)
document_count = len(documents)


def contains_term(tokens, term):
    """Return whether a document contains a whole-word term."""
    return term in tokens


# Events are defined over documents:
# D = a randomly selected document contains "data"
# R = a randomly selected document contains "project"
data_documents = [
    tokens for tokens in document_tokens
    if contains_term(tokens, "data")
]
project_documents = [
    tokens for tokens in document_tokens
    if contains_term(tokens, "project")
]
data_and_project_documents = [
    tokens for tokens in document_tokens
    if contains_term(tokens, "data")
    and contains_term(tokens, "project")
]


print("=== CORPUS PROBABILITY ANALYSIS ===")
print("Corpus file:", corpus_path)
print()

print("=== BASIC CORPUS STATISTICS ===")
print("Documents:", document_count)
print("Tokens:", total_tokens)
print("Vocabulary size:", vocabulary_size)
print()

print("=== MOST FREQUENT TOKENS ===")
for token, count in token_counts.most_common(10):
    relative_frequency = count / total_tokens
    print(
        f"{token:<15} count={count:<3} "
        f"relative_frequency={relative_frequency:.3f}"
    )

print()
print("=== TARGET TERM FREQUENCIES ===")

for term in ("data", "project"):
    token_frequency = token_counts[term]
    document_frequency = sum(
        1 for tokens in document_tokens
        if contains_term(tokens, term)
    )

    print(f"Term: {term}")
    print("  Token frequency:", token_frequency)
    print("  Document frequency:", document_frequency)
    print(
        "  Relative token frequency:",
        f"{token_frequency / total_tokens:.3f}"
        if total_tokens else "undefined",
    )
    print(
        "  Document probability:",
        f"{document_frequency / document_count:.3f}"
        if document_count else "undefined",
    )

print()
print("=== DOCUMENT-LEVEL PROBABILITIES ===")

if document_count == 0:
    print("No documents were found; probabilities cannot be calculated.")
else:
    probability_data = len(data_documents) / document_count
    probability_project = len(project_documents) / document_count
    probability_both = len(data_and_project_documents) / document_count

    if project_documents:
        probability_data_given_project = (
            len(data_and_project_documents) / len(project_documents)
        )
    else:
        probability_data_given_project = None

    print(
        "P(data) = documents containing 'data' / all documents = "
        f"{len(data_documents)} / {document_count} = "
        f"{probability_data:.3f}"
    )
    print(
        "P(project) = documents containing 'project' / all documents = "
        f"{len(project_documents)} / {document_count} = "
        f"{probability_project:.3f}"
    )
    print(
        "P(data AND project) = documents containing both / all documents = "
        f"{len(data_and_project_documents)} / {document_count} = "
        f"{probability_both:.3f}"
    )

    if probability_data_given_project is None:
        print("P(data | project) is undefined because no document contains 'project'.")
    else:
        print(
            "P(data | project) = documents containing both / documents "
            "containing 'project' = "
            f"{len(data_and_project_documents)} / {len(project_documents)} = "
            f"{probability_data_given_project:.3f}"
        )

        print()
        print("=== COMPARISON ===")
        print(f"Marginal P(data):      {probability_data:.3f}")
        print(f"Conditional P(data|project): {probability_data_given_project:.3f}")

        if probability_data_given_project > probability_data:
            print(
                "In this corpus, documents containing 'project' are more "
                "likely to contain 'data' than a randomly selected document."
            )
        elif probability_data_given_project < probability_data:
            print(
                "In this corpus, documents containing 'project' are less "
                "likely to contain 'data' than a randomly selected document."
            )
        else:
            print(
                "In this corpus, conditioning on 'project' does not change "
                "the observed probability of 'data'."
            )

print()
print("These are empirical estimates from this small corpus only.")
