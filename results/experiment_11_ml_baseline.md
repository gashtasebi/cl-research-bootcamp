# Experiment 11 — Machine Learning Baseline

## Research Question

Can a simple Naive Bayes text classifier outperform a majority-class baseline on a small positive/negative sentiment dataset?

## Hypothesis

A Naive Bayes classifier using word-presence features will achieve higher accuracy than a baseline that always predicts the majority training label.

## Dataset

The experiment used 24 manually written short review texts in `data/sentiment_dataset.txt`:

- 12 positive examples
- 12 negative examples

Each line contains a label and a text separated by `|`.

## Method

The data was split into training and test sets separately for each class, using a 75/25 split and random seed 42. This stratified split produced:

| Split | Negative | Positive | Total |
|---|---:|---:|---:|
| Training | 9 | 9 | 18 |
| Test | 3 | 3 | 6 |

Each text was represented with binary word-presence features: a feature indicates whether a word occurs in the text. An NLTK Naive Bayes classifier was trained using only the training examples.

The baseline predicted the most frequent training label for every test item. The training labels were tied, so the predefined tie rule selected `negative`.

Accuracy was calculated as the number of correct predictions divided by the number of test examples.

## Results

| System | Correct predictions | Test accuracy |
|---|---:|---:|
| Naive Bayes | 2 / 6 | 0.333 |
| Majority-class baseline | 3 / 6 | 0.500 |

Naive Bayes performed below the majority-class baseline on this test split. It predicted the positive class for five of the six test texts. This included all three negative examples, which were therefore misclassified as positive.

## Error Analysis

All three test topics—food, design, and product—were absent from the training examples. For example, the model had not seen training texts about food, so it had no training evidence for words such as `delicious`, `disgusting`, `fresh`, or `stale` in that topic. The same topic separation occurred for design and product.

The split preserved the positive/negative class proportions, but it did not ensure that topics or vocabulary were represented in both training and test sets. The resulting test set therefore challenged the model with topic-specific words it had not encountered during training.

## Interpretation

The hypothesis was not supported: Naive Bayes did not outperform the majority-class baseline on this held-out test split.

The result illustrates that training a classifier does not guarantee better performance than a simple baseline. A small dataset and a split with topic-specific vocabulary held out can limit how well word-based features generalize. The baseline's 0.500 accuracy reflects the balanced test set and its constant negative prediction.

## Limitations

The dataset contains only 24 manually written texts, and the test set contains only six. Each test example changes accuracy by approximately 0.167, so the estimate is unstable.

The result comes from one random seed and one split. The dataset was also deliberately small and does not represent a broad range of sentiment language or topics. No claim about general sentiment-classification performance can be made from this experiment.

## Conclusion

Experiment 11 implemented a stratified train/test split, binary word-presence features, an NLTK Naive Bayes classifier, and a majority-class baseline.

On the six test examples, Naive Bayes achieved 0.333 accuracy, while the baseline achieved 0.500. The experiment therefore did not confirm the hypothesis. The held-out topics and limited training data provide a plausible explanation for the classifier's errors and demonstrate why baselines, split design, and dataset size matter.

## Files

- `data/sentiment_dataset.txt` — labeled sentiment texts
- `src/ml_baseline.py` — stratified split, feature extraction, model training, prediction, and baseline comparison
- `results/experiment_11_ml_baseline.md` — experiment report
