from pathlib import Path
import re


# Nouns that the interpreter knows.
NOUNS = {"student", "teacher", "dog", "book"}

# Verbs and their normalized predicate names.
TRANSITIVE_VERBS = {
    "reads": "read",
    "likes": "like",
    "sees": "see",
}

INTRANSITIVE_VERBS = {
    "sleeps": "sleep",
}

# Patterns for simple singular English sentences.
TRANSITIVE_PATTERN = re.compile(
    r"^(?:a|the)\s+(\w+)\s+(\w+)\s+(?:a|the)\s+(\w+)$"
)

INTRANSITIVE_PATTERN = re.compile(
    r"^(?:a|the)\s+(\w+)\s+(\w+)$"
)


def interpret(sentence):
    """Return a simple predicate representation, or a reason it is unsupported."""
    normalized = sentence.strip().lower()
    normalized = re.sub(r"[.!?]+$", "", normalized)

    transitive_match = TRANSITIVE_PATTERN.fullmatch(normalized)

    if transitive_match:
        subject, verb, obj = transitive_match.groups()

        if subject not in NOUNS:
            return None, f"Unknown subject noun: {subject}"

        if obj not in NOUNS:
            return None, f"Unknown object noun: {obj}"

        if verb not in TRANSITIVE_VERBS:
            return None, f"Unknown transitive verb: {verb}"

        subject_entity = "e1"
        object_entity = "e2"

        representation = [
            f"{subject}({subject_entity})",
            f"{obj}({object_entity})",
            f"{TRANSITIVE_VERBS[verb]}({subject_entity}, {object_entity})",
        ]

        return representation, None

    intransitive_match = INTRANSITIVE_PATTERN.fullmatch(normalized)

    if intransitive_match:
        subject, verb = intransitive_match.groups()

        if subject not in NOUNS:
            return None, f"Unknown subject noun: {subject}"

        if verb not in INTRANSITIVE_VERBS:
            return None, f"Unknown intransitive verb: {verb}"

        subject_entity = "e1"
        representation = [
            f"{subject}({subject_entity})",
            f"{INTRANSITIVE_VERBS[verb]}({subject_entity})",
        ]

        return representation, None

    return None, "Sentence does not match the supported sentence patterns"


data_path = Path("data/semantics_test.txt")
sentences = data_path.read_text(encoding="utf-8").splitlines()

print("=== SIMPLE SEMANTIC INTERPRETATION ===")
print()

supported_count = 0
unsupported_count = 0

for sentence in sentences:
    if not sentence.strip():
        continue

    representation, error = interpret(sentence)

    print("Sentence:", sentence)

    if representation is None:
        unsupported_count += 1
        print("Status: UNSUPPORTED")
        print("Reason:", error)
    else:
        supported_count += 1
        print("Status: INTERPRETED")
        print("Meaning:", " AND ".join(representation))

    print("-" * 60)

print()
print("=== SUMMARY ===")
print("Interpreted sentences:", supported_count)
print("Unsupported sentences:", unsupported_count)
