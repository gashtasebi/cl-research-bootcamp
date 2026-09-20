# Experiment 3 — Standard NLP Tokenization and Evaluation

## Objective

The objective of this experiment was to compare a standard NLP
tokenizer with a manually defined Gold Standard.

The experiment also demonstrates how tokenization systems can
be evaluated quantitatively.

---

## Dataset

The experiment uses a small manually created test dataset
containing linguistically difficult expressions.

The test cases include:

- Abbreviations
- Decimal numbers
- URLs
- Email addresses
- Hyphenated expressions
- Contractions
- Uppercase abbreviations

---

## Gold Standard

The Gold Standard contains 38 manually defined tokens.

The following decisions were made for this experiment:

- `Dr.` is one token.
- `12.50` is one token.
- `https://example.com` is one token.
- `test@example.com` is one token.
- `state-of-the-art` is one token.
- `isn't` is one token.

These decisions define what counts as a token for this
specific experiment.

---

## System

The standard NLP tokenizer used in this experiment is:

**NLTK word_tokenize**

The tokenizer produced:

**43 tokens**

---

## Evaluation

The evaluation was performed using token spans in the
original text.

### Results

| Metric | Result |
|---|---:|
| Gold tokens | 38 |
| NLTK tokens | 43 |
| True Positives | 35 |
| False Positives | 8 |
| False Negatives | 3 |
| Precision | 0.814 |
| Recall | 0.921 |
| F1 Score | 0.864 |

---

## Error Analysis

The tokenizer handled several expressions correctly.

Examples include:

- `Dr.`
- `12.50`
- `state-of-the-art`

However, some expressions were split differently from
the Gold Standard.

### URL

Gold Standard:

`https://example.com`

NLTK:

`https`
`:`
`//example.com`

### Email

Gold Standard:

`test@example.com`

NLTK separates the components of the email address.

### Contraction

Gold Standard:

`isn't`

NLTK produces:

`is`
`n't`

---

## Interpretation

On this small manually annotated test dataset, the NLTK
tokenizer achieved:

- Precision: 0.814
- Recall: 0.921
- F1: 0.864

The results show that the tokenizer agrees substantially
with the Gold Standard, but also produces additional token
boundaries for some linguistic expressions.

The results should not be interpreted as a general benchmark
for NLTK. They describe the behavior of NLTK on this specific
dataset and under the tokenization decisions defined by this
experiment.

---

## Research Observation

Tokenization is not completely independent of the NLP task.

Different applications may require different tokenization
decisions.

For example, an NLP system working with web documents may
want URLs and email addresses to remain intact, while another
system may intentionally split them into smaller units.

Therefore, a tokenizer should be evaluated against a clearly
defined annotation scheme and task-specific Gold Standard.

---

## Methodological Lesson

This experiment demonstrated the following research workflow:

1. Define a linguistic problem.
2. Create a small test dataset.
3. Define a Gold Standard.
4. Apply an NLP method.
5. Compare system output with the Gold Standard.
6. Identify errors.
7. Calculate evaluation metrics.
8. Interpret the results.
9. Document methodological limitations.

---

## Conclusion

The experiment demonstrated that a standard NLP tokenizer
can handle many linguistic patterns but does not necessarily
follow the tokenization decisions defined by a particular
Gold Standard.

The experiment also showed why evaluation metrics must be
combined with qualitative error analysis.
