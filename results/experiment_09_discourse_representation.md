# Experiment 9 — Discourse Representation and Coreference

## Research Question

Can a simple rule-based resolver use entity type, gender information, and recency to link pronouns to discourse entities, while identifying cases with multiple compatible antecedents?

## Hypothesis

Pronouns with a single compatible antecedent will be linked to that entity. When several entities satisfy the implemented compatibility constraints, the system will report the candidate set and identify potential ambiguity.

## Dataset

The experiment used six short two-sentence discourses in `data/discourse_test.txt`. The manually written reference annotations are stored in `data/discourse_gold.txt`.

The examples contain:

- Named people with known gender in the small lexicon
- Common nouns classified as people, animals, or objects
- Pronouns including `he`, `her`, `they`, and `it`
- One deliberately ambiguous case: `John met Bob. | He smiled.`

The gold annotations specify the intended referent for clear examples and list both possible antecedents for the deliberately ambiguous example.

## Method

The program extracts recognized entities from the first sentence of each discourse and assigns them identifiers such as `e1` and `e2`. It records the entity type and, for names with a known value, gender information.

For each pronoun in the second sentence, the resolver applies simple compatibility constraints:

- `he` and `him` require a masculine person.
- `she` and `her` require a feminine person.
- `they` is treated as compatible with any person in the lexicon.
- `it` is treated as compatible with animals and objects.

The program lists all compatible antecedents and selects the most recently introduced compatible entity as its simple recency baseline. When more than one candidate is compatible, it reports the candidate set as a potential ambiguity.

The output is a small DRS-style representation containing discourse referents, type/gender conditions, and pronoun-reference conditions. The program compares its decisions with the manually written annotations in `data/discourse_gold.txt`.

## Results

| Measure | Result |
|---|---:|
| Discourse items | 6 |
| Pronoun decisions evaluated | 9 |
| Correct decisions | 9 |
| Incorrect decisions | 0 |
| Accuracy on this dataset | 1.000 |

The resolver reported multiple compatible antecedents in three cases:

- `It` in `A dog chased a cat. | It ran away.` — compatible candidates: dog and cat; the nearest candidate, cat, matched the gold annotation.
- `They` in `A teacher spoke to a student. | They listened.` — compatible candidates: teacher and student; the nearest candidate, student, matched the gold annotation.
- `He` in `John met Bob. | He smiled.` — compatible candidates: John and Bob; this matched the gold annotation that the reference is ambiguous.

## Interpretation

The results show how discourse referents can persist across sentence boundaries. The identifiers `e1` and `e2` represent entities introduced in the first sentence, while pronoun conditions connect later mentions to those entities.

The gender and entity-type constraints filtered candidate antecedents in examples such as `He greeted her` and `They read it`. Recency then selected the most recently introduced compatible entity in clear cases.

The final discourse demonstrates an important distinction between a resolver's preferred candidate and a uniquely determined reference. Both John and Bob satisfy the implemented constraints for `He`. The system therefore reports the candidate set as ambiguous, even though Bob is the nearest candidate.

## Limitations

The dataset contains only six manually constructed discourses and nine pronoun decisions. The lexicon and compatibility rules were designed for these examples, and the annotations are not an independently collected benchmark. The accuracy score therefore describes only this small dataset and does not establish general coreference performance.

The entity-type categories are coarse. Singular `they` is treated as compatible with any person, and `it` is treated as compatible with animals or objects. The program does not use verb meaning, broader world knowledge, syntactic binding constraints, or information from a larger discourse.

The representation is a small DRS-style structure focused on entities and reference. It does not provide a full semantic analysis of events, quantifiers, or discourse-wide inference.

## Conclusion

Experiment 9 implemented a basic discourse representation and pronoun resolver. It introduced entity identifiers, recorded simple entity properties, linked pronouns to compatible antecedents, and reported cases with multiple possible antecedents.

All nine decisions matched the manual annotations for this controlled dataset. The experiment demonstrates how type constraints and recency can support coreference resolution, while also showing that multiple compatible entities can leave a pronoun ambiguous.

## Files

- `data/discourse_test.txt` — short discourse examples
- `data/discourse_gold.txt` — manually written reference annotations
- `src/discourse_representation.py` — entity representation, pronoun resolution, and evaluation
- `results/experiment_09_discourse_representation.md` — experiment report
