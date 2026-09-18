# Computerlinguistics Research Bootcamp

A practical one-week training project to prepare for the course:

**Anwendung computerlinguistischer Methoden in einem Forschungsprojekt**

The goal of this project is not only to review theoretical concepts from previous Computerlinguistics courses, but to implement and experiment with them in practice.

---

## Main Goal

The main goal is to build practical experience with the complete workflow of a small Computerlinguistics/NLP research project:

Research Question  
↓  
Dataset / Corpus  
↓  
Data Preparation  
↓  
Linguistic Analysis  
↓  
Method  
↓  
Experiment  
↓  
Evaluation  
↓  
Error Analysis  
↓  
Scientific Report

By the end of the bootcamp, each important concept should have been implemented and experienced at least once.

---

## Concepts Covered

### Text and Corpus Processing

- Corpus
- Dataset
- Document
- Sentence
- Character
- Token
- Type
- Vocabulary
- Frequency
- Frequency Distribution
- Tokenization
- Normalization
- Regular Expressions
- n-grams

### Morphology and Linguistic Processing

- Word structure
- Morphological analysis
- Stemming
- Lemmatization
- Part-of-Speech information
- Linguistic features

### Syntax and Parsing

- Formal grammars
- Context-Free Grammars
- Constituents
- Parse Trees
- Parsing
- Syntactic ambiguity

### Formal Languages

- Regular Languages
- Finite Automata
- States
- Transitions
- Acceptance
- Relationship between Regular Expressions and Automata

### Computational Semantics

- Entities
- Predicates
- Relations
- Semantic representations
- Discourse representation
- Reference and coreference
- DRT-style representations

### Quantitative Methods and Machine Learning

- Probability
- Frequency distributions
- Train/Test Split
- Baselines
- Features
- TF-IDF
- Model Training
- Prediction
- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

### Research Methodology

- Research Questions
- Hypotheses
- Experimental Design
- Baselines
- Evaluation
- Error Analysis
- Interpretation of Results
- Scientific Documentation

---

# Experiments

## Experiment 1 — Corpus / Dataset Analysis

The first experiment introduces the basic structure of linguistic data.

Topics:

- Corpus
- Documents
- Sentences
- Tokens
- Types
- Vocabulary
- Word frequency
- Frequency distributions
- Python file handling

The experiment uses a small text corpus and analyzes its basic properties.

---

## Experiment 2 — Tokenization Error Analysis

A simple regular-expression-based tokenizer is tested on difficult examples.

Test cases include:

- Abbreviations
- Decimal numbers
- URLs
- Email addresses
- Hyphenated expressions
- Contractions
- Uppercase abbreviations

The goal is to understand that tokenization is not simply a technical preprocessing step.

The appropriate tokenization strategy depends on the dataset and the NLP task.

---

## Experiment 3 — Standard NLP Tokenization

Compare:

Custom Regex Tokenizer  
VS  
Standard NLP Tokenizer  
VS  
Gold Standard

Topics:

- NLP libraries
- Tokenization strategies
- Gold standards
- Quantitative evaluation

---

## Experiment 4 — Morphological Processing

Topics:

- Morphological structure
- Stemming
- Lemmatization
- Linguistic features
- Regular expressions

---

## Experiment 5 — n-gram Analysis

Topics:

- Unigrams
- Bigrams
- Trigrams
- Frequency distributions
- Context information

---

## Experiment 6 — Grammar and Parsing

Topics:

- Context-Free Grammar
- Constituency
- Parse Trees
- Parsing
- Ambiguity

---

## Experiment 7 — Formal Languages and Automata

Topics:

- Regular expressions
- Regular languages
- Finite automata
- States
- Transitions
- Acceptance

---

## Experiment 8 — Computational Semantics

Topics:

- Predicates
- Entities
- Relations
- Semantic representations

---

## Experiment 9 — Discourse Representation

Topics:

- Discourse entities
- Reference
- Coreference
- DRT-style representations

---

## Experiment 10 — Probability and Quantitative Analysis

Topics:

- Probability
- Frequencies
- Distributions
- Dataset statistics

---

## Experiment 11 — Machine Learning Baseline

Topics:

- Dataset splitting
- Majority-class baseline
- Features
- Training
- Prediction

---

## Experiment 12 — TF-IDF Text Classification

Topics:

- TF-IDF
- Feature matrices
- Text classification
- Logistic Regression

---

## Experiment 13 — Model Evaluation

Topics:

- Accuracy
- Precision
- Recall
- F1 Score
- Confusion Matrix

---

## Experiment 14 — Error Analysis

Analyze incorrect predictions and identify possible linguistic and methodological reasons for model errors.

---

# Final Research Project

The final project combines the concepts from the previous experiments into one small research project.

The project follows this workflow:

Research Question  
↓  
Hypothesis  
↓  
Dataset  
↓  
Preprocessing  
↓  
Method  
↓  
Baseline  
↓  
Experiment  
↓  
Evaluation  
↓  
Error Analysis  
↓  
Discussion  
↓  
Conclusion

---

# Project Structure

```text
cl-research-bootcamp/
│
├── data/
│   ├── corpus.txt
│   └── tokenization_test.txt
│
├── src/
│   └── analyze_corpus.py
│
├── results/
│   └── experiment_02_error_analysis.md
│
├── README.md
│
└── .gitignore

The project structure will grow as new experiments are added.

Technologies:

The project is primarily implemented with:

Python
Regular Expressions
Git
GitHub
NLP libraries
Machine Learning libraries

Learning Objective

The final objective is to be able to approach a new NLP research problem independently.
I should be able to:

Understand the dataset
Prepare the data
Analyze linguistic properties
Choose a suitable method
Implement the method
Design an experiment
Establish a baseline
Evaluate the result
Analyze errors
Interpret the results
Document the research scientifically
