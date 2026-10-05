# Experiment 13 — Model Evaluation and Improvement

## Experiment 13 Results

The final test set contained 12 examples: six positive and six negative.

| System | Accuracy | Macro precision | Macro recall | Macro F1 |
|---|---:|---:|---:|---:|
| Majority-class baseline | 0.500 | 0.250 | 0.500 | 0.333 |
| Default TF-IDF + Logistic Regression | 1.000 | 1.000 | 1.000 | 1.000 |
| Tuned TF-IDF + Logistic Regression | 1.000 | 1.000 | 1.000 | 1.000 |

The tuned model's confusion matrix was:

| Actual \ Predicted | Negative | Positive |
|---|---:|---:|
| Negative | 6 | 0 |
| Positive | 0 | 6 |

The three-fold topic-grouped cross-validation produced a best macro F1 of `1.000`. The selected settings were:

- Logistic Regression regularization `C = 0.1`
- TF-IDF minimum document frequency `min_df = 1`
- Unigram and bigram features, `ngram_range = (1, 2)`
- Standard term frequency, `sublinear_tf = False`

The default and tuned models tied on the final test set. Hyperparameter tuning therefore did not increase test accuracy in this experiment, although it provided a systematic model-selection procedure.

### Development and Improvement Cycle

Experiments 11 and 12 used a 24-example dataset and a split that left the food, design, and product topics out of training. On that split, Naive Bayes and TF-IDF with Logistic Regression each achieved `0.333` accuracy, below the `0.500` majority baseline.

The first Experiment 13 development evaluation achieved `0.917` accuracy on 12 examples, with one positive service example misclassified. That split was treated as development data during the improvement process. A separate final test set was then reserved for the final evaluation.

The revised setup used a larger, topic-balanced development set, topic-grouped cross-validation for model selection, and a separate final test set. Both Logistic Regression systems classified all 12 final test examples correctly.

### Result Interpretation and Scope

The final results show that the systems learned sentiment cues that worked on this controlled dataset. The result does not establish that the model will achieve 100% accuracy on real-world reviews.

The data is small and manually written. The test sentences use clear sentiment words that also occur in development examples. The test set contains only 12 examples, so each prediction changes accuracy by about `0.083`. The scores describe this experiment and should not be treated as a general sentiment-classification benchmark.

---

## Experiment Setup

### Research Question

Does a topic-balanced dataset, topic-grouped cross-validation, and Logistic Regression model selection improve sentiment classification over a majority-class baseline?

### Dataset

The development data in `data/sentiment_dataset_evaluation.txt` contains 48 manually written examples:

- 24 positive and 24 negative examples
- Six topics: book, design, film, food, product, and service
- Eight examples per topic: four positive and four negative

The separate final test data in `data/sentiment_final_test.txt` contains 12 examples:

- Six positive and six negative
- One example of each class for each topic

### Methods Used

The experiment compared:

1. **Majority-class baseline:** predicts the most frequent label in development data. Since the development set was balanced, the predefined tie rule selected `negative`.
2. **Default TF-IDF + Logistic Regression:** uses scikit-learn's default classifier settings with TF-IDF features.
3. **Tuned TF-IDF + Logistic Regression:** selects settings by cross-validation on development data.

The tuned model was selected with three-fold `StratifiedGroupKFold` cross-validation, grouping by topic so that all examples from a topic stayed together within each validation fold. The model search varied word n-grams, minimum document frequency, sublinear term frequency, and Logistic Regression's regularization strength `C`.

The final test set was not used to fit the TF-IDF vocabulary, select hyperparameters, or train the model.

---

## Educational Guide: Methods for Building and Improving Text Classification Experiments

This section introduces the main practical methods used in small text-classification experiments. It is a guide to the methods most relevant to this bootcamp, not an exhaustive catalogue of every NLP technique.

### 1. Define the Task and Labels

Before collecting data, state exactly what the model should predict. For sentiment classification, define what counts as `positive` and `negative`, and decide how to handle neutral, mixed, sarcastic, or unclear examples.

Labels should be applied consistently. If two people could reasonably assign different labels, write annotation guidelines and review disagreements. A model cannot be evaluated reliably against inconsistent labels.

### 2. Build a Representative Dataset

