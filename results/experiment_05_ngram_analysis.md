# Experiment 5 — N-gram Analysis and Laplace Smoothing

## Objective

The objective of this experiment is to analyze unigram and bigram frequencies, calculate conditional bigram probabilities, investigate the zero-probability problem caused by unseen bigrams, and evaluate the effect of Laplace smoothing.

This experiment extends the previous n-gram analysis by comparing probability estimates before and after smoothing.

---

## Experimental Pipeline

The complete workflow of Experiment 5 is:

```text
Corpus
  ↓
Tokenization
  ↓
Unigram Analysis
  ↓
Bigram Analysis
  ↓
Frequency Analysis
  ↓
Sentence Boundaries
  ↓
Conditional Probability
  ↓
Zero Probability Problem
  ↓
Laplace Smoothing
  ↓
Comparison
```

---

## Conditional Bigram Probability

For a bigram consisting of two consecutive words, the conditional probability is calculated as:

```text
P(w₂ | w₁) = Count(w₁, w₂) / Count(w₁)
```

This represents the probability of observing `w₂` given that `w₁` has already occurred.

For example:

```text
P(studying | are)
```

represents the probability that `studying` follows `are`.

---

## Zero Probability Problem

Without smoothing, an unseen bigram receives a probability of zero.

For example:

```text
P(is | students) = 0.0000
P(is | cats)     = 0.0000
```

This occurs because the corresponding bigrams do not appear in the training corpus.

Zero probabilities are problematic for language models because when probabilities are multiplied across a sequence, a single zero probability can make the probability of the entire sequence equal to zero.

---

## Laplace Smoothing

To address the zero-probability problem, Laplace (add-one) smoothing was applied.

The smoothed conditional probability is calculated as:

```text
P_Laplace(w₂ | w₁) =
    (Count(w₁, w₂) + 1) /
    (Count(w₁) + V)
```

where `V` is the vocabulary size.

Laplace smoothing assigns a small non-zero probability to every possible bigram, including bigrams that were not observed in the corpus.

---

## Smoothing Comparison

The following table compares the original conditional probabilities with their Laplace-smoothed values:

| Bigram | Without Smoothing | Laplace |
|---|---:|---:|
| `P(studying \| are)` | 0.5000 | 0.0625 |
| `P(students \| the)` | 0.2500 | 0.0588 |
| `P(is \| students)` | 0.0000 | 0.0323 |
| `P(is \| cats)` | 0.0000 | 0.0323 |

---

## Results

The experiment demonstrates three important effects of Laplace smoothing.

### 1. Unseen bigrams receive non-zero probabilities

Before smoothing:

```text
P(is | students) = 0.0000
P(is | cats)     = 0.0000
```

After Laplace smoothing:

```text
P(is | students) = 0.0323
P(is | cats)     = 0.0323
```

Therefore, Laplace smoothing successfully eliminates zero probabilities for unseen bigrams.

### 2. Observed bigrams receive lower probabilities

The probabilities of observed bigrams are reduced after smoothing.

For example:

```text
P(studying | are)
Original: 0.5000
Laplace:  0.0625
```

and:

```text
P(students | the)
Original: 0.2500
Laplace:  0.0588
```

This happens because Laplace smoothing distributes some probability mass to previously unseen bigrams.

### 3. The effect can be strong in a small corpus

The reduction in probability is particularly noticeable in this experiment because the corpus and vocabulary are relatively small.

For example, the probability of:

```text
P(studying | are)
```

decreases from:

```text
0.5000 → 0.0625
```

This shows that Laplace smoothing can substantially alter probability estimates when applied to a small dataset.

---

## Interpretation

The experiment demonstrates the fundamental trade-off introduced by Laplace smoothing.

Without smoothing, observed bigrams can receive relatively high probabilities, but unseen bigrams receive a probability of zero.

With Laplace smoothing, every possible bigram receives a non-zero probability. This makes the model more robust when encountering word sequences that were not present in the training corpus.

However, the probability mass assigned to unseen events must come from somewhere. As a result, the probabilities of observed bigrams are reduced.

For small corpora, this redistribution can be relatively large and may lead to probability estimates that are less representative of the observed frequencies.

---

## Key Findings

The main findings of Experiment 5 are:

1. **Laplace smoothing eliminates zero probabilities.**
2. **Previously unseen bigrams receive small non-zero probabilities.**
3. **Observed bigram probabilities decrease after smoothing.**
4. **The effect of smoothing can be substantial in a small corpus.**
5. **Laplace smoothing provides a simple solution to the zero-probability problem, but it may over-smooth small datasets.**

---

## Conclusion

Experiment 5 completed the n-gram probability analysis by introducing and evaluating Laplace smoothing.

The results demonstrate that smoothing solves the zero-probability problem by assigning a non-zero probability to unseen bigrams. At the same time, it reduces the probabilities of bigrams that were observed in the corpus.

Therefore, Laplace smoothing represents a trade-off between handling unseen events and preserving the empirical probability distribution of the training corpus.

The experiment provides a complete progression from corpus preprocessing and n-gram frequency analysis to conditional probability, zero-probability detection, smoothing, and quantitative comparison.

---

## Experiment Status

**Experiment 5: Complete**

The following concepts have been covered:

- Corpus preparation
- Tokenization
- Unigram frequency analysis
- Bigram frequency analysis
- Sentence boundaries
- Conditional probability
- Zero-probability problem
- Laplace smoothing
- Comparison of smoothed and unsmoothed probabilities
- Interpretation of smoothing effects
