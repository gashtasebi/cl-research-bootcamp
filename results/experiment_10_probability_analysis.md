# Experiment 10 — Probability and Quantitative Analysis

## Research Question

How does conditioning on a document containing the word `project` change the empirical probability that the document also contains `data`?

## Hypothesis

In this corpus, the conditional probability `P(data | project)` will be greater than the marginal document probability `P(data)`.

## Dataset

The experiment used `data/corpus.txt`. Each non-empty line was treated as one document.

The corpus contained:

| Statistic | Value |
|---|---:|
| Documents | 6 |
| Tokens | 49 |
| Vocabulary size | 38 |

Tokens were lowercased and extracted with a simple alphabetic regular expression.

## Method

The program calculated token frequency, relative token frequency, document frequency, and document-level empirical probabilities.

Two events were defined:

- `D`: a randomly selected document contains the whole-word token `data`.
- `R`: a randomly selected document contains the whole-word token `project`.

The following probabilities were calculated:

- `P(data)`: proportion of all documents containing `data`.
- `P(project)`: proportion of all documents containing `project`.
- `P(data AND project)`: proportion of all documents containing both terms.
- `P(data | project)`: proportion of documents containing `project` that also contain `data`.

Token relative frequency and document probability measure different things. Token relative frequency samples from all tokens, while document probability samples from documents and checks whether a term occurs at least once.

## Results

The token-level frequency of `data` was 3 out of 49 tokens:

- Relative token frequency of `data`: `3 / 49 = 0.061`
- Document frequency of `data`: 3 documents
- Document probability `P(data)`: `3 / 6 = 0.500`

The token-level frequency of `project` was 1 out of 49 tokens:

- Relative token frequency of `project`: `1 / 49 = 0.020`
- Document frequency of `project`: 1 document
- Document probability `P(project)`: `1 / 6 = 0.167`

The joint and conditional document probabilities were:

| Probability | Calculation | Result |
|---|---:|---:|
| `P(data)` | 3 / 6 | 0.500 |
| `P(project)` | 1 / 6 | 0.167 |
| `P(data AND project)` | 1 / 6 | 0.167 |
| `P(data \| project)` | 1 / 1 | 1.000 |

## Interpretation

The results support the hypothesis for this corpus: `P(data | project)` was `1.000`, which is greater than the marginal probability `P(data)`, which was `0.500`.

This means that the only document containing `project` also contained `data`. It does not mean that every document about projects in general will contain the word `data`. The conditional estimate is based on a single document containing `project`, so one additional document could change it substantially.

The experiment also illustrates why the sampling unit must be specified. The probability of selecting the token `data` from all tokens was `0.061`, while the probability of selecting a document that contains `data` was `0.500`. These are different probabilities because they use different sample spaces.

## Limitations

The corpus contains only six documents, and only one contains `project`. The probabilities are descriptive empirical estimates for this small corpus and are highly sensitive to individual documents.

The calculation uses exact whole-word matches after lowercasing. It does not account for synonyms, related terms, topic similarity, or document length. No statistical significance test was performed.

## Conclusion

Experiment 10 calculated corpus statistics and empirical probabilities at both token and document levels. In this corpus, `P(data)` was `0.500`, while `P(data | project)` was `1.000`. The conditional probability was higher because the single document containing `project` also contained `data`.

The experiment demonstrates relative frequency, document frequency, joint probability, and conditional probability. It also shows why estimates from very small corpora should be interpreted cautiously and should not be generalized beyond the observed data.

## Files

- `data/corpus.txt` — corpus analyzed as six documents
- `src/probability_analysis.py` — corpus statistics and probability calculations
- `results/experiment_10_probability_analysis.md` — experiment report