A dataset should contain examples of the language and conditions expected at evaluation time.

Useful checks include:

- Number of examples per label
- Number of examples per topic or source
- Duplicate or near-duplicate texts
- Vocabulary coverage
- Clear and ambiguous examples
- Label balance and annotation consistency

Adding more examples is useful when it improves coverage. Adding only examples that resemble a known test error can overfit the development process. New examples should cover a range of topics, wording, and difficulty.

### 3. Split Data for Training and Evaluation

The split strategy should match the intended claim.

- **Random holdout:** reserves one portion for final evaluation. It is simple, but a small dataset can produce an unrepresentative split.
- **Stratified holdout:** preserves class proportions in each split. This helps prevent a test set from accidentally containing mostly one label.
- **Topic- or group-based split:** keeps related examples together. Use it when examples from the same author, document, topic, or source could otherwise appear in both training and testing.
- **Time-based split:** trains on earlier data and tests on later data when the intended use involves future texts.
- **K-fold cross-validation:** divides development data into folds, repeatedly trains on some folds and validates on the remaining fold. It uses limited data more efficiently than a single development split.
- **Repeated cross-validation:** repeats the fold process with different partitions to show how much results vary with the split.
- **Nested cross-validation:** uses an inner loop to select settings and an outer loop to estimate performance after selection. It is useful when data is limited and a separate final test set is unavailable.

This experiment used group-aware folds for model selection and a separate final test set. Stratifying by labels alone would not have guaranteed that each topic appeared in both training and testing.

### 4. Prevent Data Leakage

Data leakage occurs when information from validation or test examples influences model training or model selection.

Common safeguards include:

- Fit vocabulary and IDF values on training data only.
- Keep vectorization and model training together in a pipeline.
- Do not choose hyperparameters based on final-test performance.
- Do not repeatedly change the model after inspecting the final test errors.
- Keep duplicates and closely related versions of a text in the same split.
- If the final test is used to guide changes, treat it as development data and obtain a new untouched test set for the next final evaluation.

A high score is not trustworthy if information from the test set has influenced the model or the choices made during development.

### 5. Represent Text as Features

A classifier needs numerical features. Common text representations include:

- **Binary bag of words:** records whether each word occurs. It is simple and was used with Naive Bayes in Experiment 11.
- **Word counts:** records how often each word occurs.
- **TF-IDF:** weights a term by its frequency in a document and how uncommon it is across the training collection. It can make informative words more prominent than very common words.
- **Word n-grams:** use individual words or short sequences, such as unigrams and bigrams. Bigrams can preserve short phrases, though they create more features and can be sparse.
- **Character n-grams:** represent short character sequences. They can help with spelling variation, morphology, and unseen word forms.
- **Stemming or lemmatization:** normalize related forms, such as inflected words. This can reduce vocabulary size but may also remove useful distinctions.
- **Word or sentence embeddings:** represent text with dense vectors that capture semantic similarity. These usually require additional models or data and are beyond this small bootcamp dataset.

Feature choices should be fitted or learned using training data only. More features do not automatically produce a better model.

### 6. Choose a Baseline and Candidate Models

A baseline provides a reference point for deciding whether a more complex method learned something useful.

Common baselines include:

- **Majority class:** always predicts the most frequent training label.
- **Random baseline:** predicts labels using their training proportions.
- **Simple rule or lexicon baseline:** uses explicit rules or sentiment-word lists.
- **Previous model:** compares a new method with an earlier model on the same data split.

Common text classifiers include:

- **Multinomial Naive Bayes:** a fast probabilistic baseline that often works with word counts or binary features.
- **Logistic Regression:** a linear classifier that learns how features contribute to class probabilities or scores.
- **Linear Support Vector Machine:** a linear margin-based classifier that is often effective for sparse text features.
- **SGD-based linear classifiers:** train linear models with stochastic gradient descent and can scale to larger datasets.
- **Decision trees and ensembles:** can model interactions but may overfit small, sparse text datasets unless carefully controlled.
- **Neural models and pretrained language models:** can capture richer context, but require more data, compute, and careful evaluation. They are not automatically suitable for tiny datasets.

A useful experiment compares a small number of methods chosen for a reason, rather than trying many models without a clear evaluation plan.

