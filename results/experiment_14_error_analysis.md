# Experiment 14: Error Analysis

## 1. Research Question

Which linguistic phenomena cause errors for the TF-IDF and Logistic Regression sentiment classifier developed in Experiment 13?

This experiment examines four phenomena:

- Negation
- Contrastive sentences
- Sarcasm and irony
- Sentiment expressed with lexical items that were not present in the development data

The goal is to diagnose model behavior on carefully selected examples, not to estimate general performance.

## 2. Method

The tuned TF-IDF and Logistic Regression settings from Experiment 13 were kept fixed. The model was trained on the 48-example development dataset and evaluated on a separate challenge set containing 16 examples.

The challenge set was balanced by sentiment:

- 8 positive examples
- 8 negative examples

It was also balanced by phenomenon, with 4 examples in each category. The challenge examples were not used to fit the model or select its settings.

A majority-class baseline that always predicts the negative class was included for comparison. Evaluation used accuracy, precision, recall, macro F1, a confusion matrix, and item-level predictions. The analysis also inspected unseen words and the strongest feature contributions for misclassified examples.

## 3. Overall Results

| Model | Accuracy | Macro F1 |
|---|---:|---:|
| Majority-class baseline | 0.500 | 0.333 |
| Tuned TF-IDF + Logistic Regression | 0.438 | 0.435 |

The classifier made 7 errors among the 16 challenge examples. It correctly classified 4 of 8 negative examples and 3 of 8 positive examples.

The confusion matrix was:

| Actual class | Predicted negative | Predicted positive |
|---|---:|---:|
| Negative | 4 | 4 |
| Positive | 5 | 3 |

On this deliberately difficult set, the classifier scored below the majority baseline in accuracy. The small challenge set was designed to expose specific weaknesses, so these figures should not be interpreted as an estimate of performance on ordinary sentiment data.

## 4. Results by Phenomenon

| Phenomenon | Correct | Accuracy | Errors |
|---|---:|---:|---:|
| Contrast | 3/4 | 0.750 | 1 |
| Lexical shift | 2/4 | 0.500 | 2 |
| Negation | 0/4 | 0.000 | 4 |
| Sarcasm | 2/4 | 0.500 | 2 |

Negation caused the most consistent failure: all four negated examples were misclassified. The classifier often relied on a sentiment-bearing word while failing to represent how the word's meaning changed in the presence of “not.”

The contrast category had the highest accuracy. However, three correct predictions out of four examples are not enough to conclude that the model handles contrast reliably.

## 5. Error Analysis

### 5.1 Negation

All four negation examples were errors:

- “The book is not bad.” was predicted as negative.
- “The service is not terrible.” was predicted as positive.
- “The app is not useful.” was predicted as positive.
- “The film is not enjoyable.” was predicted as positive.

The model's learned weights were associated mainly with individual words such as “terrible,” “useful,” and “enjoyable.” The word “not” was unseen in the development data, so the model had no learned evidence for how to use it. A bag-of-words representation also does not directly encode the scope of negation.

### 5.2 Contrast

Three contrast examples were correct, including examples where the clauses expressed opposing sentiment. One example was wrong:

- “The service is friendly, but it is completely unhelpful.” was predicted as positive.

The positive contribution of “friendly” and the negative contribution of “unhelpful” were nearly balanced. The model did not learn that the second clause can reverse or outweigh the first. The conjunction “but” was also unseen during training.

### 5.3 Sarcasm and irony

Two of four sarcasm examples were errors:

- “Wonderful, my order arrived three hours late.” was predicted as positive.
- “What a surprise: the support team fixed my problem quickly and kindly.” was predicted as negative.

The first error illustrates the effect of literal word matching: “wonderful” was a strong positive feature, while the late-delivery context was mostly unfamiliar. The second sentence was labeled positive because it describes a successful resolution, but its sarcastic opening can create conflicting cues. This example also shows that challenge-set labels may depend on context and intended interpretation.

### 5.4 Lexical shift

Two of four lexical-shift examples were errors:

- “The novel is captivating and rewarding.” was predicted as negative.
- “The meal is scrumptious and flavorful.” was predicted as negative.

The positive words “captivating,” “rewarding,” “scrumptious,” and “flavorful” did not occur in the training vocabulary. The model therefore had little or no direct evidence for the positive sentiment in these sentences. The negative lexical-shift examples were classified correctly, but this small result does not establish that the model handles unfamiliar negative vocabulary well.

## 6. Interpretation

The results reveal limits of the model's representation and training data:

1. **Negation is not adequately represented.** The model learned sentiment from word occurrence but did not learn how “not” changes a sentiment-bearing word.
2. **Unseen vocabulary provides no reliable learned signal.** Words missing from the training vocabulary cannot contribute learned TF-IDF weights.
3. **Sentence-level composition is limited.** A linear model over unigrams and bigrams does not reliably represent clause structure, contrast, or the relative importance of clauses.
4. **Sarcasm requires contextual interpretation.** Literal positive and negative words may point in a different direction from the intended meaning.
5. **High results on a small, controlled test do not guarantee robustness.** Experiment 13's final test was correctly classified, while this challenge set exposed weaknesses. The two sets measure different aspects of behavior.

## 7. Limitations

The challenge set contains only 16 hand-written examples, with four examples per phenomenon. Each accuracy value therefore changes substantially when one item changes. The examples are diagnostic and deliberately challenging; they are not a representative sample of real-world sentiment data.

The development and challenge data are small and manually constructed. Results may depend on the selected vocabulary, phrasing, labels, and topics. In particular, sarcasm can be subjective, and a sentence may require context that is not present in the example.

## 8. Conclusion

Experiment 14 found that the Experiment 13 classifier achieved 0.438 accuracy and 0.435 macro F1 on the challenge set, compared with 0.500 accuracy for the majority baseline. Negation was the clearest failure category, with 0 correct predictions out of 4. The lexical-shift and sarcasm categories each had 2 correct predictions out of 4, while contrast had 3 correct predictions out of 4.

The item-level analysis showed why errors occurred: negation words and several challenge vocabulary items were absent from training, and the model relied on familiar sentiment words without reliably composing their meanings across clauses or interpreting sarcasm. These findings identify concrete targets for future model development, but the small diagnostic set does not support broad claims about general performance.

The challenge examples were kept separate from model fitting and model selection. Any future improvement should be evaluated on new examples that were not used to develop the revised model.
