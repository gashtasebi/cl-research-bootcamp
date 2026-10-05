# Experiment 12 — TF-IDF Text Classification

## Research Question

Can TF-IDF features combined with Logistic Regression outperform a majority-class baseline on the sentiment dataset used in Experiment 11?

## Hypothesis

A Logistic Regression classifier trained on TF-IDF features will achieve higher accuracy than the majority-class baseline on the held-out test set.

## Dataset

The experiment reused the 24 manually written positive and negative texts in `data/sentiment_dataset.txt`:

- 12 positive examples
- 12 negative examples

To make the result directly comparable with Experiment 11, the same stratified 75/25 split and random seed 42 were used.

| Split | Negative | Positive | Total |
|---|---:|---:|---:|
| Training | 9 | 9 | 18 |
| Test | 3 | 3 | 6 |

## Method

`TfidfVectorizer` converted each text into a numerical feature vector. TF-IDF gives higher weight to terms that are informative within a document and lower weight to terms that occur across many documents.

The vectorizer was fitted only on the training texts. The held-out test texts were transformed using the vocabulary learned from training data. The resulting matrices had these shapes:

- Training matrix: 18 documents × 56 features
- Test matrix: 6 documents × 56 features

A Logistic Regression classifier was trained on the training feature matrix. Its accuracy was compared with a majority-class baseline that always predicted `negative`, the fixed tie choice for the balanced training set.

## Results

| System | Correct predictions | Accuracy |
|---|---:|---:|
| TF-IDF + Logistic Regression | 2 / 6 | 0.333 |
| Majority-class baseline | 3 / 6 | 0.500 |
| Naive Bayes, Experiment 11 | 2 / 6 | 0.333 |

The Logistic Regression model performed below the majority baseline and matched the Naive Bayes accuracy from Experiment 11 on this split.

## Error Analysis

All three test topics—food, design, and product—were absent from the training examples. The test texts therefore contained topic-specific words that were not in the training vocabulary.

For example, the first test text was:

`The food tastes delicious and fresh.`

Its non-zero TF-IDF features were only `the` and `and`. The terms specific to the topic and sentiment, including `food`, `tastes`, `delicious`, and `fresh`, were not represented in the training vocabulary. This left the classifier with little useful evidence for distinguishing the positive example from the negative food review.

A similar topic separation occurred for design and product examples. This indicates that the model had difficulty generalizing to test vocabulary from topics that were not represented during training.

## Interpretation

The hypothesis was not supported. TF-IDF with Logistic Regression achieved 0.333 accuracy, below the 0.500 majority baseline.

TF-IDF can weight terms only when they are present in its fitted vocabulary. It cannot learn sentiment weights for words that occur only in the test set. The result is consistent with the topic and vocabulary separation in this particular split.

The same split makes comparison with Experiment 11 possible. On this test set, TF-IDF with Logistic Regression matched Naive Bayes but neither model beat the majority baseline.

## Limitations

The dataset contains only 24 short texts, and the test set contains six. Each prediction changes test accuracy by about 0.167, making the estimate unstable.

The experiment used one split and one random seed. Stratification preserved class proportions but did not ensure that topics or sentiment vocabulary appeared in both training and test sets. The results therefore describe this split and dataset only; they do not measure general sentiment-classification performance.

## Conclusion

Experiment 12 implemented TF-IDF feature extraction and Logistic Regression with scikit-learn, using the same train/test split as Experiment 11. The model achieved 0.333 accuracy, matching Naive Bayes and performing below the 0.500 majority baseline.

The feature inspection showed that the first test text had only two terms represented in the training vocabulary. The experiment demonstrates that TF-IDF creates numerical text features, while also showing that a model cannot use informative terms it did not encounter during training. Dataset coverage and split design strongly affected this small experiment.

## Files

- `data/sentiment_dataset.txt` — labeled sentiment texts
- `src/tfidf_logistic_regression.py` — TF-IDF features, Logistic Regression, and baseline comparison
- `results/experiment_12_tfidf_classification.md` — experiment report
- `requirements.txt` — recorded Python package dependencies
