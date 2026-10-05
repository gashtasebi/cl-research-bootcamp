from pathlib import Path
import re


# Each entry describes a known discourse entity's type and, when known, gender.
ENTITY_INFO = {
    "john": {"type": "person", "gender": "masculine", "label": "John"},
    "mary": {"type": "person", "gender": "feminine", "label": "Mary"},
    "alice": {"type": "person", "gender": "feminine", "label": "Alice"},
    "bob": {"type": "person", "gender": "masculine", "label": "Bob"},
    "student": {"type": "person", "gender": "unknown", "label": "student"},
    "teacher": {"type": "person", "gender": "unknown", "label": "teacher"},
    "dog": {"type": "animal", "gender": "unknown", "label": "dog"},
    "cat": {"type": "animal", "gender": "unknown", "label": "cat"},
    "book": {"type": "object", "gender": "unknown", "label": "book"},
}

PRONOUN_CONSTRAINTS = {
    "he": {"type": "person", "gender": "masculine"},
    "him": {"type": "person", "gender": "masculine"},
    "she": {"type": "person", "gender": "feminine"},
    "her": {"type": "person", "gender": "feminine"},
    "they": {"type": "person", "gender": None},
    "it": {"type": {"animal", "object"}, "gender": None},
}


def extract_entities(first_sentence):
    """Find known entity mentions in order and assign discourse referents."""
    words = re.findall(r"\b[A-Za-z]+\b", first_sentence.lower())
    entities = []

    for word in words:
        if word in ENTITY_INFO:
            info = ENTITY_INFO[word]
            entities.append({
                "id": f"e{len(entities) + 1}",
                "label": info["label"],
                "type": info["type"],
                "gender": info["gender"],
            })

    return entities


def is_compatible(pronoun, entity):
    """Check whether an entity satisfies the pronoun's type/gender constraints."""
    constraints = PRONOUN_CONSTRAINTS[pronoun]

    allowed_type = constraints["type"]
    if isinstance(allowed_type, set):
        if entity["type"] not in allowed_type:
            return False
    elif entity["type"] != allowed_type:
        return False

    required_gender = constraints["gender"]
    if required_gender is not None:
        if entity["gender"] != required_gender:
            return False

    return True


def read_gold_annotations(path):
    """Load the manually written reference links and ambiguity labels."""
    annotations = {}

    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue

        discourse_number_text, annotation_text = line.split(":", maxsplit=1)
        discourse_number = int(discourse_number_text.strip())
        annotations[discourse_number] = {}

        for item in annotation_text.split(";"):
            pronoun, target = item.split("->", maxsplit=1)
            pronoun = pronoun.strip().lower()
            target = target.strip()

            if target.upper().startswith("AMBIGUOUS:"):
                candidates_text = target.split(":", maxsplit=1)[1]
                candidates = {
                    name.strip().lower()
                    for name in candidates_text.split(",")
                }
                annotations[discourse_number][pronoun] = {
                    "kind": "ambiguous",
                    "candidates": candidates,
                }
            else:
                annotations[discourse_number][pronoun] = {
                    "kind": "entity",
                    "entity": target.lower(),
                }

    return annotations


def format_entity(entity):
    """Format one entity for display in the discourse representation."""
    properties = [entity["type"]]

    if entity["gender"] != "unknown":
        properties.append(entity["gender"])

    return f'{entity["id"]} = {entity["label"]} ({", ".join(properties)})'


data_path = Path("data/discourse_test.txt")
gold_path = Path("data/discourse_gold.txt")

discourses = [
    line.strip()
    for line in data_path.read_text(encoding="utf-8").splitlines()
    if line.strip()
]
gold_annotations = read_gold_annotations(gold_path)

pronoun_pattern = re.compile(
    r"\b(he|him|she|her|they|it)\b",
    re.IGNORECASE,
)

total_decisions = 0
correct_decisions = 0

print("=== DISCOURSE REPRESENTATION AND COREFERENCE ===")
print()

for discourse_number, discourse in enumerate(discourses, start=1):
    if "|" not in discourse:
        print(f"Discourse {discourse_number}: invalid format; expected '|'.")
        continue

    first_sentence, second_sentence = [
        part.strip() for part in discourse.split("|", maxsplit=1)
    ]

    entities = extract_entities(first_sentence)
    pronouns = [
        match.group(1).lower()
        for match in pronoun_pattern.finditer(second_sentence)
    ]

    print(f"Discourse {discourse_number}")
    print("Text:", discourse)
    print("DRS-style representation:")

    if entities:
        print("  Referents:")
        for entity in entities:
            print("   -", format_entity(entity))
    else:
        print("  Referents: none recognized")

    conditions = []

    for entity in entities:
        conditions.append(f'{entity["type"]}({entity["id"]})')

        if entity["gender"] == "masculine":
            conditions.append(f'masculine({entity["id"]})')
        elif entity["gender"] == "feminine":
            conditions.append(f'feminine({entity["id"]})')

    discourse_gold = gold_annotations.get(discourse_number, {})

    if pronouns:
        print("  Pronoun references:")

    for pronoun in pronouns:
        compatible_entities = [
            entity
            for entity in entities
            if is_compatible(pronoun, entity)
        ]

        if compatible_entities:
            nearest_entity = compatible_entities[-1]
            candidate_labels = [entity["label"] for entity in compatible_entities]

            print(
                f"   - {pronoun} -> nearest candidate: "
                f'{nearest_entity["label"]} ({nearest_entity["id"]})'
            )

            if len(compatible_entities) > 1:
                print(
                    "     Potential ambiguity; compatible candidates:",
                    ", ".join(candidate_labels),
                )
                candidate_ids = ", ".join(
                    entity["id"] for entity in compatible_entities
                )
                conditions.append(
                    f"possible-reference({pronoun}, {candidate_ids})"
                )
            else:
                conditions.append(
                    f'{pronoun} = {nearest_entity["id"]}'
                )
        else:
            nearest_entity = None
            candidate_labels = []
            print(f"   - {pronoun} -> no compatible antecedent found")

        expected = discourse_gold.get(pronoun)
        if expected is not None:
            total_decisions += 1

            if expected["kind"] == "ambiguous":
                actual_candidates = {
                    label.lower() for label in candidate_labels
                }
                is_correct = (
                    len(compatible_entities) > 1
                    and actual_candidates == expected["candidates"]
                )
                expected_text = "ambiguity among " + ", ".join(
                    sorted(expected["candidates"])
                )
            else:
                is_correct = (
                    nearest_entity is not None
                    and nearest_entity["label"].lower()
                    == expected["entity"]
                )
                expected_text = expected["entity"]

            if is_correct:
                correct_decisions += 1
                evaluation = "CORRECT"
            else:
                evaluation = "INCORRECT"

            print(
                f"     Gold: {expected_text} | "
                f"Evaluation: {evaluation}"
            )

    print("  Conditions:")
    if conditions:
        for condition in conditions:
            print("   -", condition)
    else:
        print("   - none")

    print("-" * 60)

print()
print("=== EVALUATION SUMMARY ===")
print("Pronoun decisions evaluated:", total_decisions)
print("Correct decisions:", correct_decisions)
print("Incorrect decisions:", total_decisions - correct_decisions)

if total_decisions:
    accuracy = correct_decisions / total_decisions
    print(f"Accuracy: {accuracy:.3f}")