### 7. Tune Hyperparameters Using Development Data

Hyperparameters control the learning process but are not learned directly as model weights. Examples include:

- Logistic Regression `C`, which controls regularization strength
- Minimum term frequency for including vocabulary items
- Word n-gram range
- Whether term frequency is scaled sublinearly
- Class weighting for imbalanced data
- Decision threshold for converting scores or probabilities into labels

**Grid search** evaluates a predefined set of combinations. **Randomized search** samples combinations from larger ranges and can be more efficient for broad searches.

Search settings should be selected using cross-validation on development data. The final test set should be evaluated only after the choices are fixed.

### 8. Evaluate with More Than Accuracy

Let true positives (TP) be positive examples correctly predicted as positive, true negatives (TN) negative examples correctly predicted as negative, false positives (FP) negative examples predicted as positive, and false negatives (FN) positive examples predicted as negative.

- **Accuracy:** `(TP + TN) / all examples`. It is intuitive but can hide poor performance on a minority class.
- **Precision:** `TP / (TP + FP)`. Of the examples predicted positive, how many were actually positive?
- **Recall:** `TP / (TP + FN)`. Of the actual positive examples, how many did the model find?
- **F1:** the harmonic mean of precision and recall. It is useful when both matter.
- **Macro average:** calculates a metric separately for each class and gives each class equal weight. This is useful when class balance matters.
- **Weighted average:** averages class metrics weighted by the number of examples in each class.
- **Confusion matrix:** shows actual labels against predicted labels and makes error types visible.
- **ROC-AUC or PR-AUC:** evaluate ranking across thresholds. PR-AUC is often informative when the positive class is rare, but both require enough data and careful interpretation.

Choose metrics based on the task. If missing positive cases is costly, recall may matter more; if false alarms are costly, precision may matter more. Always report class-level results when aggregate accuracy could hide imbalance.

### 9. Inspect Errors and Improve the Right Part

For incorrect predictions, inspect:

- Whether the text contains words absent from training vocabulary
- Whether the label is ambiguous or possibly incorrect
- Whether negation, sarcasm, or mixed sentiment is present
- Whether a topic or source is missing from training
- Whether preprocessing removed meaningful words
- Which features and model scores contributed to the decision

Then decide whether the problem is mainly data coverage, label quality, representation, model choice, or the evaluation split. Improve the relevant part, retrain using development data, and retain a final test set that has not guided those changes.

### 10. Make the Experiment Reproducible

Record:

- Dataset files and label definitions
- How the data was split and the random seed
- Which features and preprocessing steps were used
- The model and its hyperparameters
- Package versions
- Metrics, confusion matrix, and representative errors
- Limitations and the scope of the conclusion

In small datasets, repeat splits or cross-validation can reveal instability. A single accuracy score should not be presented without the test-set size and class distribution.

---

## Recommended Workflow for Future Experiments

1. Define the research question and labels.
2. Inspect the dataset and check class, topic, and source coverage.
3. Create a simple baseline.
4. Choose a split strategy that matches the intended evaluation.
5. Fit preprocessing only on training data.
6. Compare a small number of justified models.
7. Tune settings with development data or cross-validation.
8. Evaluate the final chosen model once on untouched test data.
9. Report per-class metrics and inspect errors.
10. State what the dataset supports and what it cannot establish.

## Conclusion

Experiment 13 improved the evaluation design and achieved perfect scores on its 12-example final test set with both default and tuned TF-IDF Logistic Regression. The majority baseline achieved 0.500 accuracy. Grouped cross-validation selected a model with macro F1 `1.000`.

The experiment demonstrates a complete model-evaluation cycle: use a baseline, inspect a development error, improve topic coverage, tune only on development data, preserve a final test set, and report several complementary metrics. Its perfect final score is specific to this small, controlled dataset and should not be generalized to real-world sentiment classification.

## Files

- `data/sentiment_dataset_evaluation.txt` — development examples
- `data/sentiment_final_test.txt` — separate final test examples
- `src/model_evaluation.py` — cross-validation, model selection, metrics, and final predictions
- `results/experiment_13_model_evaluation.md` — experiment results and educational guide
- `requirements.txt` — Python package dependencies
